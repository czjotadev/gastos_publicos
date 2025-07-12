#!/bin/bash

echo "🔧 Preparando diretórios necessários..."

mkdir -p dags
mkdir -p logs/scheduler
mkdir -p logs/webserver
mkdir -p plugins
mkdir -p notebooks

echo "🛠️ Ajustando permissões para os diretórios..."
chmod -R 777 logs
chmod -R 777 plugins
chmod -R 777 notebooks

echo "🚀 Inicializando o container do Postgres..."
docker-compose up -d postgres

echo "⚙️ Executando o airflow-init (apenas na primeira vez)..."
docker-compose run --rm airflow-init

echo "📡 Subindo webserver, scheduler, dbt, jupyter e metabase..."
docker-compose up -d airflow-webserver airflow-scheduler dbt jupyter metabase

echo "⏳ Aguardando os serviços serem disponibilizados..."
sleep 30

echo
echo "✅ Tudo pronto!"
echo "- Airflow: http://localhost:8080"
echo "- Jupyter: http://localhost:8888"
echo "- Metabase: http://localhost:3000"
