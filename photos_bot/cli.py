"""
Command Line Interface for WhatsApp Daily Photo Bot.
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from photos_bot.core import send_daily_photo, test_whatsapp_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("photo_bot.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def setup_args():
    """Set up command line arguments."""
    parser = argparse.ArgumentParser(description="WhatsApp Daily Photo Bot")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Send a photo once (for GitHub Actions or manual sending)",
    )
    parser.add_argument(
        "--test", action="store_true", help="Run once for testing purposes"
    )
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test the WhatsApp API connection without sending a photo",
    )
    parser.add_argument(
        "--number", type=str, help="WhatsApp receiver number (with country code)"
    )
    parser.add_argument("--token", type=str, help="WhatsApp API token")
    parser.add_argument(
        "--phone-id", type=str, help="WhatsApp Business Phone Number ID"
    )
    return parser.parse_args()


def get_required_config(args, env_var, param_name, required=True):
    """Get a required configuration value from args or environment"""
    value = getattr(args, param_name) or os.getenv(env_var)
    if required and not value:
        logger.error(f"{env_var} not configured.")
        sys.exit(1)
    return value


def main():
    """Main entry point for the CLI"""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    args = setup_args()

    # Get configuration
    api_token = get_required_config(args, "WHATSAPP_API_TOKEN", "token")
    phone_number_id = get_required_config(args, "WHATSAPP_PHONE_NUMBER_ID", "phone_id")

    # If testing connection only
    if args.test_connection:
        receiver = get_required_config(
            args, "RECEIVER_NUMBER", "number", required=False
        )
        success = test_whatsapp_connection(api_token, phone_number_id, receiver)
        sys.exit(0 if success else 1)

    # For direct sending modes, we need the receiver number
    receiver_number = get_required_config(
        args, "RECEIVER_NUMBER", "number", required=(args.send or args.test)
    )

    # Process commands
    if args.send or args.test:
        logger.info(
            f"Running in {'send' if args.send else 'test'} mode - sending photo once"
        )
        success = send_daily_photo(receiver_number, api_token, phone_number_id)
        sys.exit(0 if success else 1)

    # If no specific action requested, show help
    logger.info("No action specified.")
    sys.exit(1)


if __name__ == "__main__":
    main()
