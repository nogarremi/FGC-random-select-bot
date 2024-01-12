from json import loads as json_loads, load as json_load
from os import path as os_path

from boto3 import session as boto_session
from botocore import ClientError

def get_secret(key):
    session = boto_session.Session()
    client = session.client(service_name='secretsmanager', region_name="us-west-2")

    try:
        get_secret_value_response = client.get_secret_value(SecretId="Discord-FGC-RS-Bot")
    except ClientError as e:
        raise e

    return json_loads(get_secret_value_response['SecretString'])[key]

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

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

def get_randomselect_data(game, random_type='character'):
    rs_info = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = list(rs_info[random_type].copy().keys())

    if game not in games:
        return [], games
    return rs_info[random_type].get(game, []).copy()[0:-1], games

