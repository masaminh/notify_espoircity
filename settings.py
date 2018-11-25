"""設定情報."""
import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

NOTIFY_ACCESS_TOKEN = os.environ.get("NOTIFY_ACCESS_TOKEN")
