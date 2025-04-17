"""
Command Line Interface for WhatsApp Daily Photo Bot.
"""

import argparse
import logging
import os

from dotenv import load_dotenv

from .core import send_daily_photo

logger = logging.getLogger(__name__)


def setup_args():
    """Set up command line arguments."""
    parser = argparse.ArgumentParser(description="WhatsApp Daily Photo Bot")
    parser.add_argument(
        "--number",
        type=str,
        help="WhatsApp receiver number (with country code)",
        default=os.getenv("RECEIVER_NUMBER"),
    )
    parser.add_argument(
        "--token",
        type=str,
        help="WhatsApp API token",
        default=os.getenv("WHATSAPP_API_TOKEN"),
    )
    parser.add_argument(
        "--phone-id",
        type=str,
        help="WhatsApp Business Phone Number ID",
        default=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    )
    return parser.parse_args()


def main():
    """Main entry point for the CLI"""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    args = setup_args()

    return send_daily_photo(args.number, args.token, args.phone_id)


if __name__ == "__main__":
    main()
