import functools
import shutil

import terminal_utils
from terminal_utils import clear_terminal, move_cursor_to_start, colorama


ELEMENT_CHAR = '▓'
ACCESS_ELEMENT_CHAR = '░'
SORTED_ELEMENT_CHAR = '▒'
# ELEMENT_CHAR = colorama.Back.WHITE + ' '
# ACCESS_ELEMENT_CHAR = colorama.Back.RED + ' '

if terminal_utils.colorama:
    ELEMENT_COLOR = colorama.Back.WHITE
    ACCESS_ELEMENT_COLOR = colorama.Back.RED
    BACKGROUND_COLOR = colorama.Back.RESET
    FOREGROUND_COLOR = colorama.Fore.BLACK
    SORTED_BG_COLOR = colorama.Back.GREEN


class AccessPrinterList(list):
    """
    Class that visualizes access to its items in the terminal
    """
    @functools.wraps(list.__init__)
    def __init__(self, *args, **kwargs):
        """
        Init list and cashes some list properties
        """
        super().__init__(*args, **kwargs)
        self.__length = len(self)
        self.__maximum = max(self)
        self.__last_access_item = None
        self.__last_access_item_value = None
        self.__cursor_pos = 0
        if terminal_utils.colorama:
            self.element_color = ELEMENT_COLOR
        self._first_print()

    def _first_print(self):
        """
        Prints all elements for the first time
        """
        clear_terminal()
        to_print = ''
        if terminal_utils.colorama:
            element_char = self.element_color + FOREGROUND_COLOR + '_'
            bg_char = BACKGROUND_COLOR + ' '
        else:
            element_char = ELEMENT_CHAR
            bg_char = ' '
        for i in range(self.__maximum):
            for j in range(self.__length):
                if super().__getitem__(j) >= self.__maximum - i:
                    to_print += element_char
                else:
                    to_print += bg_char
            to_print += '\n'
        print(to_print, end='')

    def recalculate(self):
        """
        Recalculates the cached list properties. Always use it, when you adding
        or removing an element
        """
        self.__length = len(self)
        self.__maximum = max(self)

    def __print_item_accessing_without_ansi(self, item) -> None:
        """
        Visualize item accessing (getting or setting) without using ANSI codes
        """
        to_print = ''
        for i in range(self.__maximum):
            for j in range(self.__length):
                if super().__getitem__(j) >= self.__maximum - i:
                    char = (ACCESS_ELEMENT_CHAR if item == j else
                            ELEMENT_CHAR)
                    to_print += char
                else:
                    to_print += ' '
            to_print += '\n'
        to_print += '\n' * max(
            shutil.get_terminal_size().lines - self.__maximum, 0
        )
        print(to_print, end='')

    def __print_end_of_sort_without_ansi(self, item) -> None:
        """
        Visualize end of sort without using ANSI codes
        """
        to_print = ''
        for i in range(self.__maximum):
            for j in range(self.__length):
                if super().__getitem__(j) >= self.__maximum - i:
                    if j < item:
                        char = SORTED_ELEMENT_CHAR
                    elif j == item:
                        char = ACCESS_ELEMENT_CHAR
                    else:
                        char = ELEMENT_CHAR
                    to_print += char
                else:
                    to_print += ' '
            to_print += '\n'
        to_print += '\n' * max(
            shutil.get_terminal_size().lines - self.__maximum, 0
        )
        print(to_print, end='')

    def _print_element(self, item, color, previous_value=None) -> str:
        previous_value = previous_value or super().__getitem__(item)
        to_print = ''
        shift = item - self.__cursor_pos
        if shift > 0:
            to_print += colorama.Cursor.FORWARD(shift)
        elif shift < 0:
            to_print += colorama.Cursor.BACK(-shift)
        value = super().__getitem__(item)

        if value >= previous_value:
            to_print += color + FOREGROUND_COLOR
            to_print += colorama.Cursor.UP(value)
            to_print += (
                                '_' + colorama.Cursor.BACK() +
                                colorama.Cursor.DOWN()
                        ) * value
            to_print += BACKGROUND_COLOR
        else:
            to_print += BACKGROUND_COLOR
            to_print += colorama.Cursor.UP(previous_value)
            to_print += (
                                ' ' + colorama.Cursor.BACK() +
                                colorama.Cursor.DOWN()
                        ) * (previous_value - value)
            to_print += color + FOREGROUND_COLOR
            to_print += (
                                '_' + colorama.Cursor.BACK() +
                                colorama.Cursor.DOWN()
                        ) * value
            to_print += BACKGROUND_COLOR
        # to_print += colorama.Cursor.BACK(item)
        self.__cursor_pos = item
        return to_print

    def __print_item_getting_with_ansi(self, item) -> None:
        """
        Visualize item getting using ANSI codes
        """
        to_print = ''

        to_print += self._print_element(item, ACCESS_ELEMENT_COLOR)
        if self.__last_access_item is not None:
            to_print += self._print_element(
                self.__last_access_item,
                self.element_color,
                self.__last_access_item_value
            )
        print(to_print, end='')
        self.__last_access_item = item
        self.__last_access_item_value = None

    def __print_item_setting_with_ansi(self, key, value):
        """
        Visualize item setting using ANSI codes
        """
        to_print = ''

        to_print += self._print_element(key, ACCESS_ELEMENT_COLOR)
        if self.__last_access_item is not None:
            to_print += self._print_element(
                self.__last_access_item,
                self.element_color,
                self.__last_access_item_value
            )
        print(to_print, end='')
        self.__last_access_item = key
        self.__last_access_item_value = super().__getitem__(key)

    def end_of_sort(self):
        if terminal_utils.colorama:
            if self:
                self.__getitem__(0)
            self.element_color = SORTED_BG_COLOR
            for i in range(1, len(self)):
                self.__getitem__(i)
        else:
            for i in range(len(self)):
                self.__print_end_of_sort_without_ansi(i)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            return super().__setitem__(key, value)
        if terminal_utils.colorama:
            self.__print_item_setting_with_ansi(key, value)
            return super().__setitem__(key, value)
        else:
            self.__print_item_accessing_without_ansi(key)
            item = super().__setitem__(key, value)
            self.__print_item_accessing_without_ansi(key)
            return item

    def __getitem__(self, item):
        if isinstance(item, slice):
            return super().__getitem__(item)
        if terminal_utils.colorama:
            self.__print_item_getting_with_ansi(item)
        else:
            self.__print_item_accessing_without_ansi(item)
        return super().__getitem__(item)
