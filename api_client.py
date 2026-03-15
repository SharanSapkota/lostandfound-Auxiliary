import requests
import logging
from config import API_BASE_URL, API_ADMIN_EMAIL, API_ADMIN_PASSWORD

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None

    def login(self):
        response = requests.post(f"{self.base_url}/users/login", json={
            "email": API_ADMIN_EMAIL,
            "password": API_ADMIN_PASSWORD,
        })
        response.raise_for_status()
        self.token = response.json()["access_token"]
        logger.info("API client authenticated successfully.")

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def get_all_items(self) -> list:
        response = requests.get(f"{self.base_url}/items/", headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_all_claims_for_item(self, item_id: int) -> list:
        response = requests.get(f"{self.base_url}/items/{item_id}/claims", headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_all_pickups(self) -> list:
        response = requests.get(f"{self.base_url}/pickups/", headers=self._headers())
        response.raise_for_status()
        return response.json()