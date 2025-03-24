"""
Core functionality for WhatsApp Daily Photo Bot.
"""

import logging
import os
import random
from io import BytesIO
from typing import Any, Dict, List, Optional, cast

import requests
from PIL import Image
from pywa import WhatsApp

# Configure logging
logger = logging.getLogger(__name__)

# Configuration constants
PHOTOS_URL = "https://raw.githubusercontent.com/dconnolly/chromecast-backgrounds/refs/heads/master/backgrounds.json"
TEMP_IMAGE_PATH = "temp_photo.jpg"


def fetch_photo_data() -> Optional[List[Dict[str, Any]]]:
    """Fetch the photo data from the GitHub repository"""
    try:
        response = requests.get(PHOTOS_URL)
        response.raise_for_status()
        return cast(List[Dict[str, Any]], response.json())
    except requests.RequestException as e:
        logger.error(f"Error fetching photo data: {e}")
        return None


def select_random_photo(photos_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Select a random photo from the data"""
    return random.choice(photos_data) if photos_data else None


def download_photo(photo_url: str) -> Optional[str]:
    """Download the photo from the URL"""
    try:
        response = requests.get(photo_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.save(TEMP_IMAGE_PATH)
        return TEMP_IMAGE_PATH
    except (requests.RequestException, IOError) as e:
        logger.error(f"Error downloading photo: {e}")
        return None


def init_whatsapp(api_token: str, phone_number_id: str) -> Optional[WhatsApp]:
    """Initialize WhatsApp client"""
    if not api_token or not phone_number_id:
        logger.error("Missing WhatsApp credentials")
        return None

    try:
        return WhatsApp(
            phone_id=phone_number_id,
            token=api_token,
        )
    except Exception as e:
        logger.error(f"Failed to initialize WhatsApp client: {e}")
        return None


def send_whatsapp_photo(
    photo_url: str,
    caption: str,
    receiver_number: str,
    api_token: str,
    phone_number_id: str,
) -> bool:
    """Send the photo to WhatsApp using pywa"""
    if not receiver_number:
        logger.error("Receiver number not configured")
        return False

    # Format phone number
    receiver = (
        receiver_number if receiver_number.startswith("+") else f"+{receiver_number}"
    )

    client = init_whatsapp(api_token, phone_number_id)
    if not client:
        return False

    logger.info(f"Sending image to {receiver} from {photo_url}")

    # Try sending from URL, then fallback to local download if needed
    try:
        response = client.send_image(
            image=photo_url,
            caption=caption,
            to=receiver,
        )
        logger.info(f"Photo sent successfully, message ID: {response.id}")
        return True
    except Exception as url_error:
        logger.warning(f"Failed to send from URL: {str(url_error)}")

        # Fallback to local image
        local_image_path = download_photo(photo_url)
        if not local_image_path:
            logger.error("Failed to download image locally")
            return False

        try:
            response = client.send_image(
                image=local_image_path,
                caption=caption,
                to=receiver,
            )
            logger.info(
                f"Photo sent successfully from local file, message ID: {response.id}"
            )
            return True
        except Exception as local_error:
            logger.error(f"Failed to send from local file: {str(local_error)}")
            return False


def cleanup() -> None:
    """Clean up any temporary files"""
    if os.path.exists(TEMP_IMAGE_PATH):
        try:
            os.remove(TEMP_IMAGE_PATH)
        except OSError as e:
            logger.error(f"Error removing temporary file: {e}")


def test_whatsapp_connection(
    api_token: str,
    phone_number_id: str,
    phone_number_to_send_to: str,
) -> bool:
    """Test the WhatsApp API connection and credentials"""
    logger.info("Testing WhatsApp API connection...")

    client = init_whatsapp(api_token, phone_number_id)
    if not client:
        return False

    try:
        profile = client.get_business_profile()
        logger.info("WhatsApp connection successful!")
        logger.info(f"Business profile details: {profile}")
        return True
    except Exception as e:
        logger.error(f"WhatsApp API connection test failed: {e}")
        return False


def send_daily_photo(
    receiver_number: str,
    api_token: str,
    phone_number_id: Optional[str] = None,
) -> bool:
    """Main function to send the daily photo"""
    logger.info("Starting daily photo send process")

    # Get phone number ID from environment if not provided
    phone_id = phone_number_id or os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    if not phone_id:
        logger.error("WhatsApp Phone Number ID not configured")
        return False

    # Fetch photo data
    photos_data = fetch_photo_data()
    if not photos_data:
        return False

    # Try sending photos until one succeeds or we run out of attempts
    max_attempts = min(5, len(photos_data))
    tried_photos = set()

    for attempt in range(max_attempts):
        # Select a random photo, avoiding already tried ones
        available_photos = [p for p in photos_data if id(p) not in tried_photos]
        if not available_photos:
            break

        photo = random.choice(available_photos)
        tried_photos.add(id(photo))

        photo_url = photo.get("url")
        if not photo_url:
            logger.warning(
                f"No URL found in photo data (attempt {attempt+1}/{max_attempts})"
            )
            continue

        author = photo.get("author", "Unknown")
        caption = f"Today's beautiful photo by: {author}"

        logger.info(f"Selected photo by {author} (attempt {attempt+1}/{max_attempts})")

        if send_whatsapp_photo(
            photo_url, caption, receiver_number, api_token, phone_id
        ):
            logger.info("Daily photo process completed successfully")
            return True

    logger.error(f"Failed to send any photo after {max_attempts} attempts")
    return False
