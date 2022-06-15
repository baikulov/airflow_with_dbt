# airflow_with_dbt

## Устанавливаем Docker и docker-compose

1. Обновляем пакеты Linux
```bash
sudo apt-get update
```

2. Затем ставим вспомогательные пакеты для установки Docker
```bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

3. Следующим шагом добавляем ключ GPG Docker'а
```bash
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4. Ещё одним шагом в подготовке будет добавление ссылки на стабильную версию репозитория Docker
```bash 
 echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. После этого мы обновим все пакеты и установим Docker
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
Теперь у нас установлен Docker и мы можем скачивать различные образы из частных или центрального репозитория Docker Hub

6. Для установки Docker Compose необходимо добавить запись. Свежую версию всегда можно взять на официальном сайте https://docs.docker.com/compose/install/.
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

7. И последним шагом необходимо применить права к бинарному файлу
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

## Клонируем текущий репозиторий
```bash
git clone https://github.com/baikulov/airflow_with_dbt.git
```
## Указываем учётные данные для подключения в файле .env
```bash
AIRFLOW_UID=1000
DBT_SCHEMA_DEV=<clickhouse_dev>
DBT_SCHEMA_PROD=<clickhouse_prod>
DBT_HOST=<clickhouse_host>
DBT_PORT=<clickhouse_port>
DBT_USER=<clickhouse_user>
DBT_PASSWORD=<clickhouse_password>
DBT_PROFILES_DIR=.
TELEGRAM_TOKEN=<telegram_bot_token>
TELEGRAM_CHAT_ID=<telegram_chat_id>
```
## Клонируем свой проект dbt в папку dags/scripts/dbt
```bash
cd dags/scripts/
git clone https://github.com/baikulov/dbt.git
```
## Запускаем airflow
```bash
 docker-compose up -d
 ```