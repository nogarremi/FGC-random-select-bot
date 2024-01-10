from random import choice as random_choice # For randomizing arrays

# Local imports
from commands.utilities import (register, bold, get_randomselect_data) # Bring in some utilities to help the process

# All @register decorators are a product of reviewing Yaksha
# See utilities.register for more information

@register('fgc-rs-github')
async def github(command, msg, user, channel, *args, **kwargs):
    # Static message for the Lizard-BOT Github
    return await fgc_rs_help('', '', '', '')

@register('fgc-rs-help')
async def fgc_rs_help(command, msg, user, channel, *args, **kwargs):
    # Message should only have two args at most
    if len(msg.split(' ')) > 2:
        raise Exception(bold("FGC_RS_Help") + ": Too many arguments. " + await fgc_rs_help('','','',''))
    help_commands = kwargs.get('help', False) # Get all the commands for the help message

    split = msg.lower().split(' ')
    cmd = ' '.join(split[0:2]) if len(split) > 1 else split[0]

    # Probably internal query from another command
    if not help_commands:
        return "For more information about the bot and its commands: <https://github.com/nogarremi/fgc-random-select-bot>"
    # No command specified
    elif not split[0]:
        return ('Allows you to get help on a command. '
                '\nThe available commands are ```%s```' % ', '.join(list(help_commands.keys())))
    # Return the help message
    elif cmd in help_commands.keys():
        return help_commands[cmd]
    # Invalid argument
    else:
        raise Exception(bold("FGC_RS_Help") + ": Invalid command: " + bold(cmd) + ". Ensure you are using the full command name."
                '\nThe available commands are ```%s```' % ', '.join(list(help_commands.keys())))

@register('nogarremi')
@register('ping')
@register('nog')
async def ping(command, msg, user, channel, *args, **kwargs):
    # FGC-RS-Bot's version of an !ping command
    return "Fuck you, Nog"

@register('randomselect')
@register('random')
@register('rs')
async def randomselect(command, msg, user, channel, *args, **kwargs):
    if len(msg.split(' ')) > 2:
        raise Exception(bold("RandomSelect") + ": Too many arguments. " + await fgc_rs_help('','','',''))
    # Start with randomselect basis to get characters
    random_type = ''
    game = msg.split(' ')[-1].lower()

    if msg.split(' ')[0].lower() != '':
        random_type = msg.split(' ')[0].lower()
    if random_type == "char" or (random_type == game and random_type != 'stage'):
        random_type = "character"

    if random_type == "character":
        if game in ["character", "char"]:
            # No game to be found so default to sfv
            game = 'sfv'
        elif msg.split(' ')[-1].lower() != '':
            game = msg.split(' ')[-1].lower()
        elif msg.split(' ')[-1].lower() == '':
            # No game to be found so default to sfv
            game = 'sfv'

    try:
        data, games = get_randomselect_data(game, random_type=random_type)
    except:
        raise Exception(bold("RandomSelect") + ": Invalid parameters. " + await fgc_rs_help('','','',''))

    if not data:
        raise Exception(bold("RandomSelect") + ": Invalid game: {0}. Valid games are: {1}".format(bold(game), bold(', '.join(games))))

    if random_type == "stage":
            return "{0} Your randomly selected stage is: {1}".format(user.mention, bold(random_choice(data)))
    return "{0} Your randomly selected character is: {1}".format(user.mention, bold(random_choice(data)))

