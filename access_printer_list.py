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

    def __access_item_without_ansi(self, item):
        pass

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

    def _access_item(self, item):
        to_print = ''
        if terminal_utils.colorama:
            for i, char in ((self.__last_access_item, self.ELEMENT_CHAR),
                            (item, self.ACCESS_ELEMENT_CHAR),):
                if i is not None:
                    to_print += self._print_element(i, char)
            to_print += colorama.Cursor.UP()
        else:
            move_cursor_to_start()
            for i in range(self.__maximum):
                for j in range(self.__length):
                    if super().__getitem__(j) >= self.__maximum - i:
                        char = (self.ACCESS_ELEMENT_CHAR if item == j else
                                self.ELEMENT_CHAR)
                        to_print += char
                    else:
                        to_print += ' '
                to_print += '\n'
        print(to_print)
        # exit()
        # exit() if self.__last_access_item is not None else None
        self.__last_access_item = item

    def __setitem__(self, key, value):
        # self._access_item(key)
        print(self._print_element(self.__last_access_item, self.ELEMENT_CHAR)
              + colorama.Cursor.UP())
        print(self._print_element(key, self.ACCESS_ELEMENT_CHAR) +
              colorama.Cursor.UP())
        print(self._print_element(key, self.ACCESS_ELEMENT_CHAR,
                                  value) + colorama.Cursor.UP())
        self.__last_access_item = key
        # result = super().__setitem__(key, value)
        # self._access_item(key)

        return super().__setitem__(key, value)
        # return result

    def __getitem__(self, item):
        self._access_item(item)
        return super().__getitem__(item)
