from json import load as json_load
from os import path as os_path

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

if __name__ == "__main__":
    print(commands)
