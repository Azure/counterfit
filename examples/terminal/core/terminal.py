
import importlib
from typing import Any

import cmd2
from counterfit import CFPrint
from examples.terminal import commands
from examples.terminal.core.state import CFState


class Terminal(cmd2.Cmd):
    """Terminal class responsible for setting the CLI and loading commands
    """
    _cmd = None

    def __init__(self):
        super().__init__(allow_cli_args=False, auto_load_commands=False)
        self._load_counterfit()
        self.prompt = "counterfit> "

    def default(self, command: str) -> None:
        """ Executed when the command given isn't a recognized command
        implemented by a do_* method.
        """
        CFPrint.warn("Command does not exist.\n")
        return

    def postcmd(self, stop, line):
        """ Set the prompt to reflect interaction changes. """
        active_attack = CFState.state().active_attack
        active_target = CFState.state().active_target
        if not active_target:
            self.prompt = "counterfit> "
            return
        if not active_attack:
            self.prompt = f"{active_target.target_name}> "
        else:
            attack_full_name = active_attack.name
            attack_name = attack_full_name.split(".")[-1]
            attack_info = f"{attack_name}:{active_attack.attack_id}"
            self.prompt = f"{active_target.target_name}>{attack_info}> "

        # Reload to update terminal to trigger new options to populate.
        self._load_counterfit()
        return stop


    # def pexcept(self, msg: Any, *, end: str = '\n', apply_style: bool = True) -> None:
    #     """Print an exception
    #     Args:
    #         msg (Any): [description]
    #         end (str, optional): [description]. Defaults to '\n'.
    #         apply_style (bool, optional): [description]. Defaults to True.
    #     """
    #     if isinstance(msg, Exception):
    #         final_msg = f"EXCEPTION of type '{type(msg).__name__}' occurred with message: {msg}"
    #     else:
    #         final_msg = str(msg)

    #     if apply_style:
    #         final_msg = cmd2.ansi.style_error(final_msg)

    #     if not self.debug and 'debug' in self.settables:
    #         warning = "\n [!] To enable full traceback, run the following command: 'set debug true'"
    #         final_msg += cmd2.ansi.style_warning(warning)

    #     self.perror(final_msg, end=end, apply_style=False)

    # @cmd2.with_category('Source Code Reload')
    # def do_reload_terminal(self, other):
    #     self._load_counterfit()

    def _load_counterfit(self):
        if self._cmd:
            self.unregister_command_set(self._cmd)
        importlib.reload(commands)
        self._cmd = commands.CounterfitCommands()
        self.register_command_set(self._cmd)
