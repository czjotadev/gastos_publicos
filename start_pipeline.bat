@echo off
echo ==========================
echo 🔧 Preparando estrutura
echo ==========================

if not exist "dags" (
    mkdir dags
)

if not exist "logs" (
    mkdir logs
)

if not exist "logs\scheduler" (
    mkdir logs\scheduler
)

if not exist "logs\webserver" (
    mkdir logs\webserver
)

if not exist "plugins" (
    mkdir plugins
)

if not exist "notebooks" (
    mkdir notebooks
)

echo ==========================
echo 🚀 Iniciando containers
echo ==========================

echo - Iniciando o Postgres...
docker-compose up -d postgres

echo - Executando airflow-init (apenas na primeira vez)...
docker-compose run --rm airflow-init

echo - Subindo webserver, scheduler, dbt, jupyter e metabase...
docker-compose up -d airflow-webserver airflow-scheduler dbt jupyter metabase

echo.
echo ==========================
echo ✅ Tudo pronto!
echo - Airflow: http://localhost:8080
echo - Jupyter: http://localhost:8888
echo - Metabase: http://localhost:3000
echo ==========================
pause
