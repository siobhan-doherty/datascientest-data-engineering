from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


def print_var():
    print("my_param =", Variable.get("my_param"))

with DAG(
    dag_id = "var_reader_dag",
    schedule_interval = None,
    tags = ["tutorial", "datascientest"],
    start_date = days_ago(0)
) as dag:
    read = PythonOperator(
        task_id = "print_variable",
        python_callable = print_var
    )
