from airflow import DAG
from airflow_dbt.operators.dbt_operator import (
    DbtRunOperator,
    DbtTestOperator
)
from airflow.utils.dates import days_ago

default_args = {
  'dir': './dbt',
  'start_date': days_ago(0)
}

with DAG(dag_id='dbt', default_args=default_args, schedule_interval='@daily') as dag:

  dbt_run = DbtRunOperator(
    task_id='dbt_run',
    profiles_dir='./dbt/',
    dbt_bin='/usr/local/bin/dbt'
  )

  dbt_test = DbtTestOperator(
    task_id='dbt_test',
    retries=0,  # Failing tests would fail the task, and we don't want Airflow to try again
    profiles_dir='./dbt/',
    dbt_bin='/usr/local/bin/dbt'
  )

  dbt_run >> dbt_test