import functools
import time

import terminal_utils
from terminal_utils import clear_terminal, move_cursor_to_start, colorama


class AccessPrinterList(list):
    """
    Class that visualizes access to its items in the terminal
    """
    ELEMENT_CHAR = '▓'
    ACCESS_ELEMENT_CHAR = '░'

    ELEMENT_COLOR = colorama.Back.WHITE
    ACCESS_ELEMENT_COLOR = colorama.Back.RED
    BACKGROUND_COLOR = colorama.Back.RESET

    # ELEMENT_CHAR = colorama.Back.WHITE + ' '
    # ACCESS_ELEMENT_CHAR = colorama.Back.RED + ' '

    @functools.wraps(list.__init__)
    def __init__(self, *args, **kwargs):
        """
        Init list and cashes some list properties
        """
        super().__init__(*args, **kwargs)
        self.__length = len(self)
        self.__maximum = max(self)
        self.__last_access_item = None
        self._first_print()

    def _first_print(self):
        """
        Prints all elements for the first time
        """
        clear_terminal()
        to_print = ''
        if terminal_utils.colorama:
            element_char = self.ELEMENT_COLOR + colorama.Fore.BLACK + '_'
            bg_char = self.BACKGROUND_COLOR + ' '
        else:
            element_char = self.ELEMENT_CHAR
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
        move_cursor_to_start()
        to_print = ''
        for i in range(self.__maximum):
            for j in range(self.__length):
                if super().__getitem__(j) >= self.__maximum - i:
                    char = (self.ACCESS_ELEMENT_CHAR if item == j else
                            self.ELEMENT_CHAR)
                    to_print += char
                else:
                    to_print += ' '
            to_print += '\n'
        print(to_print, end='')

    def _print_element(self, item, color, element=None) -> str:
        value = super().__getitem__(item)
        to_print = ''
        to_print += colorama.Cursor.FORWARD(item)
        element = element or value

        if element >= value:
            to_print += color + colorama.Fore.BLACK
            to_print += colorama.Cursor.UP(element)
            to_print += (
                                '_' + colorama.Cursor.BACK() +
                                colorama.Cursor.DOWN()
                        ) * element
            to_print += self.BACKGROUND_COLOR
        else:
            to_print += self.BACKGROUND_COLOR
            to_print += colorama.Cursor.UP(value)
            to_print += (
                                ' ' + colorama.Cursor.BACK() +
                                colorama.Cursor.DOWN()
                        ) * (value - element)
            to_print += color + colorama.Fore.BLACK
            to_print += (
                                '_' + colorama.Cursor.BACK() +
                                colorama.Cursor.DOWN()
                        ) * element
            to_print += self.BACKGROUND_COLOR
        to_print += colorama.Cursor.BACK(item)
        return to_print

    def __print_item_getting_with_ansi(self, item) -> None:
        """
        Visualize item getting using ANSI codes
        """
        to_print = ''

        to_print += self._print_element(item, self.ACCESS_ELEMENT_COLOR)
        if self.__last_access_item is not None:
            to_print += self._print_element(
                self.__last_access_item, self.ELEMENT_COLOR
            )
        print(to_print, end='')
        # print(self._print_element(item, self.ELEMENT_COLOR), end='')
        self.__last_access_item = item

    def __print_item_setting_with_ansi(self, key, value):
        """
        Visualize item setting using ANSI codes
        """
        to_print = ''

        to_print += self._print_element(key, self.ACCESS_ELEMENT_COLOR)
        if self.__last_access_item is not None:
            to_print += self._print_element(
                self.__last_access_item, self.ELEMENT_COLOR
            )
        to_print += self._print_element(key, self.ACCESS_ELEMENT_COLOR, value)
        print(to_print, end='')
        # print(self._print_element(key, self.ELEMENT_COLOR, value), end='')
        # print(self._print_element(key, self.ACCESS_ELEMENT_COLOR, value),
        #       end='')
        self.__last_access_item = None

    def __setitem__(self, key, value):
        if terminal_utils.colorama:
            self.__print_item_setting_with_ansi(key, value)
            return super().__setitem__(key, value)
        else:
            self.__print_item_accessing_without_ansi(key)
            item = super().__setitem__(key, value)
            self.__print_item_accessing_without_ansi(key)
            return item

    def __getitem__(self, item):
        if terminal_utils.colorama:
            self.__print_item_getting_with_ansi(item)
        else:
            self.__print_item_accessing_without_ansi(item)
        return super().__getitem__(item)
