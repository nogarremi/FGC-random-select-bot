from json import loads as json_loads, load as json_load
from os import path as os_path
from thefuzz import process as fuzz_process, fuzz as fuzz_fuzz

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

def rs_autocomplete(random_type, user_value):
    rs_data = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = [{"name": game_data["name"], "value": rs_game, "stripped": f"{rs_game.lower()} {game_data["name"]}"} for rs_game, game_data in rs_data.items() if random_type in game_data]
    games_stripped = [game['stripped'].lower() for game in games]

    extract_list = fuzz_process.extractBests(user_value.lower(), games_stripped, scorer=fuzz_fuzz.partial_ratio, score_cutoff=70)

    game_list = []
    for item in extract_list:
        item_value = item.split(' ')[0]
        for game in games:
            if game['value'].lower() == item_value:
                game_list.append(game)

    return game_list

def rs_data_getter(random_type, game):
    rs_data = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = [rs_game for rs_game, game_data in rs_data.items() if random_type in game_data]

    if game not in games:
        return []
    return rs_data[game].get(random_type, []).copy()

