import argparse
import random
import runpy
import shutil
import time
import typing

import terminal_utils
from access_printer_list import AccessPrinterList
from singleton import Singleton
from sorting_algorithms import SORTING_ALGORITHMS

DEFAULT_MINIMUM = 1
DESCRIPTION = (
    'Visualization of sorting algorithms in a terminal. For better experience '
    'you need to install the colorama package'
)
ALGORITHM_ARG_HELP = (
    'Sorting algorithm which be visualized. You may choose one of the builtin '
    'algorithms or specify the algorithm from an external script (in this way '
    'this argument means the function name from the --script argument; '
    'function must accept a single argument - sorting array and mustn\'t '
    'return anything; array must be sorted in-place). The builtin algorithms '
    'are {sorting_algorithms_names}'
)
SCRIPT_ARG_HELP = (
    'Path to the external script where sorting algorithm will be imported from'
)
MIN_HELP = 'Minimum value of the generating array. Must be greater, than 0'
MAX_HELP = (
    'Maximum value of the generating array. Must be greater, than --min value. '
    'By default it\'s equal to half of the height of the terminal'
)
LENGTH_HELP = (
    'Count of the array elements. Must be greater, than 0. By default it\'s '
    'equal to half of the width of the terminal'
)


def print_terminal_size(columns=None, lines=None):
    if not (columns and lines):
        columns, lines = shutil.get_terminal_size()
    print(f'Your terminal size is ({columns}, {lines})')


def create_array(
        min_val: int, max_val: int, length: int
) -> typing.List[int]:
    """
    Creates array of random numbers
    :param min_val: Minimal value to generate
    :param max_val: Maximal value to generate
    :param length: Length of the generating array
    :return: Array of random numbers
    """
    return [random.randint(min_val, max_val) for _ in range(length)]


class Program(Singleton):
    def __init__(self):
        self._sorting_algorithms_names = list(SORTING_ALGORITHMS.keys())
        self._parser = argparse.ArgumentParser(
            description=DESCRIPTION
        )
        self._init_parser()

        # Parser arguments
        self._args = None

        # Array properties
        self._min_element = None
        self._max_element = None
        self._array_length = None

        # Function which be used for array sorting
        self._sorting_function = None

    def _init_parser(self):
        """
        Inits command-line arguments parser
        """
        self._parser.add_argument(
            '-a', '--algorithm',
            default=self._sorting_algorithms_names[0],
            help=ALGORITHM_ARG_HELP.format(
                sorting_algorithms_names=', '.join(
                    self._sorting_algorithms_names
                )
            ),
            dest='algorithm'
        )
        self._parser.add_argument(
            '-s', '--script',
            help=SCRIPT_ARG_HELP,
            dest='script'
        )
        self._parser.add_argument(
            '--min',
            default=DEFAULT_MINIMUM,
            help=MIN_HELP,
            type=int,
            dest='min'
        )
        self._parser.add_argument(
            '--max',
            help=MAX_HELP,
            type=int,
            dest='max'
        )
        self._parser.add_argument(
            '-N', '--length',
            help=LENGTH_HELP,
            type=int,
            dest='length'
        )
        self._parser.add_argument(
            '--no-colorama', '-n',
            dest='no_colorama',
            action='store_true'
        )

    def _is_args_valid(self) -> bool:
        """
        Validates arguments and prints an error message if the arguments are
        incorrect
        :return: True if the arguments are valid else False
        """
        algorithm = self._args.algorithm

        # Checking --algorithm and --script args
        if algorithm not in self._sorting_algorithms_names:
            script = self._args.script
            if not script:
                print(
                    f'Error. {algorithm} is not a builtin algorithm, so you '
                    f'must specify --script argument'
                )
                return False
            try:
                script_dict = runpy.run_path(script)
                self._sorting_function = script_dict.get(algorithm)
                if not self._sorting_function:
                    print(
                        f'Error. There is no {algorithm} function in the '
                        f'{script}'
                    )
                    return False
            except FileNotFoundError:
                print(f'Error. File {script} not found')
                return False
            except Exception as exception:
                print(f'Error. {type(exception).__name__} exception occurred '
                      f'during {script} executing. '
                      f'Additional info: {exception}')
                return False
        else:
            self._sorting_function = SORTING_ALGORITHMS[self._args.algorithm]

        # Now checking --min, --max and --length args and setting
        # _min_element, _max_element and _array_length fields
        columns, lines = shutil.get_terminal_size()

        self._min_element = self._args.min
        if not self._args.min > 0:
            print('Error. --min value must be greater than 0')
            return False
        elif self._args.min >= lines:
            print('Error. --min value must be less than your terminal size')
            print_terminal_size(columns, lines)
            return False

        if self._args.max is None:
            self._max_element = lines // 2
        else:
            if self._args.max >= lines:
                print('Error. --max value must be less than your terminal size')
                print_terminal_size(columns, lines)
                return False
            elif not self._args.max >= self._args.min:
                print('Error. --max value must be greater than or equal to '
                      '--min value')
                return False
            self._max_element = self._args.max

        if self._args.length is None:
            self._array_length = columns // 2
        else:
            if not self._args.length > 0:
                print('Error. --length value must be greater than 0')
                return False
            elif self._args.length >= columns:
                print('Error. --length value must be less than terminal size')
                print_terminal_size(columns, lines)
                return False
            self._array_length = self._args.length

        # Everything is correct
        return True

    def main(self):
        """
        Main method of the program. Read and validate arguments and if
        everything is OK visualize array sorting
        """
        self._args = self._parser.parse_args()
        if not self._is_args_valid():
            return

        if self._args.no_colorama:
            terminal_utils.colorama = None
        if terminal_utils.colorama:
            terminal_utils.colorama.init()

        array = create_array(self._min_element,
                             self._max_element,
                             self._array_length)
        to_sort_array = array.copy()
        shuffled_arr = to_sort_array.copy()
        to_sort_array = AccessPrinterList(to_sort_array)

        # Visualising sorting
        try:
            start_time = time.time()
            self._sorting_function(to_sort_array)
            to_sort_array.end_of_sort()
            # Print sorting info
            sort_time = time.time() - start_time
            if terminal_utils.colorama:
                print(terminal_utils.colorama.Back.RESET +
                      terminal_utils.colorama.Fore.RESET)
            print()
            print('Sorted and visualized for', sort_time)
            print('Original array', shuffled_arr)
            print('Sorted array', list(to_sort_array))
        except KeyboardInterrupt:
            terminal_utils.clear_terminal()
            # print(terminal_utils.colorama.Back.RESET +
            #       terminal_utils.colorama.Fore.RESET)
            print('Error. Program execution was interrupted')
