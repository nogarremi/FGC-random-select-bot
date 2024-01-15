from command_list import commands
from requests import put

from boto3 import session as boto_session
from botocore import ClientError

def get_secrets(keys):
    session = boto_session.Session()
    client = session.client(service_name='secretsmanager', region_name="us-west-2")

    try:
        get_secret_value_response = client.get_secret_value(SecretId="Discord-FGC-RS-Bot")
    except ClientError as e:
        raise e

    secretstring = json_loads(get_secret_value_response['SecretString'])

    secrets = {}
    for key in keys:
        secrets[key] = secretstring[key]

    return secrets

def reg_commands():
    secrets = get_secrets(['fgc-rs-bot-app-id', 'fgc-rs-bot-server-id', 'fgc-rs-bot-token'])
    APP_ID = secrets['fgc-rs-bot-app-id']
    SERVER_ID = secrets['fgc-rs-bot-server-id']
    BOT_TOKEN = secrets['fgc-rs-bot-token']

    BASE_URL = f'https://discord.com/api/v10/applications/{APP_ID}/commands'

    for command, command_info in commands.items():
        res = put(url, headers={'Authorization': f'Bot {BOT_TOKEN}'}, json=command_info)
        print(res.json())

if __name__ == "__main__":
    reg_commands()

