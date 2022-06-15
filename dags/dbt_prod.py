from airflow import DAG
from scripts.telegram_webhook import telegramm_alert
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow_dbt.operators.dbt_operator import (
     DbtSeedOperator,
     DbtSnapshotOperator,
     DbtRunOperator,
     DbtTestOperator
)

default_args = {
  'owner': 'Baikulov',
  'depends_on_past': False,
  'email': ['baikulov.ant@gmail.com'],
  'dir': '/opt/airflow/dags/scripts/cable_dbt_clickhouse',
  'start_date': datetime(2019, 1, 1, 17, 30),
}

dag = DAG(
  dag_id='dbt_prod_clickhouse',
  default_args=default_args,
  schedule_interval='@daily',
  max_active_runs=1,
)

dbt_test_sources = DbtTestOperator(
  task_id='dbt_test_sources',
  dag=dag,
  target="dev",
  select="source:*",
  vars={'execution_date': "'{{ macros.ds_add(ds, -1) }}'"},  # передаём дату(дата выполнения - 1) внутрь dbt
  dbt_bin='/home/airflow/.local/bin/dbt',
  profiles_dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  on_failure_callback=telegramm_alert,
)


dbt_run_dev = DbtRunOperator(
  task_id='dbt_run_dev',
  dag=dag,
  target="dev",
  vars={'execution_date': "'{{ macros.ds_add(ds, -1) }}'"},  # передаём дату(дата выполнения - 1) внутрь dbt
  dbt_bin='/home/airflow/.local/bin/dbt',
  profiles_dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  on_failure_callback=telegramm_alert,
)

dbt_test_dev = DbtTestOperator(
  task_id='dbt_test_dev',
  dag=dag,
  target="dev",
  profiles_dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  on_failure_callback=telegramm_alert,
)

dbt_run_prod = DbtRunOperator(
  task_id='dbt_run_prod',
  dag=dag,
  target="prod",
  select="tag:presets",
  vars={'execution_date': "'{{ macros.ds_add(ds, -1) }}'"},  # передаём дату(дата выполнения - 1) внутрь dbt
  dbt_bin='/home/airflow/.local/bin/dbt',
  profiles_dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  dir='/opt/airflow/dags/scripts/cable_dbt_clickhouse/',
  on_failure_callback=telegramm_alert,
)

dbt_test_sources >> dbt_run_dev >> dbt_test_dev >> dbt_run_prod