from airflow import DAG
import pendulum
from datetime import datetime, timedelta 
from api.video_stats import get_playlist_id, get_video_ids,extract_video_data,load_to_json

from datawarehouse.dw import staging_table, core_table


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
    dag_id="produce_json",
    default_args=default_args,
    description = "DAG to produce JSON file with raw data",
    schedule="0 14 * * *",
    catchup=False
) as dag:
    
    # Define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json = load_to_json(extract_data)

    # Define dependencies 
    playlist_id >> video_ids >> extract_data >> save_to_json

with DAG(
    dag_id="update_db",
    default_args=default_args,
    description = "DAG to process JSON file and insert data into both staging and core schemas",
    schedule="0 15 * * *",
    catchup=False
) as dag:
    
    # Define tasks
    update_staging = staging_table()
    update_core = core_table()

    # Define dependencies 
    update_staging >> update_core