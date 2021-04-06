from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['pawel.k.lonca@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'first_dag_PL',
    default_args=default_args,
    description='Test DAG by PL',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['test', 'nozbe'],
)

t1 = BashOperator(
    task_id='print_greetings',
    bash_command='echo "Hello, world!"',
    dag=dag,
)

t2 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t1 >> t2
