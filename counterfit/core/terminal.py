import inspect
import os
import pkgutil
import sys
import types
from typing import Any
from cmd2 import Cmd
from cmd2 import ansi
from counterfit.core import config
from counterfit.core.state import CFState


class Terminal(Cmd):
    """Terminal class responsible for setting the CLI and loading commands"""
    # rename the built-in "set" attribute to "setg"
    setattr(Cmd, "do_setg", Cmd.do_set)
    delattr(Cmd, "do_set")

    def __init__(self, *args, **kwargs):
        super().__init__(use_ipython=True, startup_script=".counterfit")
        self.prompt = "counterfit> "

    def _set_prompt(self):
        if not CFState.get_instance().active_target:
            self.prompt = "counterfit> "

        else:
            if not CFState.get_instance().active_target.active_attack:
                self.prompt = f"{CFState.get_instance().active_target.model_name}> "
            else:
                self.prompt = f"{CFState.get_instance().active_target.model_name}>{CFState.get_instance().active_target.active_attack.attack_name}> "

    def default(self, command):
        """Executed when the command given isn't a recognized command implemented by a do_* method.

        :param command: command object with parsed input
        """
        self.pwarning("\n [!] Command does not exist.\n")
        return

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        self._set_prompt()
        return stop

    def load_commands(self):
        """Loads all the commands that exists under counterfit.commands sub-package"""
        commands_full_dir_path = os.path.join(os.getcwd(), config.commands_path)
        for module_finder, package_name, ispkg in pkgutil.iter_modules([commands_full_dir_path]):
            if not ispkg:
                current_module = module_finder.find_module(package_name).load_module()
                for member in inspect.getmembers(current_module, inspect.isfunction):
                    if "do_" in member[0] or "complete_" in member[0]:
                        setattr(self, member[0], types.MethodType(member[1], self))
                    if "finish_" in member[0]:
                        continue

    # same as in parent, except "setg debug true" instead of "set debug true"
    def pexcept(self, msg: Any, *, end: str = '\n', apply_style: bool = True) -> None:
        """Print Exception message to sys.stderr. If debug is true, print exception traceback if one exists.
        :param msg: message or Exception to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_error will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """
        if self.debug and sys.exc_info() != (None, None, None):
            import traceback

            traceback.print_exc()

        if isinstance(msg, Exception):
            final_msg = f"EXCEPTION of type '{type(msg).__name__}' occurred with message: {msg}"
        else:
            final_msg = str(msg)

        if apply_style:
            final_msg = ansi.style_error(final_msg)

        if not self.debug and 'debug' in self.settables:
            warning = "\n [!] To enable full traceback, run the following command: 'setg debug true'"
            final_msg += ansi.style_warning(warning)

        self.perror(final_msg, end=end, apply_style=False)

