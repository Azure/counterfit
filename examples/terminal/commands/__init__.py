import argparse
import importlib

import cmd2
import examples.terminal.commands.docs as docs_
import examples.terminal.commands.exit as exit_
import examples.terminal.commands.interact as interact_
import examples.terminal.commands.list as list_
import examples.terminal.commands.new as new_
import examples.terminal.commands.predict as predict_
import examples.terminal.commands.reload as reload_
import examples.terminal.commands.run as run_
import examples.terminal.commands.save as save_
import examples.terminal.commands.scan as scan_
import examples.terminal.commands.set as set_
import examples.terminal.commands.show as show_
import examples.terminal.commands.use as use_

# Reload all the Counterfit Commands to allow for real-time source-code updates
# https://docs.python.org/3/library/importlib.html#importlib.reload
importlib.reload(docs_)
importlib.reload(exit_)
importlib.reload(interact_)
importlib.reload(list_)
importlib.reload(new_)
importlib.reload(predict_)
importlib.reload(reload_)
importlib.reload(run_)
importlib.reload(save_)
importlib.reload(scan_)
importlib.reload(set_)
importlib.reload(show_)
importlib.reload(use_)

@cmd2.with_default_category("Counterfit Commands")
class CounterfitCommands(cmd2.CommandSet):
    def __init__(self):
        """ Initialize the Counterfit Commands object. """
        super().__init__()

    @cmd2.with_argparser(interact_.interact_args)
    def do_interact(self, args: argparse.Namespace) -> None:
        """ Sets the the active target. """
        interact_.interact_cmd(args)

    @cmd2.with_argparser(list_.list_args)
    def do_list(self, args: argparse.Namespace) -> None:
        """ List available targets, commands, and frameworks."""
        list_.list_cmd(args)

    @cmd2.with_argparser(new_.new_args)
    def do_new(self, args: argparse.Namespace) -> None:
        """ Create a new template. """
        new_.new_cmd(args)

    @cmd2.with_argparser(predict_.predict_args)
    def do_predict(self, args: argparse.Namespace) -> None:
        """ Predict the classification of the N-th attack generated sample for a given target.

        This command can be used for initial prediction and after attack
        prediction for a given sample.

        The index range will be limited to the number of available samples
        for any given target.
        """
        predict_.predict_cmd(args)
    #
    # @cmd2.with_argparser(reload_.reload_args)
    # def do_reload(self, args: argparse.Namespace) -> None:
    #     """ Reload the Counterfit object. """
    #     reload_.reload_cmd(args)

    @cmd2.with_argparser(run_.run_args)
    def do_run(self, args: argparse.Namespace) -> None:
        """ Run specified attack on target.
        These options must be preset prior to running the command.
        """
        run_.run_cmd(args)

    @cmd2.with_argparser(save_.save_args)
    def do_save(self, args: argparse.Namespace) -> None:
        """ Save things. """
        save_.save_cmd(args)

    @cmd2.with_argparser(scan_.scan_args)
    def do_scan(self, args: argparse.Namespace) -> None:
        """ Save things. """
        scan_.scan_cmd(args)

    @cmd2.with_argparser(set_.set_args)
    def do_set_params(self, args: argparse.Namespace) -> None:
        """Set parameters of the active attack on the active target using 

        For infinity, use 'inf' or 'float("inf")'.

        This command replaces built-in "set" command, which is renamed to "setg".
        """
        set_.set_cmd(args)

    @cmd2.with_argparser(show_.show_args)
    def do_show(self, args: argparse.Namespace) -> None:
        """'show info' describes the active attack.
        'show options' lists attack parameters.
        'show sample' displays the target data
        """
        show_.show_cmd(args)

    @cmd2.with_argparser(use_.set_attack_args)
    def do_use(self, args: argparse.Namespace) -> None:
        """Select an attack to use on the active target.
        Use 'interact' to select a target first.
        """
        use_.set_attack_cmd(args)


    @cmd2.with_argparser(docs_.docs_args)
    def do_docs_server(self, args: argparse.Namespace) -> None:
        """Start a local web server that hosts the documentation

        """
        docs_.docs_cmd(args)


    @cmd2.with_argparser(exit_.exit_args)
    def do_exit(self, args: argparse.Namespace) -> None:
        """Exit Counterfit
        """
        exit_.exit_cmd(args)
