import datetime
import airflow
from airflow.operators.email import EmailOperator

with airflow.DAG(
    "composer_sample_sendgrid",
    start_date=datetime.datetime(2022, 1, 1),
    schedule_interval="@once",
) as dag:

    task_email = EmailOperator(
        task_id='send-email',
        conn_id='sendgrid_default',
        # You can specify more than one recipient with a list.
        to='user@example.com',
        subject='EmailOperator test for SendGrid',
        html_content='This is a test message sent through SendGrid.',
        dag=dag,
    )

    task_email