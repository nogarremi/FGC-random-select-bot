# Py Default Imports
from json import loads as json_loads, dumps as json_dumps
from random import choice as random_choice

# External Imports
from requests import post
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

# Local Imports
from command_list import commands
from utils import bold, rs_autocomplete, rs_data_getter

PUBLIC_KEY = '9679ddc48e1a1c27b33c0b41fef42191eeca92a3b48d5f52ed601d55e906e235'

def lambda_handler(event, context):
    print(event)
    try:
        e_body = event['body']
        body = json_loads(e_body)

        timestamp = event['headers']['x-signature-timestamp']
        
        if timestamp != "test-imerragon-2024":
            # Validate interaction
            signature = bytes.fromhex(event['headers']['x-signature-ed25519'])
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
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
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
    interaction_id = body['id']
    interaction_token = body['token']

    if command not in commands:
        return return_format(400, 'Bad Request')
    
    URL = f'https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback'
    if command == "github":
        data = {'type':4, 'data':{'content':"For more information about FGC-RS-Bot and its commands: <https://github.com/nogarremi/fgc-random-select-bot>"}}
    elif command == "ping":
        data = {'type':4, 'data':{'content':"FGC-RS Pong!"}}
    elif command == "random-select":
        chars_or_stages = body['data']['options'][0]['name']
        
        game_option_data = body['data']['options'][0]['options'][0]
        
        if 'focused' in game_option_data and game_option_data['focused']:
            rs_autocomplete_data = rs_autocomplete(chars_or_stages)
            print(rs_autocomplete)
            data = {'type':8, 'data':{'choices':rs_autocomplete_data}}
        else:
            game = game_option_data['value']
            data = {'type':4, 'data':{'content':f'Your randomly selected {chars_or_stages[:-1]} for {bold(game.upper())} is: {bold(random_choice(rs_data_getter(chars_or_stages, game)))}'}}
    else:
        return return_format(400, 'Bad Request')

    resp = post(URL, json=data)
    r_format = return_format(200, data)
    print(r_format)
    return r_format

