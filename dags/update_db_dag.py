from airflow import DAG
import pendulum
from datetime import datetime, timedelta 
from api.video_stats import get_playlist_id, get_video_ids,extract_video_data,load_to_json
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datawarehouse.dw import staging_table, core_table
from dataquality.soda import yt_elt_data_quality

local_tz = pendulum.timezone("UTC")

default_args = {
    "owner": "DE",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "de@gmail.com",
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrum_timeout": timedelta(hours=1),
    "start_date": datetime(2025,1,1,tzinfo=local_tz),
    # "end_date": datetime(2025,12,31,tzinfo=local_tz)
}

with DAG(
    dag_id="update_db",
    default_args=default_args,
    description = "DAG to process JSON file and insert data into both staging and core schemas",
    schedule=None,
    catchup=False
) as dag_update:
    
    # Define tasks
    update_staging = staging_table()
    update_core = core_table()

    trigger_data_quality = TriggerDagRunOperator(
        task_id="trigger_data_quality",
        trigger_dag_id="data_quality"
    )

    # Define dependencies 
    update_staging >> update_core >> trigger_data_quality