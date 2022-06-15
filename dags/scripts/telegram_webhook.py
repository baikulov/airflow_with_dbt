def telegramm_alert(context):
    import requests
    token = "953719854:AAF8yberWRp-tMH5BWrFk1NilnJeI9vJpZg"  # токен бота в телеге
    chat_id = "-537128908"  # номер чата с ботом, можно получить внутри телеги
    error_context = context["task_instance"]
    url = "https://api.telegram.org/bot{}/sendMessage"

    json = {
        "chat_id": chat_id,
        "text": "Task = " +
        str(error_context.task_id) +
        " failed in DAG = " + str(error_context.dag_id)
    }

    get = requests.post(url.format(token), json=json)
    print(get.status_code)
