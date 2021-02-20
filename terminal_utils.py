import os

from singleton import CallSingleton

try:
    import colorama
except ModuleNotFoundError:
    colorama = None


class _ClearConsole(CallSingleton):
    def __init__(self):
        super().__init__()
        if colorama:
            self._call = lambda: print(colorama.Back.RESET +
                                       colorama.Fore.RESET +
                                       colorama.ansi.clear_screen())
        elif os.name in ('nt', 'dos'):
            self._call = lambda: os.system("cls")
        elif os.name in ('linux', 'osx', 'posix'):
            self._call = lambda: os.system("clear")
        else:
            self._call = lambda: print("\n" * 120)


class _MoveCursorToStart(CallSingleton):
    def __init__(self):
        super().__init__()
        if colorama:
            self._call = lambda: print('\033[H')
        else:
            self._call = lambda: clear_terminal()


def clear_terminal():
    _ClearConsole()()


def move_cursor_to_start():
    _MoveCursorToStart()()
