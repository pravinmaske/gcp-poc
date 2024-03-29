from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

default_args ={
    'owner': 'Pravin Maske',
    'start_date': datetime(2024, 3, 28),
    'depends_on_past': False,
    'email': ['gcppravindev3@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG('Employee_Data',
          default_args=default_args,
          description= 'Runs an external Python script to load data in BQ',
          schedule_interval='@daily',
          catchup=False)

with dag:
    run_data_extractor = BashOperator(
        task_id= 'run_data_extractor',
        bash_command='python /home/airflow/gcs/dags/scripts/extract.py'
    )

    start_pipeline = CloudDataFusionStartPipelineOperator(
        location='us-central1',
        pipeline_name='etl_pipeline',
        instance_name="fusion-dev1",
        task_id="start_datafusion_pipeline",
    )
    run_data_extractor >> start_pipeline

