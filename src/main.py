from json import loads as json_loads, dumps as json_dumps, load as json_load
from os import path as os_path

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from utils import get_secret

rs_info = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))

valid_char_games = [{"name": game_info['name'], "value":game_id} for game_id, game_info in rs_info.items() if "characters" in game_info]
valid_stage_games = [{"name": game_info['name'], "value":game_id} for game_id, game_info in rs_info.items() if "stages" in game_info]

commands = {
    "fgc-rs-github": {
        "name": "fgc-rs-github",
        "description": "Show FGC-RS-Bot's GitHub page",
        "type": 1,
        "options": []
    },
    "fgc-rs-ping": {
        "name": "fgc-rs-ping",
        "description": "Check if bot is online",
        "type": 1,
        "options": []
    },
    "randomselect": {
        "name": "randomselect",
        "description": "Return a randomly selected character/stage",
        "type": 1,
        "dm_permission": False,
        "options": [
            {
                "type": 1,
                "name": "characters",
                "description": "Get a random character",
                "choices": valid_char_games
            },
            {
                "type": 1,
                "name": "stages",
                "description": "Get a random stage",
                "choices": valid_stage_games
            }
        ]
    }
}

def lambda_handler(event, context):
    print(event)
    print(commands)
    try:
        e_body = event['body']
        body = json_loads(e_body)

        signature = bytes.fromhex(event['headers']['x-signature-ed25519'])
        timestamp = event['headers']['x-signature-timestamp']

        # Validate interaction
        invalid_request = validate(timestamp, signature, e_body)
        if invalid_request:
            return invalid_request

        t = body['type']

        # Check type
        return type_check(t, body)
    except Exception as e:
        print(e)
        return return_format(500, 'Server Error')

def return_format(status_code, body):
    return {
        'statusCode': status_code,
        'body': json_dumps(body)
    }

def validate(timestamp, signature, e_body):
    verify_key = VerifyKey(bytes.fromhex(get_secret('fgc-rs-bot-pub-key')))
    message = f"{timestamp}{e_body}".encode()

    try:
        verify_key.verify(message, signature=signature)
    except BadSignatureError:
        return return_format(401, 'Unauthorized')
    return False

def type_check(t, body):
    if t == 1:
        return return_format(200, {'type':1})
    elif t == 2:
        return command_handler(body)
    return return_format(400, 'Bad Request')

def command_handler(body):
    command = body['data']['name']

    if command not in commmands:
        return return_format(400, 'Bad Request')
    elif command == "fgc-rs-github":
        return return_format(200, "For more information about FGC-RS-Bot and its commands: <https://github.com/nogarremi/fgc-random-select-bot>")
    elif command == "fgc-rs-ping":
        return return_format(200, "FGC-RS Pong!")
    elif command == "randomselect" or "rs":
        return return_format(200, {'type':1, 'data':{'content':body}})

