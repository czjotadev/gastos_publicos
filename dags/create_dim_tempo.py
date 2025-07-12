import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema

datas = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

df = pd.DataFrame()
df['data'] = datas
df['ano'] = df['data'].dt.year
df['mes'] = df['data'].dt.month
df['dia'] = df['data'].dt.day
df['nome_mes'] = df['data'].dt.month_name(locale='pt_BR')
df['dia_da_semana'] = df['data'].dt.day_name(locale='pt_BR')
df['fim_de_semana'] = df['dia_da_semana'].isin(['sábado', 'domingo'])
df['trimestre'] = df['data'].dt.quarter

engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))

df.to_sql("dim_tempo", con=engine, schema="gold", if_exists="replace", index=False)
print(f"Inserido {len(df)} registros na tabela gold.dim_tempo")
