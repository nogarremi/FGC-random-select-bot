# Local imports
from commands import commands # Bring in all commands
from commands.utilities import get_callbacks # Bring in some utilities to help the process

# Yaksha
class Interface():

    # Yaksha
    # Initialize Interface with all our nice defaults
    def __init__(self, help):
        self._func_mapping = {} # Map for future reference
        self._modules = [commands] # Stores the reference to each .py we have command functions in
        self.remap_functions() # Map functions for reference by command name
        self.help = help # Bring over help info

    # Yaksha
    def remap_functions(self):
        '''
        Utilities.get_callbacks() returns a dictionary mapping of
        each command with the name of the function to be called.

        The name of the function is replaced by this function
        with a reference to the function and the class it belongs
        to. This is later used by self.call_command when handling
        messages.
        '''
        name_mapping = get_callbacks()

        for key, value in name_mapping.items():
            func_name = value[0]
            module_name = value[1]
            # Go through the imported modules to determine which
            # module the class belongs to.
            for module in self._modules:
                if module.__name__ != module_name:
                    continue
                else:
                    func_ref = getattr(module, func_name)

                    # Replace the function name with a tuple
                    # containing a reference to the function and
                    # the class name. The class name will be used
                    # get the correct class from self._class_mapping.
                    self._func_mapping[key] = func_ref
                    # We found the module so there is no need for further
                    # iterations.
                    break

    # Yaksha
    async def call_command(self, command, msg, user, channel, *args, **kwargs):
        '''
        Determines which function to call from the func_mapping
        dict using the command arg as the key.
        '''
        # Try to complete the command's function
        try:
            result = await self._func_mapping[command](command, msg, user, channel, *args, **kwargs)

            return result
        except:
            raise # Re-raise same error

