import emoji
from colorama import Fore, Style

def text_print(text, emoji_name=None, color="CYAN"):
    """
    Prints text in the specified color with an optional emoji.

    :param text: The message to print.
    :param color: The color name (e.g., "CYAN", "GREEN", "RED"). Default is "CYAN".
    :param emoji_name: The emoji name (e.g., "smile", "rocket"). Default is None.
    """
    # Get the color dynamically from `Fore`
    color_attr = getattr(Fore, color.upper(), Fore.CYAN)  # Default to CYAN if invalid

    # Convert emoji name to actual emoji
    emoji_str = emoji.emojize(f":{emoji_name}:", language='alias') if emoji_name else ""

    # Print the formatted text
    print(color_attr + text + " " + emoji_str + Style.RESET_ALL)