import requests
from typing import Dict, Any, Optional
from config import POSTMAN_API_KEY, POSTMAN_API_BASE_URL


class PostmanClient:
    def __init__(self):
        self.api_key = POSTMAN_API_KEY
        self.base_url = POSTMAN_API_BASE_URL
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_collection(self, collection_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/collections/{collection_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_environment(self, environment_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/environments/{environment_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None