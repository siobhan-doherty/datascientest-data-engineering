from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator


with DAG(
    dag_id = 'my_dag_of_the_morning',
    description = 'DAG describing my morning routine',
    tags = ['tutorial', 'datascientest'],
    schedule_interval = None,
    default_args = {
        'owner': 'airflow',
        'start_date': days_ago(2),
    }
) as my_dag:

    def print_task(step):
        print(step)

    texts = [
        'Put on trousers',
        'Put on right sock',
        'Put on left sock',
        'Put on right trainer',
        'Put on left trainer',
        'Start moving'
    ]

    ids = [
        'trousers',
        'right_sock',
        'left_sock',
        'right_trainer',
        'left_trainer',
        'exit'
    ]

    tasks = []
    for t, task_id in zip(texts, ids):
        op = PythonOperator(
            task_id = task_id,
            python_callable = print_task,
            op_kwargs = {'step': t},
        )
        tasks.append(op)

    tasks[0] >> [tasks[1], tasks[3]]
    tasks[1] >> tasks[2]
    tasks[3] >> tasks[4]
    [tasks[2], tasks[4]] >> tasks[5]
