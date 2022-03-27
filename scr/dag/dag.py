from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator

from airflow_dbt.operators.dbt_operator import (
    DbtRunOperator,
    DbtTestOperator
)
from airflow.utils.dates import days_ago

default_args = {
  'start_date': days_ago(0),
  'retries': 1,
  'retry_delay': timedelta(days=1),
}

with DAG(dag_id='etl', default_args=default_args, schedule_interval='@daily') as dag:
  ge_check = BashOperator(
    task_id = "checkpoint_run",
    bash_command = "(cd ../great_expectations/ ; great_expectations --v3-api checkpoint run checkpoint_customer )",
    depends_on_past = False
  )
  
  dbt_test = DbtTestOperator(
    task_id='dbt_test',
    retries=0,  # Failing tests would fail the task, and we don't want Airflow to try again
    profiles_dir='../dbt/',
    dbt_bin='/usr/local/bin/dbt'
  )

  dbt_run = DbtRunOperator(
    task_id='dbt_run',
    profiles_dir='../dbt/',
    dbt_bin='/usr/local/bin/dbt'
  )

  

  ge_check >> dbt_test >> dbt_run