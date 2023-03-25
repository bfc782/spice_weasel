"""
Simple example of a DAG
"""
##### 1. Import modules #####
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


##### 2. Define default arguments #####
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2022, 5, 11),
    "email": ["bfc782@hotmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    'end_date': datetime(2022, 5, 12),
}

##### 3. Instantiate DAG #####
dag = DAG("tutorial", default_args=default_args, schedule_interval=timedelta(minutes=5))

##### 4. Create Tasks #####
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

##### 5. Set up dependencies #####
t1 >> t2
# t2 << t1
# t1.set_downstream(t2)
# t2.set_upstream(t1)
