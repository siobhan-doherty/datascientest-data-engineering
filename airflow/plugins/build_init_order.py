from airflow import DAG, settings
from airflow.operators.python_operator import PythonOperator
from airflow.models.connection import Connection
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.task_group import TaskGroup


# connection configs
postgres_conn_conf = {
    "connection_id": "postgres", "connection_type": "postgres",
    "host": "postgres", "login": "airflow",
    "password": "airflow", "schema": "airflow"
}
fs_default_conn_conf = {
    "connection_id": "fs_default", "connection_type": "File",
    "host": "/opt/airflow/", "login": None,
    "password": None, "schema": None
}
connection_keys = ["connection_id", "connection_type", "host", "login", "password", "schema"]

def create_connection(**kwargs):
    session = settings.Session()
    existing = [c.conn_id for c in session.query(Connection)]
    if kwargs["connection_id"] not in existing:
        params = {k:kwargs[k] for k in connection_keys}
        session.add(Connection(**params))
        session.commit()
    session.close()

def build_init_order(dag: DAG):
    with TaskGroup(group_id = "init_order") as tg:
        pg = PythonOperator(
            task_id = "create_postgres_connnection",
            python_callable = create_connection,
            op_kwargs = postgres_conn_conf,
            dag = dag
        )
        fs = PythonOperator(
            task_id = "create_fs_default_connnection",
            python_callable = create_connection,
            op_kwargs = fs_default_conn_conf,
            dag = dag
        )
        customer = PostgresOperator(
            task_id = "create_table_customer",
            postgres_conn_id = "postgres",
            sql = "sql/create_table_customer.sql",
            dag = dag
        )
        product = PostgresOperator(
            task_id = "create_table_product",
            postgres_conn_id = "postgres",
            sql = "sql/create_table_product.sql",
            dag = dag
        )
        order = PostgresOperator(
            task_id = "create_table_order",
            postgres_conn_id = "postgres",
            sql = "sql/create_table_order.sql",
            dag = dag
        )
        # wiring
        fs
        pg >> [customer, product]
        [customer, product] >> order

    return tg
