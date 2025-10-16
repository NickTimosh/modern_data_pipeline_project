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
    dag_id="data_quality",
    default_args=default_args,
    description = "DAG to trigger soda checks",
    schedule=None,
    catchup=False
) as dag_quality:
    
    # Define tasks
    soda_validate_staging = yt_elt_data_quality("staging")
    soda_validate_core= yt_elt_data_quality("core")

    # Define dependencies 
    soda_validate_staging >> soda_validate_core