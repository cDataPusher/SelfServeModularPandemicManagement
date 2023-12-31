# Supporting Regional Pandemic Management by Enabling Self-Service Reporting Through Modularisation

This repository contains the code and configurations for the paper "Supporting regional pandemic management by enabling self-service reporting through modularisation". The system is built using open-source technologies and follows a dataflow-driven approach.

## Overview

The system is designed to cater to three main user groups:

1. **Data Suppliers**: These include clinics, health offices, National Institute of Health and Veterinary Inspection, and publicly available data sources.
2. **Data Processors**: These include local research facilities such as the Center for Evidence-Based Health Care and the Center for Medical Informatics of the TU-Dresden.
3. **Data Users**: These include clinical control centers for patient disposition, clinical management, and legal governmental and non-governmental entities.

The system is composed of several interconnected components that work together to facilitate data processing, storage, and visualization:

1. **Data Processing**: This is handled by [Apache Airflow](./airflow/README.md), an orchestration tool that automates the flow of data from suppliers to storage. It can be scheduled to retrieve, process, and store data efficiently.
2. **Data Storage**: This is handled by a [PostgreSQL Database](https://www.postgresql.org/docs/), which serves as a central data repository. It is used for staging, data transformation, modeling, and role-based data access.
3. **Predictions**: Custom Python and R scripts can be executed within Airflow tasks for building and training predictive models based on the data.
4. **Content Visualization and Reporting**: This is handled by [Apache Superset](./superset/README.md), an application for creating charts and dashboards, enabling data exploration through role-based access control.
5. **User Management**: This is handled by [Keycloak](./keycloak/README.md), a central instance for user administration, and role and access rights assignment.

## Component Interaction

1. **Data Retrieval**: Apache Airflow is scheduled to retrieve data from various sources. 
2. **Data Processing and Predictions**: Airflow processes the data (including executing predictive models) and stores the results in the PostgreSQL database.
3. **Data Visualization**: Apache Superset accesses the data in PostgreSQL and allows users to create visualizations, charts, and dashboards.
4. **User Management and Access Control**: Keycloak manages user accounts and permissions, ensuring that users have the appropriate access to Apache Superset.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Docker and Docker Compose installed on your machine.

### Component Documentation
For more detailed information about each component of the system, please refer to the README files in the respective directories:

* [Apache Superset](./superset/README.md)
* [Apache Airflow](./airflow/README.md)
* [Keycloak](./keycloak/README.md)

### Quick Start

1. Clone this repository:

   ```bash
   git clone https://github.com/cDataPusher/SelfServeModularPandemicManagement.git
    ```

2. Navigate to the repository directory:
    ```bash
    cd SelfServeModularPandemicManagement
    ```
3. Start the services:

Once the services are running, you can access the Superset web interface at http://localhost:8088 and Airflow at http://localhost:8080. The Keycloak admin console is available at http://localhost:8081/auth/admin/.


## Running the System

Follow these steps to get the system running:

1. **Start Apache Superset**: Navigate to the Superset directory and run the Docker Compose command to start the service. Refer to the [Superset Documentation](./superset/README.md) for detailed steps.

2. **Start Apache Airflow**: Navigate to the Airflow directory and use Docker Compose to start the Airflow services. Detailed steps can be found in the [Airflow Documentation](./airflow/README.md).

3. **Start Keycloak**: Run the Keycloak services using Docker Compose. Follow the instructions in the [Keycloak Documentation](./keycloak/README.md) to add users and set up roles and clients.

4. **Start the RKI-Airflow-DAG**: Access the Airflow web interface, login with the default credentials (`airflow:airflow`), and trigger the RKI-Airflow-DAG.

5. **Import the Dashboard into Superset**: After starting Superset, access the Superset web interface at http://localhost:8088. Log in with the default credentials (`superset:superset`). Navigate to the 'Dashboards' tab and use the 'Import Dashboard' option to import the `dashboard_export` file located in the Superset directory.

Please note that if it's your first time running these services, you might need to go through initial setup processes such as creating admin users or initializing databases.

Ensuring the proper interaction between networks is crucial for successfully initiating the Superset application, followed by Airflow, and finally executing the RKI example DAG.