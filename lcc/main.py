import argparse
import os

from lcc import compiler
from lcc.utils import LccError

join = os.path.join
split = os.path.split
real_path = os.path.realpath
exists = os.path.exists

DOT = '.'
OUTPUT_HELP = 'The file to create. ' \
              '(Default: current_working_directory/source_file_name.py)'


class Path:
    def __init__(self, initial):
        if isinstance(initial, Path):
            self.directory = initial.directory
            self.name = initial.name
            self.extension = initial.extension
            return

        full = real_path(initial)
        head, tail = split(full)
        self.directory = head

        if DOT in tail:
            *name_parts, extension = tail.split(DOT)
            name = DOT.join(name_parts)
        else:
            name = tail
            extension = ''

        self.name = name
        self.extension = extension

    def __str__(self):
        if self.extension:
            extension = DOT + self.extension
        else:
            extension = ''
        file = self.name + extension
        return join(self.directory, file)


def run_compiler(source, target):
    with open(source, mode='r', encoding='utf-8') as file:
        text = file.read()
    try:
        result = compiler.run_compile(text)
    except LccError as lcc_error:
        print('Compiler error: {}'.format(str(lcc_error)))
    except Exception as ex:
        print('Unknown error: {}'.format(ex))
    else:
        with open(target, mode='w', encoding='utf-8') as file:
            file.write(result)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('source_file', help='The lambda calculus file to compile')
    arg_parser.add_argument('-o', '--output', help=OUTPUT_HELP)
    args = arg_parser.parse_args()

    initial_source_file, initial_out_file = args.source_file, args.output
    source_path = Path(initial_source_file)

    if initial_out_file is None:
        target_path = Path(source_path)
        target_path.directory = os.getcwd()
        target_path.extension = 'py'
    else:
        target_path = Path(initial_out_file)

    valid = True
    if not exists(str(source_path)):
        valid = False
        print('Source path "{}" does not exist.'.format(source_path))

    if valid:
        run_compiler(str(source_path), str(target_path))


if __name__ == '__main__':
    main()
