import argparse
import random
import runpy
import time
import typing

import terminal_utils
from access_printer_list import AccessPrinterList
from singleton import Singleton
from sorting_algorithms import SORTING_ALGORITHMS

DEFAULT_MINIMUM = 1
DEFAULT_MAXIMUM = 70  # 80
DEFAULT_LENGTH = 200
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
    'Maximum value of the generating array. Must be greater, than --min value'
)
LENGTH_HELP = (
    'Count of the array elements. Must be greater, than 0'
)


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
            default=DEFAULT_MAXIMUM,
            help=MAX_HELP,
            type=int,
            dest='max'
        )
        self._parser.add_argument(
            '-N', '--array-length',
            default=DEFAULT_LENGTH,
            help=LENGTH_HELP,
            type=int,
            dest='length'
        )
        self._parser.add_argument(
            '--no-colorama', '-n',
            default=False,
            type=bool,
            dest='no_colorama'
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
                if not self._sorting_function :
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

        # Now checking --min, --max and --length args
        if not self._args.min > 0:
            print('Error. --min value must be greater than 0')
            return False
        if not self._args.max > self._args.min:
            print('Error. --max value must be greater than --min value')
            return False
        if not self._args.length > 0:
            print('Error. --length value must be greater than 0')
            return False

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

        array = create_array(self._args.min, self._args.max, self._args.length)
        to_sort_array = array.copy()
        shuffled_arr = to_sort_array.copy()
        to_sort_array = AccessPrinterList(to_sort_array)

        start_time = time.time()

        self._sorting_function(to_sort_array)

        for i in range(len(to_sort_array)):
            to_sort_array.__getitem__(i)

        # Print sorting info
        sort_time = time.time() - start_time
        print('Sorted for', sort_time)
        print('Original array', shuffled_arr)
        print('Sorted array', list(to_sort_array))
