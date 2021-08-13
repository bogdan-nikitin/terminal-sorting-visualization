import abc
import shutil
import sys
import time

import terminal_utils
from terminal_utils import colorama


# TODO: Make it class members
ELEMENT_CHAR = '▓'
ACCESS_ELEMENT_CHAR = '░'
SORTED_ELEMENT_CHAR = '▒'
# ELEMENT_CHAR = colorama.Back.WHITE + ' '
# ACCESS_ELEMENT_CHAR = colorama.Back.RED + ' '

if terminal_utils.colorama:
    # TODO: Add ability to change these parameters from CLI
    ELEMENT_COLOR = colorama.Back.WHITE
    ACCESS_ELEMENT_COLOR = colorama.Back.RED
    # Should be changed to RESET, but BLUE is fine too
    BACKGROUND_COLOR = colorama.Back.BLUE
    FOREGROUND_COLOR = colorama.Fore.BLACK
    SORTED_BG_COLOR = colorama.Back.GREEN


ANSI_ELEMENT_CHAR = '_'
BACKGROUND_CHAR = ' '


class AbstractAccessPrinterList(abc.ABC):
    """
    Class that visualizes access to its items in the terminal
    """

    class SliceError(Exception):
        def __init__(self):
            super().__init__(
                f'{AbstractAccessPrinterList.__name__} does not support slices'
            )

    def __init__(self, lst, delay):
        """
        Init list and cashes some list properties
        """
        self.__delay = delay
        self._list = lst
        self._length = len(self._list)
        self._maximum = max(self._list)
        self.__terminal_size = shutil.get_terminal_size()
        self._first_print()

    def _catch_terminal_resizing(self):
        """
        Exits if catches a terminal resizing
        """
        if shutil.get_terminal_size() != self.__terminal_size:
            terminal_utils.clear_terminal()
            print('Error. Terminal size changed. Execution stopped')
            sys.exit(1)

    def _print_frame(self, frame):
        """
        Prints the frame of visualization and catches a terminal resizing
        """
        self._catch_terminal_resizing()
        print(frame, end='', flush=True)
        # flushing doesn't happen without delay on Mac OS
        time.sleep(self.__delay)

    @property
    @abc.abstractmethod
    def _first_print_preface(self) -> str:
        """
        What to print before calling _first_print 
        """
        pass

    @property
    @abc.abstractmethod
    def _element_char(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def _bg_color(self) -> str:
        pass

    def _first_print(self):
        """
        Prints all elements for the first time
        """
        terminal_utils.clear_terminal()

        to_print = self._first_print_preface
        element_char = self._element_char
        bg_char = self._bg_color + BACKGROUND_CHAR

        for i in range(self._maximum):
            for j in range(self._length):
                if self._list[j] >= self._maximum - i:
                    to_print += element_char
                else:
                    to_print += bg_char
            to_print += self._bg_color + '\n'
        self._print_frame(to_print)

    @abc.abstractmethod
    def end_of_sort(self):
        """
        Should print sorting completion animation
        """
        pass

    @abc.abstractmethod
    def _setitem(self, key: int, value: int):
        """
        Should handle __setitem__ call
        """
        pass

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise AbstractAccessPrinterList.SliceError
            # return self.__list.__setitem__(key, value)
        return self._setitem(key, value)

    @abc.abstractmethod
    def _getitem(self, item: int):
        """
        Should handle __getitem__ call
        """
        pass

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise AbstractAccessPrinterList.SliceError
        return self._getitem(item)

    def __len__(self):
        return self._length


# colorama needed
class ANSIAccessPrinterList(AbstractAccessPrinterList):
    def __init__(self, lst, delay):
        self.__last_access_item = None
        self.__last_access_item_value = None
        self.__cursor_pos = 0
        self.__element_color = ELEMENT_COLOR
        super().__init__(lst, delay)

    def __get_to_print_last_access_item(self):
        """
        Repaints the last accessed element to the element color
        """
        if self.__last_access_item is not None:
            return self.__get_to_print_element(
                self.__last_access_item,
                self.__element_color,
                self.__last_access_item_value
            )
        return ''

    def __print_item_setting(self, key):
        to_print = ''

        to_print += self.__get_to_print_element(key, ACCESS_ELEMENT_COLOR)
        to_print += self.__get_to_print_last_access_item()
        self._print_frame(to_print)
        self.__last_access_item = key
        self.__last_access_item_value = self._list[key]
        # self.__last_access_item_value = value

    def __get_to_print_element(self, item, color, previous_value=None):
        previous_value = previous_value or self._list[item]
        to_print = ''
        shift = item - self.__cursor_pos
        if shift > 0:
            to_print += colorama.Cursor.FORWARD(shift)
        elif shift < 0:
            to_print += colorama.Cursor.BACK(-shift)
        value = self._list[item]

        if value >= previous_value:
            to_print += color + FOREGROUND_COLOR
            to_print += colorama.Cursor.UP(value)
            to_print += (ANSI_ELEMENT_CHAR + colorama.Cursor.BACK() +
                         colorama.Cursor.DOWN()) * value
            to_print += BACKGROUND_COLOR
        else:
            to_print += BACKGROUND_COLOR
            to_print += colorama.Cursor.UP(previous_value)
            to_print += (BACKGROUND_CHAR + colorama.Cursor.BACK() +
                         colorama.Cursor.DOWN()) * (previous_value - value)
            to_print += color + FOREGROUND_COLOR
            to_print += (ANSI_ELEMENT_CHAR + colorama.Cursor.BACK() +
                         colorama.Cursor.DOWN()) * value
            to_print += BACKGROUND_COLOR
        # to_print += colorama.Cursor.BACK(item)
        self.__cursor_pos = item
        return to_print

    def __print_item_getting(self, item) -> None:
        to_print = ''

        to_print += self.__get_to_print_element(item, ACCESS_ELEMENT_COLOR)
        to_print += self.__get_to_print_last_access_item()
        self._print_frame(to_print)
        self.__last_access_item = item
        self.__last_access_item_value = None

    @property
    def _first_print_preface(self):
        return BACKGROUND_COLOR + '\n'

    @property
    def _element_char(self):
        return self.__element_color + FOREGROUND_COLOR + ANSI_ELEMENT_CHAR

    @property
    def _bg_color(self):
        return BACKGROUND_COLOR

    def end_of_sort(self):
        if self:
            self.__getitem__(0)
        self.__element_color = SORTED_BG_COLOR
        for i in range(1, self._length):
            self.__getitem__(i)

    def _setitem(self, key, value):
        self.__print_item_setting(key)
        return self._list.__setitem__(key, value)

    def _getitem(self, item):
        self.__print_item_getting(item)
        return self._list[item]


class NoANSIAccessPrinterList(AbstractAccessPrinterList):
    def __print_end_of_sort_till_item(self, item) -> None:
        to_print = ''
        for i in range(self._maximum):
            for j in range(self._length):
                if self._list[j] >= self._maximum - i:
                    if j < item:
                        char = SORTED_ELEMENT_CHAR
                    elif j == item:
                        char = ACCESS_ELEMENT_CHAR
                    else:
                        char = ELEMENT_CHAR
                    to_print += char
                else:
                    to_print += BACKGROUND_CHAR
            to_print += '\n'
        to_print += '\n' * max(
            shutil.get_terminal_size().lines - self._maximum, 0
        )
        self._print_frame(to_print)

    def __print_item_accessing(self, item) -> None:
        to_print = ''
        for i in range(self._maximum):
            for j in range(self._length):
                if self._list[j] >= self._maximum - i:
                    char = (ACCESS_ELEMENT_CHAR if item == j else
                            ELEMENT_CHAR)
                    to_print += char
                else:
                    to_print += BACKGROUND_CHAR
            to_print += '\n'
        to_print += '\n' * max(
            shutil.get_terminal_size().lines - self._maximum, 0
        )
        self._print_frame(to_print)

    @property
    def _first_print_preface(self):
        return ''

    @property
    def _element_char(self):
        return ELEMENT_CHAR

    @property
    def _bg_color(self):
        return ''

    def end_of_sort(self):
        for i in range(self._length):
            self.__print_end_of_sort_till_item(i)

    def _setitem(self, key, value):
        self.__print_item_accessing(key)
        result = self._list.__setitem__(key, value)
        self.__print_item_accessing(key)
        return result

    def _getitem(self, item):
        self.__print_item_accessing(item)
        return self._list[item]


def choose_access_printer_list_class():
    if terminal_utils.colorama:
        return ANSIAccessPrinterList
    else:
        return NoANSIAccessPrinterList
