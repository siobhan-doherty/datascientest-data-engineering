from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import os
import datetime


def failed_task():
    raise Exception("This task did not work!")

# email address in .env
ALERT_EMAIL = os.environ.get("ALERT_EMAIL")

with DAG(
    dag_id = "notifications_dag",
    description = "Retries + email notifications on failure",
    schedule_interval = None,
    catchup = False,
    default_args = {
        "owner": "airflow",
        "start_date": days_ago(0, minute=1),
    },
    tags = ["tutorial", "datascientest"]
) as dag:

    task1 = PythonOperator(
        task_id = "my_failed_task",
        python_callable = failed_task,
        retries = 5,
        retry_delay = datetime.timedelta(seconds=30),

        email_on_retry = True,
        email_on_failure = True,
        email = [ALERT_EMAIL]
    )
