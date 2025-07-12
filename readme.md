# ℹ️ Informações

Este projeto foi desenvolvido por **Julio Cesar de Araújo Santos** e **Ramon Bomfim** como parte da disciplina **Engenharia de Dados I**, da pós-graduação em Inteligência Artificial e Ciência de Dados.

---

# 🚀 Pipeline de Dados com Airflow, Postgres, DBT e Jupyter

Este projeto configura uma pipeline de dados local usando Docker Compose, incluindo:

- Apache Airflow (Webserver, Scheduler e Init)
- PostgreSQL
- DBT
- Jupyter Notebook (opcional)
- Metabase (opcional)

---

## ✅ Pré-requisitos

Antes de rodar o projeto, é necessário ter instalado na máquina:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Git Bash ou WSL (para Windows) — recomendado se for usar o `.sh`

---

## 📁 Estrutura do Projeto

 - dags/                # DAGs do Airflow
 - logs/                # Logs gerados pelo Airflow
- plugins/             # Plugins do Airflow (opcional)
- dbt/                 # Projeto DBT
- .dbt/                # Profiles DBT (config local)
- docker-compose.yml   # Compose com os serviços
- start_pipeline.sh    # Script para rodar em Linux/macOS
- start_pipeline.bat   # Script para rodar em Windows

---

## ▶️ Como Rodar a Pipeline

### 💻 Linux/macOS

```bash
chmod +x start_pipeline.sh
./start_pipeline.sh
```

### 🪟 Windows

1. Dê dois cliques no arquivo `start_pipeline.bat`

Ou, via terminal CMD ou PowerShell:

```bat
start_pipeline.bat
```

---

## 🌐 Acessos

- **Airflow**: [http://localhost:8080](http://localhost:8080)
- **Usuário**: `admin`
- **Senha**: `admin`

