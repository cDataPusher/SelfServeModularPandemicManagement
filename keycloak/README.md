# Airflow with Keycloak Integration

This guide will help you set up Keycloak as an Identity and Access Management solution for Apache Airflow.

## Prerequisites

- Docker and Docker Compose installed
- Apache Airflow set up

## Keycloak Setup

1. Start Keycloak and Postgres services using Docker Compose:

```bash
docker-compose -f keycloak-compose.yml up
```

1. Open Keycloak admin console at http://localhost:8080/auth/admin/. Use admin as both username and password.
2. Create a new realm for your application.
3. In the new realm, create a new client for Apache Airflow.
4. Set Access Type to confidential and Valid Redirect URIs to your Airflow webserver's URL.
5. In the Credentials tab, note down the Secret value. This will be used as KEYCLOAK_CLIENT_SECRET in Airflow's configuration.
6. Create roles corresponding to Airflow's roles (Admin, User, Viewer, Op, Public) in the Roles tab of the client.
7. Create users and assign them roles as needed.

## Airflow Configuration
1. In your Airflow's webserver_config.py, set AUTH_TYPE to AUTH_OAUTH.
2. Set the following environment variables in your Airflow's configuration:
`KEYCLOAK_AUTH`: Set to true to enable Keycloak authentication.
`KEYCLOAK_BASE_URL`: The URL of your Keycloak server.
`KEYCLOAK_REALM`: The realm you created in Keycloak.
`KEYCLOAK_CLIENT_ID`: The client ID of the client you created in Keycloak.
`KEYCLOAK_CLIENT_SECRET`: The client secret you noted down earlier.
`KEYCLOAK_ROLES_SYNC_AT_LOGIN`: Set to true to sync roles at login.

3. Restart your Airflow webserver.

Now, your Airflow instance should use Keycloak for authentication and role management.