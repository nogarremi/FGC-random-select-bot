from command_list import commands
from requests import put

from utils import get_secrets

def main():
    secrets = get_secrets(['fgc-rs-bot-app-id', 'fgc-rs-bot-server-id', 'fgc-rs-bot-token'])
    APP_ID = secrets['fgc-rs-bot-app-id']
    SERVER_ID = secrets['fgc-rs-bot-server-id']
    BOT_TOKEN = secrets['fgc-rs-bot-token']

    BASE_URL = f'https://discord.com/api/v10/applications/{APP_ID}/commands'

    for command, command_info in commands.items():
        res = put(url, headers={'Authorization': f'Bot {BOT_TOKEN}'}, json=command_info)
        print(res.json())

if __name__ == "__main__":
    main()

