import os
from dotenv import load_dotenv

load_dotenv()

POSTMAN_API_KEY = os.getenv("POSTMAN_API_KEY")
POSTMAN_VAULT_KEY = os.getenv("POSTMAN_VAULT_KEY")
POSTMAN_API_BASE_URL = "https://api.getpostman.com"

if not POSTMAN_API_KEY:
    raise ValueError("POSTMAN_API_KEY environment variable is required. Please create a .env file with your Postman API key.")