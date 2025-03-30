# T0phAt

A personal bot that runs on Discord.

## Building

1. Make sure to get Python 3.8 or higher
2. Set up a virtual environment: `python -m .venv venv`
3. Install dependencies: `pip install -U -r requirements.txt`
4. Run the bot with `python main.py`

## Setup configuration

The next step is just to create a .env file in the root directory where the bot is with the following template:

```.env
ICON="./public/tophat.jpg"
BOTNAME="T0phAt"
DEFAULTGUILDID="{GUILDLIDHERE}"
#WARNING, keep HIDDEN!~
BOTTOKEN="{BOTIDTOKEN}"
VERSION="v1.0.0"
TOPGGAPIKEY="{API_KEY_HERE}"
SHODAN_API_KEY="{API_KEY_HERE}"
LOGGING_LEVEL="DEBUG"
```
See the `.env.example` file for the template.

## Privacy Policy and Terms of Service

 No personal data is stored.
