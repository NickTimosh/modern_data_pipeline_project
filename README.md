# Modern Data Pipeline with Apache Airflow, Docker, Data Quality Testing, and CI/CD automation

## Overview

I’ve started building a personal data platform that collects and processes data from my YouTube channel, LinkedIn, GitHub, and other platforms to better understand engagement, growth, and audience behavior across channels. It’s also a great opportunity to apply modern data engineering tools and practices such as Apache Airflow, Docker, API integrations, functional and data quality testing, and CI/CD automation.

## Summary
This ELT (or I`d rather say EtLT) pipeline is orchestrated with Airflow, containerized with Docker, and stores data in PostgreSQL. The process includes:
* Retrieve video metadata via the YouTube API.
* Store the raw data in a staging schema inside a dockerized PostgreSQL instance.
* Transform & Load to reporting tables
* Ensure data quality applying unit tests and data quality checks.
* Run tests and build Docker images using GitHub Actions CI/CD workflows.
<img width="773" height="664" alt="image" src="https://github.com/user-attachments/assets/8884df62-bb68-466d-bf4d-8e2ff72ebf7d" />

## DAGs
Three Airflow DAGs are defined and triggered sequentially:
* produce_json — Extracts YouTube data and saves it as a JSON file.
* update_db — Loads and processes the data into staging and core schemas.
* data_quality — Runs Soda checks to validate data quality.

## CI/CD & Testing
* Unit and integration tests ensure pipelines behave as expected.
* Data quality is monitored automatically with Soda.
* A GitHub Actions workflow builds and pushes Docker images, starts Airflow services, and tests DAG execution.

## Useful links for everyone who is interested in grasping these tools:

## Youtube API
* [Google Dev Console](https://console.cloud.google.com/cloud-resource-manager)
* [API Docs](https://developers.google.com/youtube/v3/docs)
* [Quotas & Limits](https://developers.google.com/youtube/v3/determine_quota_cost)
* [Postman API Platform](https://www.postman.com/)

## Docker
* [Install Docker](https://docs.docker.com/engine/install/)
* [Docker Airflow Image](https://hub.docker.com/r/apache/airflow)
* [Docker hub](https://hub.docker.com/repositories/timoshtop)
* [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

## Airflow

* [Storing Airflow Variables in Environment Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html)
* [Timezone](https://timezonedb.com/time-zones)
* [Declaring an Airflow DAG](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#declaring-a-dag)
* [Crontab](https://crontab.guru/)
* [Airflow start_date](https://airflow.apache.org/docs/apache-airflow/stable/faq.html#what-s-the-deal-with-start-date)

## Tests

* [Soda Postgres Configuration](https://docs.soda.io/data-source-reference/connect-postgres)
* [SodaCL Checks](https://docs.soda.io/soda-cl-overview)
* [Conftest script](https://docs.pytest.org/en/stable/reference/fixtures.html)

## Github Actions

* [Github Actions QuickStart](https://docs.github.com/en/actions/get-started/quickstart)
* [Checkout Action](https://github.com/actions/checkout)
* [Changed File Action](https://github.com/tj-actions/changed-files)
* [Setup Buildx Action](https://github.com/docker/setup-buildx-action)

This project is inspired by [the Data Engineering ELT Pipeline course](https://www.udemy.com/course/start-your-data-engineering-journey-project-based-learning/#instructor-1) by @MattTheDataEngineer — a great resource for mastering Airflow + Docker development. 100% recommend!!!
