import json
from pathlib import Path
from time import sleep

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class HomeAssistantAPIException(Exception):
    pass


class HomeAssistantAPI:
    def __init__(self, url, bearer_token, language):
        self.session = Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}",
            }
        )
        self.base_url = url

        retries = Retry(backoff_factor=0.2, total=7)
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        # Setup the language stuff, the HA API returns state in English, so we need to translate it on our end
        # to make life a bit easier
        self.language = language
        api_translation_file = Path(__file__).parent / f"./api_translations/{language}.json"
        if language != "en":
            if api_translation_file.is_file():
                self.translation = json.load(api_translation_file.open())
            else:
                raise HomeAssistantAPIException(
                    f"API Translation file for language '{language}' doesn't exist. "
                    f"You will need to create one in components/home_assistant/api_translations/{language}.json"
                )

        # Make a test call to see if everything works
        try:
            self.get("/api/")
        except requests.exceptions.ConnectionError:
            raise HomeAssistantAPIException(
                f"Unable to connect to Home Assistant server at {url} - "
                "Ensure the URL is correct, Home Assistant is running and try again!"
            )
        except requests.HTTPError as error:
            if error.response.status_code == 401:
                raise HomeAssistantAPIException(
                    "401 Unauthorized. Ensure your Home Assistant bearer token is correct"
                )
            else:
                raise

    def get(self, url):
        response = self.session.get(f"{self.base_url}{url}", timeout=5)
        response.raise_for_status()
        return response.json()

    def get_entity(self, entity, service_response=None):
        entity = self._get_entity(entity, service_response)

        if self.language != "en":
            if "state" in entity:
                entity["state"] = self.translation[entity["state"]]

        return entity

    def _get_entity(self, entity, service_response=None):
        if isinstance(service_response, list):
            # call_service in HA returns a list of entities.
            # There's a bug where sometimes it returns an empty list
            # you have to wait ~1s to actually get the new state
            if service_response:
                try:
                    return _extract_from_list(service_response, entity)
                except EntityIdNotFoundInList:
                    pass
            sleep(1)
        return self.get(f"/api/states/{entity}")

    def post(self, url, body):
        response = self.session.post(f"{self.base_url}{url}", json=body)
        response.raise_for_status()
        return response.json()

    def call_service(self, domain, service, body):
        return self.post(f"/api/services/{domain}/{service}", body)


class EntityIdNotFoundInList(LookupError):
    pass


def _extract_from_list(service_response, entity_id):
    for entity in service_response:
        if entity["entity_id"] == entity_id:
            return entity

    raise EntityIdNotFoundInList()
