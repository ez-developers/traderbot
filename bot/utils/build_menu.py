from telegram import KeyboardButton
from typing import Union, List


def build_menu(
    buttons: List[KeyboardButton],
    n_cols: int,
    header_buttons: Union[KeyboardButton,
                          List[KeyboardButton]] = None,
    footer_buttons: Union[KeyboardButton,
                          List[KeyboardButton]] = None) -> List[List[KeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(
            header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(
            footer_buttons, list) else [footer_buttons])
    return menu
