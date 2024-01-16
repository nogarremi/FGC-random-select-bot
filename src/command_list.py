from json import load as json_load
from os import path as os_path

rs_info = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))

valid_char_games = [{"name": game_info['name'], "value":game_id} for game_id, game_info in rs_info.items() if "characters" in game_info]
valid_stage_games = [{"name": game_info['name'], "value":game_id} for game_id, game_info in rs_info.items() if "stages" in game_info]

commands = {
    "github": {
        "name": "github",
        "description": "Show FGC-RS-Bot's GitHub page",
        "type": 1,
        "options": []
    },
    "ping": {
        "name": "ping",
        "description": "Check if the FGC-RS-Bot is online",
        "type": 1,
        "options": []
    },
    "random-select": {
        "name": "random-select",
        "description": "Return a randomly selected character/stage",
        "type": 1,
        "dm_permission": False,
        "options": [
            {
                "type": 1,
                "name": "characters",
                "description": "Get a random character",
                "options": [{
                    "name": "game",
                    "type": 3,
                    "description": "Choose a supported game",
                    "autocomplete": True,
                    "required": True
                }]
            },
            {
                "type": 1,
                "name": "stages",
                "description": "Get a random stage",
                "options": [{
                    "name": "game",
                    "description": "Choose a supported game",
                    "type": 3,
                    "autocomplete": True,
                    "required": True
                }]
            }
        ]
    },
    "random-select-testing":{"name":"random-select-testing"}
}

if __name__ == "__main__":
    print(commands)

