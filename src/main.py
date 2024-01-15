from json import loads as json_loads, dumps as json_dumps
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

# Local Imports
from command_list import commands

PUBLIC_KEY = '9679ddc48e1a1c27b33c0b41fef42191eeca92a3b48d5f52ed601d55e906e235'

def lambda_handler(event, context):
    print(event)
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

    if command not in commands:
        return return_format(400, 'Bad Request')
    elif command == "fgc-rs-github":
        return return_format(200, {'type':4, 'data':{'content':"For more information about FGC-RS-Bot and its commands: <https://github.com/nogarremi/fgc-random-select-bot>"}})
    elif command == "fgc-rs-ping":
        return return_format(200, {'type':4, 'data':{'content':"FGC-RS Pong!"}})
    elif command == "randomselect" or "rs":
        return return_format(200, {'type':4, 'data':{'content':body}})

