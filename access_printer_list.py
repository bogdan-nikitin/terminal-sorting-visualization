import functools
import time

from terminal_utils import clear_terminal, move_cursor_to_start, colorama
import terminal_utils


class AccessPrinterList(list):
    # ELEMENT_CHAR = colorama.Fore.WHITE + '▓' if colorama else '▓'
    # ACCESS_ELEMENT_CHAR = colorama.Fore.RED + '▓' if colorama else '░'
    ELEMENT_CHAR = '▓'
    ACCESS_ELEMENT_CHAR = '░'

    @functools.wraps(list.__init__)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__length = len(self)
        self.__maximum = max(self)
        self.__last_access_item = None
        self._first_print()

    def _first_print(self):
        clear_terminal()
        to_print = ''
        for i in range(self.__maximum):
            for j in range(self.__length):
                if super().__getitem__(j) >= self.__maximum - i:
                    char = self.ELEMENT_CHAR
                    to_print += char
                else:
                    to_print += ' '
            to_print += '\n'
        to_print += colorama.Cursor.UP()
        print(to_print)

    def recalculate(self):
        self.__length = len(self)
        self.__maximum = max(self)

    def __print_item_accessing_without_ansi(self, item):
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

    def _print_element(self, item, char, element=None) -> str:
        value = super().__getitem__(item)
        to_print = ''
        to_print += colorama.Cursor.FORWARD(item)
        element = element or value
        if element >= value:
            to_print += colorama.Cursor.UP(element)
            to_print += (
                    char + colorama.Cursor.BACK() + colorama.Cursor.DOWN()
            ) * element
        else:
            to_print += colorama.Cursor.UP(value)
            to_print += (
                    ' ' + colorama.Cursor.BACK() + colorama.Cursor.DOWN()
            ) * (value - element)
            to_print += (
                    char + colorama.Cursor.BACK() + colorama.Cursor.DOWN()
            ) * element
        to_print += colorama.Cursor.BACK(item)
        return to_print

    def __print_item_getting_with_ansi(self, item):
        to_print = ''
        for i, char in ((self.__last_access_item, self.ELEMENT_CHAR),
                        (item, self.ACCESS_ELEMENT_CHAR),):
            if i is not None:
                to_print += self._print_element(i, char)
        print(to_print, end='')
        self.__last_access_item = item

    def __print_item_setting_with_ansi(self, key, value):
        to_print = ''
        to_print += self._print_element(
            self.__last_access_item, self.ELEMENT_CHAR
        )
        to_print += self._print_element(key, self.ACCESS_ELEMENT_CHAR)
        print(to_print, end='')
        print(
            self._print_element(key, self.ACCESS_ELEMENT_CHAR, value),
            end=''
        )
        self.__last_access_item = key

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
