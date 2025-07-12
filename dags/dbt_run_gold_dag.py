from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='dbt_run_gold_dag',
    default_args=default_args,
    description='Executa os modelos da camada gold no DBT',
    schedule_interval=None,
    catchup=False,
    tags=['gastos_publicos_gold', 'carregamento'],
) as dag:

    dbt_run_gold = BashOperator(
        task_id='run_dbt_gold',
        bash_command='cd /opt/airflow/dbt && dbt run --select models/gold',
    )
