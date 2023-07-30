from datetime import timedelta

import pendulum
import pytz
from airflow.hooks.base import BaseHook
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.slack.operators.slack_webhook import \
    SlackWebhookOperator
from docker.types import Mount
from airflow.models import Variable

from airflow import DAG

SLACK_CONN_ID = 'slack'
MOUNT_PATH = Variable.get('local_logs')
NETWORK_ID = Variable.get('network_id')

def convert_datetime(datetime_string):

    return datetime_string.astimezone(pytz.timezone('Europe/Paris')).strftime('%b-%d %H:%M:%S')


##### Slack Alerts #####
def slack_fail_alert(context):
    # Called on failure
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    channel = BaseHook.get_connection(SLACK_CONN_ID).login
    slack_msg = f"""
        :x: Task Failed.
        *Task*: {context.get('task_instance').task_id}
        *Dag*: {context.get('task_instance').dag_id}
        *Execution Time*: {convert_datetime(context.get('execution_date'))}
        <{context.get('task_instance').log_url}|*Logs*>
    """

    slack_alert = SlackWebhookOperator(
        task_id='slack_fail',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        channel=channel,
        username='airflow',
        http_conn_id=SLACK_CONN_ID
    )

    return slack_alert.execute(context=context)


def slack_succeed_alert(context):
    # Called on success
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    channel = BaseHook.get_connection(SLACK_CONN_ID).login
    slack_msg = f"""
        :white_check_mark: Task Succeed.
        *Task*: {context.get('task_instance').task_id}
        *Dag*: {context.get('task_instance').dag_id}
        *Execution Time*: {convert_datetime(context.get('execution_date'))}
        <{context.get('task_instance').log_url}|*Logs*>
    """

    slack_alert = SlackWebhookOperator(
        task_id='slack_success',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        channel=channel,
        username='airflow',
        http_conn_id=SLACK_CONN_ID
    )

    return slack_alert.execute(context=context)


default_args = {
                'owner': 'NYT_team',
                'start_date': pendulum.datetime(2023, 7, 26, 00, 00, tz="Europe/Paris"),
                'retries': 1,
                'retry_delay': timedelta(seconds=30),
                'on_failure_callback': slack_fail_alert,
                'on_success_callback': slack_succeed_alert
                }

dag = DAG(
            dag_id='nyt_etl_dag',
            description='Check if Elasticsearch service is available / healthy and if yes, runs the ETL',
            doc_md=''' # Run ETL dag
            This DAG check if Elasticsearch service is available / healthy
            If yes, it runs ETL and sends a slack notification with running final status: succeed / failed 
            ''',
            tags=['NYT', 'ETL', 'datascientest'],
            default_args=default_args,
            schedule_interval='0 9 * * *',
            catchup=False
)

elastic_healthcheck = DockerOperator(
    image='curlimages/curl',
    command='curl -u elastic:elastic -s -f es-container:9200/_cat/health',
    network_mode=NETWORK_ID,
    auto_remove=True,
    task_id='elastic_healthcheck',
    doc_md=''''# elastic_healthcheck
    Task that checks Elastisearch by sending and http request''',
    dag=dag,
    retries=5
)


run_etl = DockerOperator(
    image='cedricsoares/ny_times-etl:1.0.0',
    mounts=[
        Mount(
            source=MOUNT_PATH,
            target='/app/logs',
            type='bind'
        )
    ],
    network_mode=NETWORK_ID,
    auto_remove=True,
    task_id='run_etl',
    doc_md=''''# run_etl
    Task that runs ETL''',
    dag=dag,
    retries=5
)


elastic_healthcheck >> run_etl
