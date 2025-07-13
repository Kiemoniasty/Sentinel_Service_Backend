<div align='center'>

<img src="https://github.com/user-attachments/assets/7571f879-c872-40ad-ab44-38845900a6a2" style="width: 40%; max-width: 250px;"/>

<br>

<h3>Service Sentinel is a backend service designed for efficient and real-time tracking of system components. Built with Flask, SQLAlchemy, and InfluxDB, it supports user management, logging, and metric collection.</h3>

<br>

### Navigation

[Overview](#overview) | [Tech Stack](#tech-stack) | [How to Install](#how-to-install) | [Progress](#progress)

</div>

<br>
<br>

## Overview

<div align='justify'>
Service Sentinel is a backend platform designed for tracking service states, user management, and real-time notification logging. It exposes a RESTful API for frontend or system integrations and uses a modular Python architecture for scalability and maintainability.

<br>

Related Projects:

<ul>
  <li><a href="https://github.com/Kiemoniasty/Sentinel_Service_Frontend">Sentinel Service Backend</a></li>
</ul>


<br>

Key features include:

<ul>
  <li>Token-based (JWT) authentication</li>
  <li>Service registration and status tracking</li>
  <li>Custom user roles and management</li>
  <li>InfluxDB integration for time-series metrics</li>
  <li>PostgreSQL with SQLAlchemy ORM</li>
</ul>
</div>

<br>

## Tech stack

| Category       | Technology            |
| -------------- | --------------------- |
| Language       | Python 3.8+           |
| Framework      | Flask                 |
| ORM            | SQLAlchemy            |
| Authentication | JWT (JSON Web Tokens) |
| Time-Series DB | InfluxDB              |
| Relational DB  | PostgreSQL            |
| Architecture   | Modular / MVC-like    |

<br>

## How to Install

<details>
<summary>🔧 Local setup</summary>

```bash
# Clone the repository
git clone https://github.com/kiemoniasty/service_sentinel_backend.git
cd service_sentinel_backend

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate #on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file
cp .env.example .env
```

 OR manually create .env and paste the following:

</details> <details> <summary>📄 .env example</summary>

```bash
# PostgreSQL database URLs
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/postgres
SENTINEL_URL=postgresql://postgres:PASSWORD@localhost:5432/sentinel_db
USER_URL=postgresql://postgres:PASSWORD@localhost:5432/users_db

# Postgres connection details
POSTGRES=Postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=PASSWORD

# Database names
POSTGRES_DB_NAME=postgres
SENTINEL_DB_NAME=sentinel_db
USER_DB_NAME=users_db

# InfluxDB settings
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=api_token
INFLUXDB_ORG=Service-Sentinel
```

</details> <details> <summary>▶️ Run the app</summary>

```bash
# Run app
python main.py
```

</details> 
<br>

## Progress

| Feature                             | Status |
| ----------------------------------- | ------ |
| REST API for user & service control | ✅      |
| InfluxDB metrics logging            | ✅      |
| JWT auth & token handling           | ✅      |
| PostgreSQL integration (SQLAlchemy) | ✅      |
| Configurable routes / endpoints     | ✅      |
| Logging system                      | ✅      |

<br>

✅ done
🛠️ in progress
🕒 planned
