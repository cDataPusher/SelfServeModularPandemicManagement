# Keycloak Integration with Apache Airflow and Superset

This guide will help you set up Keycloak as an Identity and Access Management (IAM) solution for Apache Airflow and Apache Superset.

## Prerequisites

- Docker and Docker Compose installed
- Apache Airflow set up
- Apache Superset set up

## Keycloak Setup

1. Start Keycloak using Docker Compose.
2. Open Keycloak admin console at `http://localhost:8081/auth/admin/`. Use `admin` as both username and password.
3. Create a new realm for your applications. The realm will be a logical container for all the users, roles, and clients.

### Adding Users

1. In the Keycloak admin console, go to your realm and click on `Users` in the left-hand menu.
2. Click on `Add User` and enter the relevant details such as username and email.
3. After saving, go to the `Credentials` tab to set a password for the user.
4. Go to the `Role Mappings` tab to assign roles to the user.

### Creating Roles

1. In the Keycloak admin console, go to your realm and click on `Roles` in the left-hand menu.
2. Click on `Add Role` and provide a name.
3. Create roles corresponding to Airflow's and Superset’s roles (e.g., Admin, User, Viewer).

### Creating Clients

1. Go to `Clients` and click `Create`.
2. Set `Client ID` and save.
3. Set `Access Type` to `confidential`.
4. In the `Credentials` tab, note down the `Secret` value.
5. In `Scope` tab, ensure that the roles you want to use are in the `Assigned Roles` box.

## Configuring Apache Airflow for Keycloak

1. In your Airflow's `webserver_config.py`, set `AUTH_TYPE` to `AUTH_OAUTH`.
2. Set the following environment variables in your Airflow configuration:
    - `KEYCLOAK_AUTH`: Set to `True` to enable Keycloak authentication.
    - `KEYCLOAK_BASE_URL`: The URL of your Keycloak server.
    - `KEYCLOAK_REALM`: The realm you created in Keycloak.
    - `KEYCLOAK_CLIENT_ID`: The client ID of the client you created in Keycloak.
    - `KEYCLOAK_CLIENT_SECRET`: The client secret you noted down.
    - `KEYCLOAK_ROLES_SYNC_AT_LOGIN`: Set to `True` to sync roles at login.

3. Restart your Airflow webserver.

## Configuring Apache Superset for Keycloak

1. In your Superset's `superset_config.py`, set the `ENABLE_KEYCLOAK` environment variable to `True`.
2. Set the following environment variables in your Superset configuration:
    - `KEYCLOAK_BASE_URL`: The URL of your Keycloak server.
    - `KEYCLOAK_CLIENT_ID`: The client ID of the client you created in Keycloak.
    - `KEYCLOAK_CLIENT_SECRET`: The client secret you noted down.

3. Restart your Superset webserver.

Now, your Airflow and Superset instances should use Keycloak for authentication and role management. Users and roles created in Keycloak can be synchronized with Apache Airflow and Apache Superset.