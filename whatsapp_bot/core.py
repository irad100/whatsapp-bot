"""
Core functionality for WhatsApp Daily Photo Bot.
"""

import logging
import random

import requests
from pywa import WhatsApp

# Configure logging
logger = logging.getLogger(__name__)

# Configuration constants
PHOTOS_URL = "https://raw.githubusercontent.com/dconnolly/chromecast-backgrounds/refs/heads/master/backgrounds.json"


def send_daily_photo(
    receiver_number: str,
    api_token: str,
    phone_number_id: str,
) -> bool:
    """Main function to send the daily photo"""
    logger.info("Starting daily photo send process")

    # Fetch photo data
    response = requests.get(PHOTOS_URL)
    if response.status_code != 200:
        logger.error(f"Failed to fetch photo data: {response.status_code}")
        return False

    photos_data = response.json()
    photo = random.choice(photos_data)
    caption = f"*התמונה היומית:*\nיוצר: {photo.get('author')}"
    client = WhatsApp(phone_number_id, api_token)
    response = client.send_image(
        image=photo.get("url"),
        caption=caption,
        to=receiver_number,
    )

    return response.id is not None
