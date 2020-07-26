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

    def _print_element(self, item, char):
        # move_cursor_to_start()
        element = super().__getitem__(item)
        to_print = ''
        # to_print += '\033[H'

        to_print += colorama.Cursor.UP(self.__maximum)

        # last_access = self.__last_access_item or 0
        # if last_access > item:
        #     to_print += colorama.Cursor.BACK(last_access - item)
        # else:
        #     to_print += colorama.Cursor.FORWARD(item - last_access)

        # to_print += colorama.Cursor.POS(item + 1, '')
        to_print += colorama.Cursor.FORWARD(item)
        # to_print += f'\033[G'
        # to_print += colorama.Cursor.FORWARD(2)
        i = 0
        for i in range(self.__maximum - element):
            to_print += ' '
            to_print += colorama.Cursor.BACK()
            to_print += colorama.Cursor.DOWN()
        f_i = i
        for i in range(element):
            to_print += char
            to_print += colorama.Cursor.BACK()
            # break
            to_print += colorama.Cursor.DOWN()
        with open('log.txt', mode='a') as file:
            file.write(f'i:\t{f_i},\ti:\t{i},\titerations:\t{f_i + i},\t'
                       f'maximum:\t{self.__maximum},\telement:\t{element},'
                       f'\titem:\t{item},\tchar:\t{ord(char)}')
            file.write('\n')
        # print(f_i, i, f_i + i, self.__maximum, element)
        to_print += colorama.Cursor.BACK(item)
        # time.sleep(0.2)
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
        # if self.__last_access_item is not None:
        #     exit()
        #     print(super().__getitem__(item))
        self.__last_access_item = item

    def __setitem__(self, key, value):
        self._access_item(key)
        result = super().__setitem__(key, value)
        self._access_item(key)
        return result

    def __getitem__(self, item):
        self._access_item(item)
        return super().__getitem__(item)
