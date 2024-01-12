from json import loads as json_loads, load as json_load
from os import path as os_path

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

def rs_autocomplete(random_type):
    rs_data = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = [{"name": game_data["name"], "value": rs_game} for rs_game, game_data in rs_data.items() if random_type in game_data]
    
    return games

def rs_data_getter(random_type, game):
    rs_data = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = [rs_game for rs_game, game_data in rs_data.items() if random_type in game_data]

    if game not in games:
        return []
    return rs_data[game].get(random_type, []).copy()

