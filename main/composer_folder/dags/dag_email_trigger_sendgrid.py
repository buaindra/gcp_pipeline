import datetime
import airflow
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator

default_args={
    "owner": "Airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=1)  # datetime.timedelta(days=1)
}

with airflow.DAG(
    "composer_sample_sendgrid",
    start_date=datetime.datetime(2022, 7, 1),
    default_args = default_args,
    schedule_interval="@once",
    catchup=False,
) as dag:
    start = DummyOperator(task_id="start", dag=dag)
    end = DummyOperator(task_id="end", dag=dag)

    task_email = EmailOperator(
        task_id='send-email',
        conn_id='sendgrid_default',
        # You can specify more than one recipient with a list.
        to='indra.tutun@gmail.com',
        subject='EmailOperator test for SendGrid',
        html_content='This is a test message sent through SendGrid.',
        dag=dag,
    )

    start >> task_email >> end