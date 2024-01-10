from json import loads as json_loads, dumps as json_dumps
from os import path as os_path

# Local imports
from commands.sheets.sheets import sheets # Talk to Google Sheets API

_callbacks = {} # Yaksha

# Yaksha
def register(command):
    '''
    _Registers_ each function with by storing the command its name
    into a dict.
    '''
    def decorator(func):
        print('Registering %s with command %s' % (func.__name__, command))
        #print('Qual name: %s | Module: %s' % (func.__qualname__, func.__module__))
        _callbacks[command] = (func.__qualname__, func.__module__)
        return func
    return decorator

# Yaksha
def get_callbacks():
    '''
    Simple getter that returns the dictionary containing
    the registered functions. Might be better to make
    registration into a class instead.
    '''
    return _callbacks

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

def get_randomselect_data(game, random_type='character'):
    rs_info = json_loads(open(os_path.join(os_path.dirname(__file__), 'rs.json')).json())
    games = list(rs_info[random_type].copy().keys())

    if game not in games:
        return [], games
    return rs_info[random_type].get(game, []).copy()[0:-1], games
