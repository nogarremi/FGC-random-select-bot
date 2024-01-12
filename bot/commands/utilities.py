from json import load as json_load
from os import path as os_path

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
    rs_info = json_load(open(os_path.join(os_path.dirname(__file__), 'rs.json')))
    games = list(rs_info[random_type].copy().keys())

    if game not in games:
        return [], games
    return rs_info[random_type].get(game, []).copy()[0:-1], games

if __name__ == '__main__':
    get_randomselect_data('sfv')
