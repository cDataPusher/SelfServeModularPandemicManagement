# Supporting regional pandemic management by enabling self-service reporting through modularisation

This repository contains the code and configurations for the paper "Supporting regional pandemic management by enabling self-service reporting through modularisation". The system is built using open-source technologies and follows a dataflow-driven approach.

## Overview

The system is designed to cater to three main user groups:

1. **Data Suppliers**: These include clinics, health offices, National Institute of Health and Veterinary Inspection, and publicly available data sources.
2. **Data Processors**: These include local research facilities such as the Center for Evidence-Based Health Care and the Center for Medical Informatics of the TU-Dresden.
3. **Data Users**: These include clinical control centers for patient disposition, clinical management, and legal governmental and non-governmental entities.

The functionalities of the system are divided into different service groups, each handled by a specific application:

1. **Data Processing**: Handled by Apache Airflow, an orchestration tool that provides many interfaces and processing functionalities.
2. **Data Storage**: Handled by PostgreSQL Database, a relational database for staging, data transformation, modeling, and role-based data access.
3. **Predictions**: Handled by custom Python and R scripts for building and training predictive models.
4. **Content Visualization and Reporting**: Handled by Apache Superset, an application for creating charts and dashboards, enabling data exploration through role-based access control.
5. **User Management**: Handled by Keycloak, a central instance of user administration and role and access rights assignment.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Docker and Docker Compose installed on your machine.

### Component Documentation
For more detailed information about each component of the system, please refer to the README files in the respective directories:

* [Apache Airflow](./airflow/README.md)
* [Apache Superset](./superset/README.md)
* [Keycloak](./keycloak/README.md)

