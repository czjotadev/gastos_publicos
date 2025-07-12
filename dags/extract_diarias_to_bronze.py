from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import pandas as pd
import requests
from sqlalchemy import create_engine, text

DEFAULT_ARGS = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def extrair_resumo(**kwargs):
    data_ini = kwargs['data_inicial']
    data_fim = kwargs['data_final']
    mode = kwargs['mode']

    base_url = "https://transparencia.al.gov.br/despesa/json-despesa-diarias/"
    limit = 100
    offset = 0
    todos_dados = []

    while True:
        params = {
            "data_registro_dti_": data_ini,
            "data_registro_dtf_": data_fim,
            "limit": limit,
            "offset": offset
        }
        resp = requests.get(base_url, params=params)
        json_data = resp.json()

        rows = json_data.get("rows", [])
        if not rows:
            break
        todos_dados.extend(rows)
        offset += limit
        if offset >= json_data.get("total", 0):
            break

    df = pd.DataFrame(todos_dados)
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")

    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gastos_publicos_bronze"))


    df.to_sql("diarias_resumo", con=engine, schema="gastos_publicos_bronze", if_exists=mode, index=False)
    print(f"{len(df)} registros inseridos em gastos_publicos_bronze.diarias_resumo")

def extrair_favorecidos(**kwargs):
    data_ini = kwargs['data_inicial']
    data_fim = kwargs['data_final']
    mode = kwargs['mode']

    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")
    ugs_df = pd.read_sql("SELECT DISTINCT ug FROM gastos_publicos_bronze.diarias_resumo", con=engine)
    limit = 100
    todos_dados = []

    for ug in ugs_df["ug"]:
        offset = 0
        while True:
            url = f"https://transparencia.al.gov.br/despesa/json-despesa-diarias-ug/{ug}/"
            params = {
                "data_registro_dti_": data_ini,
                "data_registro_dtf_": data_fim,
                "limit": limit,
                "offset": offset
            }
            resp = requests.get(url, params=params)
            json_data = resp.json()

            rows = json_data.get("rows", [])
            if not rows:
                break
            for item in rows:
                item["ug"] = ug
            todos_dados.extend(rows)
            offset += limit
            if offset >= json_data.get("total", 0):
                break

    df = pd.DataFrame(todos_dados)
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gastos_publicos_bronze"))

    df.to_sql("diarias_favorecidos", con=engine, schema="gastos_publicos_bronze", if_exists=mode, index=False)
    print(f"{len(df)} registros inseridos em gastos_publicos_bronze.diarias_favorecidos")

with DAG(
    dag_id='extract_diarias_mensal',
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    catchup=False,
    tags=['gastos_publicos_bronze', 'extracao'],
) as dag:

    task_resumo = PythonOperator(
        task_id='extrair_resumo_diarias',
        python_callable=extrair_resumo,
        op_kwargs={
            'data_inicial': '01/01/2024',
            'data_final': '31/01/2024',
            'mode': 'replace'
        }
    )

    task_favorecidos = PythonOperator(
        task_id='extrair_detalhes_favorecidos',
        python_callable=extrair_favorecidos,
        op_kwargs={
            'data_inicial': '01/01/2024',
            'data_final': '31/01/2024',
            'mode': 'replace'
        }
    )

    task_resumo >> task_favorecidos
