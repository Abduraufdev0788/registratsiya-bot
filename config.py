import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")
BASE_URL_REFRESH = os.getenv("BASE_URL_REFRESH")
IMG_URL = os.getenv("IMG_URL")