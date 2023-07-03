# Superset Testing Setup

This repository contains a setup for testing Apache Superset with Docker Compose.

##Getting Started

1. Clone this repository:

```bash
git clone <repository_url>
```

2. Navigate to the repository directory:
```bash
cd <repository_directory>
```

3. Start the services:
```bash
docker-compose up
```

Once the services are running, you can access the Superset web interface at http://localhost:8088.

## Configuration
The superset_config.py file contains the necessary configuration for running Superset with a PostgreSQL database and a Redis instance. This file is mounted into the Superset Docker service at /app/superset/superset_config.py. You can modify this file to change the configuration.

## Keycloak Configuration
This setup includes optional support for Keycloak as an OAuth provider. You can enable this by setting the ENABLE_KEYCLOAK environment variable to "true" in the docker-compose.yml file. You also need to set the KEYCLOAK_BASE_URL, KEYCLOAK_CLIENT_ID, and KEYCLOAK_CLIENT_SECRET environment variables to your actual Keycloak base URL, client ID, and client secret, respectively.