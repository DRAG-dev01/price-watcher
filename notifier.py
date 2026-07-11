import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_message(message):
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Discord webhook URL is missing!")

    data = {"content": message}

    response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)

    if response.status_code != 204:
        raise Exception(f"Discord error: {response.status_code} - {response.text}")
