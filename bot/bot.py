import discord # Discord bot needs discord library

from asyncio import sleep as asyncio_sleep # For sleeping specific threads
from json import loads as json_loads # For bringing in config file
from os import path as os_path # For bringing in config file
from traceback import print_exc as traceback_print_exc, format_exc as traceback_format_exc # For printing error messages
from sys import exc_info as sys_exc_info # For grabbing error information

# Local imports
import interface # The selector between bot.py and commands
from secret import token # Discord token

intents = discord.Intents.default()
intents.message_content = True

# Create the Discord client
client = discord.Client(
    intents=intents
)

# Once bot is fully logged in, print the guilds it is in
@client.event
async def on_ready():
    print('\nLogged in as {0.user}'.format(client))
    print('-------------------------------')
    for guild in client.guilds:
        print('Joined guild %s' % guild)

# Yaksha
# When message is typed in any channel the bot has access to, check to see if the bot needs to respond
@client.event
async def on_message(message):
    # If the bot is the user, do not respond
    if message.author == client.user:
        return

    # If the bot is mentioned in a message, respond with a message informing it of being a bot
    if client.user.mentioned_in(message):
        return

    try:
        prefix = "!"

        # If other commands don't start with the correct prefix, do nothing
        if not message.content.startswith(prefix):
            return
        # Check if the attempted_cmd takes arguments
        elif message.content.split(' ')[0][1:].lower() in client.no_arg_cmds and len(message.content.split()) > 1:
            await message.channel.send("Too many arguments. Check !fgc-rs-help for more info")
            return

        # Rotate through commands to see if the message matches
        for command in client.commands:
            command = command.lower() # Lower the command for easier matching
            msg = message.content # The message
            attempted_cmd = msg.split(' ')[0][1:].lower() # Get the attempted command from the beginning of the string

            if attempted_cmd in ['challonge', 'chal', 'edit'] and len(msg.split(' ')) > 1:
                attempted_cmd += ' ' + msg.split(' ')[1].lower()

            # Check if the message begins with a command
            if attempted_cmd and attempted_cmd == command:
                user = message.author # The author
                kwargs = {'guild':message.guild.id}

                # Remove the command from the start
                msg = msg[len(command)+1:].strip()

                # Await the interface calling the command
                response = await client.interface.call_command(command, msg, user, message.channel, **kwargs)
                # If there is a response, send it
                if response:
                    await message.channel.send(response)
                break
    except Exception:
        string_info = str(sys_exc_info()[1]) # Error message
        function_name = string_info.split(':')[0] # The command the error message came from

        # Expected error
        # Return friendly user message
        # Additional checks needed for challonge and edit commands that have multiple subcommands
        if client.interface._func_mapping[command].__name__ in function_name.strip("*").lower():
            await message.channel.send(function_name.replace('_', '-') + ': ' + ':'.join(string_info.split(':')[1:]))
        else:
            # Print error to console
            traceback_print_exc()
            # If we get this far and something breaks
            # Something is very wrong. Send user generic error message
            await message.channel.send("I is broken.\nSubmit an issue via <https://github.com/nogarremi/fgc-random-select-bot/issues>\nOr just tell Nogarremi. That's what I do.")

# Yaksha
# Main thread the kicks off the initial setup and starts the bot
def main():
    print(token)
    client.commands, client.no_arg_cmds = [], [] # Init
    client.help = {} # Init

    # Pull in a separate config
    config = json_loads(open(os_path.join(os_path.dirname(__file__), 'commands/bots.json')).read())

    # Grab our commands from the json
    commands = list(config.get('common_commands', {}).copy().values())
    no_arg_cmds = config.get('no_arg_commands', []).copy()

    # Sort the raw json into the appropriate variables
    # For every entry in commands loop over the child array
    for aliases in commands:
        # For every child in the child array, sort it to the appropriate variable for later
        for alias in aliases:
            # If the child item is the last item(the help message), move on to the next command
            if alias == aliases[-1]:
                break
            # Elif the full command doesn't take args, have the aliases not accept args
            elif aliases[0] in no_arg_cmds:
                client.no_arg_cmds.append(alias.lower())
            # Add the help message for each alias
            client.help.update({alias.lower():aliases[-1]})
            # Add the command and aliases as valid commands
            client.commands.append(alias)

    # Start our interface for our commands and Discord
    client.interface = interface.Interface(client.help)

    # Start the bot
    client.run(token)

# If main is here, run main
if __name__ == '__main__':
    main()
