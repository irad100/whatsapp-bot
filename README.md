# WhatsApp Daily Photo Bot

A Python bot that sends a daily photo with author attribution from the Chromecast backgrounds collection to a WhatsApp contact using the WhatsApp Business API via [pywa](https://pywa.readthedocs.io/).

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/photos-bot.git
cd photos-bot

# Install the package
pip install -e .
```

### Using pip (once published)

```bash
pip install photos-bot
```

## GitHub Actions Integration

This project includes GitHub Actions workflows for automated scheduling and testing:

### Scheduled Photo Sending

The bot automatically runs daily at 8:00 AM UTC using GitHub Actions. To use this feature:

1. Fork this repository to your own GitHub account
2. Add the following secrets to your repository:
   - `WHATSAPP_API_TOKEN`: Your WhatsApp API token
   - `WHATSAPP_PHONE_NUMBER_ID`: Your WhatsApp Business Phone Number ID
   - `RECEIVER_NUMBER`: The WhatsApp number to send photos to (with country code)

You can also manually trigger the workflow from the Actions tab in your GitHub repository.

### Testing

The repository includes a test workflow that verifies your WhatsApp connection is working properly. It runs automatically on pushes to the main branch and pull requests, or can be triggered manually.

## Setup

1. Create a `.env` file with your configuration:

   ```env
   # WhatsApp receiver phone number (with country code)
   RECEIVER_NUMBER="+1234567890"

   # Time to send the daily photo (24-hour format)
   SEND_TIME="08:00"

   # WhatsApp Business API settings
   WHATSAPP_API_TOKEN="<TOKEN>"
   WHATSAPP_PHONE_NUMBER_ID="<PHONE_NUMBER_ID>"
   ```

## Usage

### Command Line

```bash
# Run the bot normally (scheduled mode)
photos-bot

# Test by sending a photo immediately
photos-bot --test

# Specify all parameters manually
photos-bot --time "18:30" --number "+1234567890" --token "<TOKEN>" --phone-id "<PHONE_NUMBER_ID>"
```

### As a Python Package

```python
from photos_bot.core import send_daily_photo

# Send a photo immediately (basic usage)
send_daily_photo("+1234567890", "<TOKEN>", "<PHONE_NUMBER_ID>")

# With named parameters
send_daily_photo(
    receiver_number="+1234567890",
    api_token="<TOKEN>",
    phone_number_id="<PHONE_NUMBER_ID>"
)
```

## WhatsApp Business API

This bot uses [pywa](https://pywa.readthedocs.io/) - a modern Python wrapper for the WhatsApp Cloud API. To get your own API credentials:

1. Create a [Meta for Developers](https://developers.facebook.com/) account
2. Set up a Meta App with WhatsApp integration
3. Configure a WhatsApp Business phone number
4. Get your Phone Number ID from the WhatsApp dashboard
5. Generate an API token from the Meta App Dashboard

The WhatsApp Business API requires:

- A permanent access token
- Your WhatsApp Phone Number ID (different from your actual phone number)

For more details, see:

- [pywa documentation](https://pywa.readthedocs.io/en/latest/)
- [WhatsApp Cloud API documentation](https://developers.facebook.com/docs/whatsapp/cloud-api)

## Features

- Fetches beautiful photos from Chromecast backgrounds collection
- Sends daily photos with author attribution via WhatsApp Business API
- Uses pywa library for simplified WhatsApp integration
- Configurable send time
- Retry mechanism if photo fails to send
- Logs activity

## Requirements

- Python 3.10+
- Internet connection
- WhatsApp Business API credentials

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format photos_bot

# Lint code
ruff check photos_bot
```
