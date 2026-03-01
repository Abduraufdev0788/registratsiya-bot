import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")
BASE_SITE_URL = os.getenv("BASE_SITE_URL")
BASE_URL_LOGIN = os.getenv("BASE_URL_LOGIN")
BASE_URL_REFRESH = os.getenv("BASE_URL_REFRESH")