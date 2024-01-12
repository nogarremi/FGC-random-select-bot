from json import load as json_load
from os import path as os_path

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

def get_randomselect_data(game, random_type='character'):
    rs_info = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = list(rs_info[random_type].copy().keys())

    if game not in games:
        return [], games
    return rs_info[random_type].get(game, []).copy()[0:-1], games

