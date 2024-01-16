from command_list import commands
from requests import put
from secret import token

def reg_commands(testing=False):
    APP_ID = 1195150675139637248
    #SERVER_ID = '745298426979418204'
    SERVER_ID = '361659611444543490' 

    BASE_URL = f'https://discord.com/api/v10/applications/{APP_ID}/commands'

    if testing:
        BASE_URL = f'https://discord.com/api/v10/applications/{APP_ID}/guilds/{SERVER_ID}/commands'

    commands_to_reg = [command_info for command, command_info in commands.items()]

    res = put(BASE_URL, headers={'Authorization': f'Bot {token}'}, json=commands_to_reg)
    print(res.json())

if __name__ == "__main__":
    reg_commands(True)

