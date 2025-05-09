import emoji
from colorama import Fore, Style

def text_print(text, color="CYAN"):
    """
    Prints text in the specified color.

    :param text: The message to print.
    :param color: The color name (e.g., "CYAN", "GREEN", "RED"). Default is "CYAN".
    """
    # Get the color dynamically from `Fore`
    color_attr = getattr(Fore, color.upper(), Fore.CYAN)  # Default to CYAN if invalid

    # Print the formatted text
    print(color_attr + text + Style.RESET_ALL)