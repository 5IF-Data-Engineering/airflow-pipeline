# Airflow image with Python 3.11
FROM apache/airflow:2.8.0b1-python3.11

# Install dependencies
USER root

# Install dependencies
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libyaml-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install OpenJDK-17
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
RUN export JAVA_HOME

## Switch back to airflow user
## https://airflow.apache.org/docs/docker-stack/build.html#adding-a-new-pypi-package
USER airflow

# Install Python packages
RUN pip install apache-airflow-providers-mongo==2.3.1 \
    apache-airflow-providers-apache-spark==4.4.0 \
    geocoder==1.38.1 \
    apache-airflow-providers-snowflake==5.1.2