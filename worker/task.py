import requests
from worker.executor import app
import config

@app.task(name='UrlTask', max_retries=2)
def run_url_task(data):
    """
        THIS IS THE PLACE WHERE THE TASK IS DEFINED
        WRITE A TASK HERE THAT TAKES TIME t TO COMPLETE
        JUST MAKE SURE THAT t < ♾ (infinite)
    """
    data = json.loads(data)
    url = data['url'].lower()
    method = data['method'].upper()
    try:
        response = requests.request(method, url)
    except:
        raise
    
    if response == 200:
        pass
    else:
        raise Exception("Probably needs a proxy or recheck the url. Thanks")

if __name__ == "__main__":
    run_test_job(json.dumps({'url': "https://api.ipyfy.org"}, 'GET'))