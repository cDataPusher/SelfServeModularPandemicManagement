# Airflow Docker Compose Setup

This folder contains a Docker Compose file for setting up an Apache Airflow environment for local development and testing. The setup includes a Postgres database, an Airflow webserver, a scheduler, and a worker.

## Docker Compose File

The `docker-compose.yaml` file defines the services, networks, and volumes for the Airflow setup. Each service uses the Apache Airflow Docker image and has the Airflow DAGs and plugins directories mounted into the container.

## Environment Variables

The Docker Compose file uses several environment variables to configure the Airflow services. These variables can be set in an `.env` file in the same directory as the Docker Compose file. Here are the variables used:

- `POSTGRES_USER`: The username for the Postgres database. Default is `airflow`.
- `POSTGRES_PASSWORD`: The password for the Postgres database. Default is `airflow`.
- `POSTGRES_DB`: The name of the Postgres database. Default is `airflow`.
- `AIRFLOW_VERSION`: The version of the Apache Airflow Docker image to use. Default is `2.6.2.004`.
- `FERNET_KEY`: The Fernet key for Airflow to secure sensitive data. This should be a base64-encoded 32-byte key. You can generate one with `openssl rand -base64 32`.
- `AIRFLOW__WEBSERVER__SECRET_KEY`: The secret key for the Airflow webserver. This should be a hexadecimal string. You can generate one with `openssl rand -hex 32`.
- `HOST_PROTOCOL`: The protocol for the Airflow webserver's base URL. Default is `http`.
- `HOST_NAME`: The host name for the Airflow webserver's base URL. Default is `localhost:8080`.

## Usage

To start the Airflow environment, run the following command in the same directory as the Docker Compose file:

```bash
docker-compose up
```

To stop the environment, use the following command:

```bash
docker-compose down
```

You can access the Airflow webserver at http://localhost:8080 (or whatever you set as the HOST_NAME and HOST_PROTOCOL).

Remember to set your environment variables in the .env file or in your shell before starting the environment.


docker exec -u 0 airflow_webserver_1 chown -R airflow: /opt/airflow/airflow_dag_data
