from datetime import timedelta
import os

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

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

def validate(**context):
    from great_expectations.data_context import DataContext

    conn = BaseHook.get_connection('bigquery_sasakky')
    connection_json = conn.extra_dejson
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = connection_json['/run/secrets/gcp_secret']

    data_context: DataContext = DataContext(context_root_dir="/usr/app/great_expectations")

    result = data_context.run_checkpoint(
        checkpoint_name="checkpoint_customer",
        batch_request=None,
        run_name=None,
    )

    data_context.build_data_docs()

    if not result["success"]:
        raise AirflowException("Validation of the data is not successful ")

with DAG(dag_id='etl', default_args=default_args, schedule_interval='@daily') as dag:
  ge_check = PythonOperator(
        task_id='validate',
        python_callable=validate,
        provide_context=True,
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