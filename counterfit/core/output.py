from rich.console import Console

console = Console()

class CFPrint:
    @staticmethod
    def info(message: str):
        """Print an informational message

        Args:
            message (str): The message to print
        """
        console.print(f"[cyan][-][/cyan] {message}")

    @staticmethod
    def success(message: str):
        """Print a success message.

        Args:
            message (str): The message to print
        """
        console.print(f"[green][+][/green] {message}")

    @staticmethod
    def warn(message):
        """Print a warning message. Process can continue.

        Args:
            message (str): The message to print
        """
        console.print(f"[yellow][*][/yellow] {message}")

    @staticmethod
    def failed(message):
        """Print a failure message. Process cannot continue

        Args:
            message (str): The message to print
        """
        console.print(f"[red][!][/red] {message}")

    @staticmethod
    def output(message):
        """No output formatting.

        Args:
            message (str): The message to print
        """
        console.print(message)
