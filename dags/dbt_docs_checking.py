from airflow import DAG
from scripts.telegram_webhook import telegramm_alert
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow.operators.bash import BashOperator

default_args = {
  'owner': 'Baikulov',
  'depends_on_past': False,
  'email': ['baikulov.ant@gmail.com'],
  'dir': '/opt/airflow/dags/scripts/dbt',
  'start_date': datetime(2022, 6, 1, 17, 30),
}

dag = DAG(
  dag_id='dbt_docs_test_check',
  default_args=default_args,
  schedule_interval='@daily',
  max_active_runs=1,
)

dbt_deps = BashOperator(
    task_id='dbt_deps',
    bash_command="cd /opt/airflow/dags/scripts/dbt && dbt deps",
)

dbt_check = BashOperator(
    task_id='dbt_run_docs',
    bash_command="cd /opt/airflow/dags/scripts/dbt && dbt run-operation required_docs",
)

dbt_check >> dbt_check