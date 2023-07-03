# RKI Infection Data DAG

This document describes an Apache Airflow Directed Acyclic Graph (DAG) that fetches infection data from the Robert Koch Institute (RKI) website and writes it into a PostgreSQL database.

## DAG Overview

The DAG is named `rki_infection_data` and runs on a daily schedule. It consists of two tasks:

1. `fetch_data`: This task fetches the infection data from the RKI website. The data is fetched as an HTML table and converted into a pandas DataFrame.

2. `write_data`: This task writes the DataFrame into the 'rki_infection_data' table in the PostgreSQL database. If the table already exists, it is replaced.

## Setup

To use this DAG, you need to have Apache Airflow and pandas installed, and you need to have a PostgreSQL database available. The database connection is configured in the `write_data` task.

## Usage

To use this DAG, you need to place it in your Airflow DAGs folder. Once Airflow picks up the DAG, it will start running it on the specified schedule.

## Customization

You can customize this DAG to fit your needs. For example, you could modify the `fetch_data` task to fetch different data, or you could modify the `write_data` task to write the data to a different database or table.
