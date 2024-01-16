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
    }
}

if __name__ == "__main__":
    print(commands)

