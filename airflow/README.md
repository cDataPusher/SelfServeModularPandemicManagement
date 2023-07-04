# Apache Superset Testing Setup

This repository contains a Docker Compose setup for testing Apache Superset.

## Getting Started

Follow these steps to get Apache Superset running on your local machine for development and testing purposes.


### 1. Navigate to the Repository Directory
```bash
cd airflow
```


### 2. Start the Services
```bash
docker compose up
```
Once the services are running, you can access the Airflow web interface at http://localhost:8080.

## Docker Compose File

The `docker-compose.yaml` file defines the services, networks, and volumes for the Airflow setup. Each service uses the Apache Airflow Docker image and has the Airflow DAGs and plugins directories mounted into the container.

## Configuration

The Docker Compose file uses several environment variables to configure the Airflow services. These variables can be set in an `.env` file in the same directory as the Docker Compose file. Here are the variables used:

- `POSTGRES_USER`: The username for the Postgres database. Default is `airflow`.
- `POSTGRES_PASSWORD`: The password for the Postgres database. Default is `airflow`.
- `POSTGRES_DB`: The name of the Postgres database. Default is `airflow`.
- `AIRFLOW_VERSION`: The version of the Apache Airflow Docker image to use. Default is `2.6.2.004`.
- `FERNET_KEY`: The Fernet key for Airflow to secure sensitive data. This should be a base64-encoded 32-byte key. You can generate one with `openssl rand -base64 32`.
- `AIRFLOW__WEBSERVER__SECRET_KEY`: The secret key for the Airflow webserver. This should be a hexadecimal string. You can generate one with `openssl rand -hex 32`.
- `HOST_PROTOCOL`: The protocol for the Airflow webserver's base URL. Default is `http`.
- `HOST_NAME`: The host name for the Airflow webserver's base URL. Default is `localhost:8080`.


## Keycloak Integration
Superset can be integrated with Keycloak for authentication. This is disabled by default for testing purposes but can be enabled via the ENABLE_KEYCLOAK environment variable in the superset_config.py file.

To enable Keycloak integration, set ENABLE_KEYCLOAK to True. Additionally, set the following environment variables in the docker-compose.yml file:

- `KEYCLOAK_BASE_URL`: Your Keycloak base URL.
- `KEYCLOAK_CLIENT_ID`: Your Keycloak client ID.
- `KEYCLOAK_CLIENT_SECRET`: Your Keycloak client secret.

The enabling can be done in the superset_config.py:
```python
ENABLE_KEYCLOAK = True
```
Make sure Keycloak is running and properly configured before enabling integration in Superset.
Remember to set your environment variables in the .env file or in your shell before starting the environment.


You can add rights for airflow to download data:
```bash
docker exec -u 0 airflow_webserver_1 chown -R airflow: /opt/airflow/airflow_dag_data
```
