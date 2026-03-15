import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")
API_ADMIN_EMAIL = os.environ.get("API_ADMIN_EMAIL")
API_ADMIN_PASSWORD = os.environ.get("API_ADMIN_PASSWORD")
REPORT_HOUR = int(os.environ.get("REPORT_HOUR", 0))
REPORT_MINUTE = int(os.environ.get("REPORT_MINUTE", 0))