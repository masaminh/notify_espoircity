"""設定情報."""
import os
from os.path import dirname, join

from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

NOTIFY_ACCESS_TOKEN = os.environ.get("NOTIFY_ACCESS_TOKEN")
