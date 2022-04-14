from datetime import timedelta
import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow import AirflowException

from airflow_dbt.operators.dbt_operator import (
    DbtRunOperator,
    DbtTestOperator
)
from airflow.utils.dates import days_ago


default_args = {
  'start_date': days_ago(0),
  'retries': 0,
}

def validate(**context):
    from great_expectations.data_context import DataContext

    conn = BaseHook.get_connection('sasakky_bigquery')
    connection_json = conn.extra_dejson
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = connection_json['extra__google_cloud_platform__keyfile_dict']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = connection_json['extra__google_cloud_platform__key_path']

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
    retries=0,
    profiles_dir='/usr/app/dbt',
    dbt_bin='/usr/local/bin/dbt',
    dir='/usr/app/dbt'
  )

  dbt_run = DbtRunOperator(
    task_id='dbt_run',
    profiles_dir='/usr/app/dbt',
    dbt_bin='/usr/local/bin/dbt',
    dir='/usr/app/dbt'
  )

  
  ge_check >> dbt_run >> dbt_test 