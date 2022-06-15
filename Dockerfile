FROM apache/airflow:2.2.4
USER root
RUN sudo apt-get -y update
RUN sudo apt-get -y install git
USER airflow
COPY requirements.txt .
RUN pip install -r requirements.txt