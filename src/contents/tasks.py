import requests
from contentapi.celery import app

@app.task(queue="content_pull")
def pull_and_store_content():
    # TODO: The design of this celery task is very weird. It's posting the response to localhost:3000.
    #  which is not ideal
    url = "https://example.com/api/pull_data"
    api_url = "http://localhost:3000/contents/"
    res = requests.get(url).json()
    for item in res:
        payload = {**item}
        requests.post(api_url, json=payload)