import requests

class HttpFetcher:
    def __init__(self):
        self.headers = {"User-Agent":"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 DNT=1"}


    def GET(self, url):
        response = requests.get(url, headers=self.headers)
        return response


