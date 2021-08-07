import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class HomeAssistantAPI:
    def __init__(self, url, bearer_token):
        self.session = Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Authorization": f"Bearer {bearer_token}",}
        )
        self.base_url = url

        retries = Retry(backoff_factor=1)
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            self.get("/api/")
        except requests.exceptions.ConnectionError as error:
            raise Exception(
                f"Unable to connect to rhasspy server at {url} - "
                "Ensure it is running and try again!"
            )
        # TODO: add session auto retry logic from urllib3

    def get(self, url):
        response = self.session.get(f"{self.base_url}{url}")
        response.raise_for_status()
        return response.json()

    def get_entity(self, entity):
        return self.get(f"/api/states/{entity}")

    def post(self, url, body):
        response = self.session.post(f"{self.base_url}{url}", json=body)
        response.raise_for_status()
        return response.json()

    def call_service(self, domain, service, body):
        return self.post(f"/api/services/{domain}/{service}", body)
