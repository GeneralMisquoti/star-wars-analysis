from __future__ import annotations
from collections import OrderedDict
import argparse
from utils import file_names
from pathlib import Path
import csv
from typing import List, Optional, Tuple, Dict
HERE = Path(__file__).parent
DATA = HERE / "data"


def filter_files(filtered: List[int]):
    file_paths = []
    if args.only_movies:
        for i in args.only_movies:
            if i not in range(1, 9):
                raise Exception(
                    f"Filter part number {i} is not in range 1-8"
                )
            file_paths.append(file_names[i-1])
    else:
        file_paths = file_names
    file_paths = map(lambda p: DATA / p, file_paths)
    return file_paths


def count_words(line):
    return len(line[3].strip().split(' '))


def wc(args):
    global file_names
    wc = 0
    character = args.character
    file_paths = filter_files(args.only_movies)

    for path in file_paths:
        matched_characters = set()
        sub_wc = 0
        reader = csv.reader(path.open('r', encoding='UTF-8'))
        if character is None:
            for line in reader:
                sub_wc += count_words(line)
            print(f'{sub_wc} words in file {path.name}')
        else:
            lower_character = character.strip().lower()
            for line in reader:
                if lower_character in line[0].strip().lower() :
                    matched_characters.add(line[0])
                    sub_wc += count_words(line)
            print(
                f'Character '
                f'{matched_characters if len(matched_characters) > 0 else character} '
                f'has {sub_wc} words in file {path.name}'
            )
        wc += sub_wc


def are_characters_in_line(line: List[str], lower_characters: List[str], orig_characters: Optional[List[str]] = None, resolve_groups=True):
    speaker = line[0].strip().lower()
    speaked_to = line[1].strip().lower()
    if resolve_groups:
        is_speaker = [orig_characters[i] for i, x in enumerate(lower_characters) if x in speaker]
        is_speaked_to = [orig_characters[i] for i, x in enumerate(lower_characters) if x in speaked_to]
        if len(is_speaker) > 0 and len(is_speaked_to) > 0:
            return is_speaker, is_speaked_to
        else:
            return None
    else:
        is_speaker = [x for x in lower_characters if x in speaker]
        is_speaked_to = [x for x in lower_characters if x in speaked_to]
        if len(is_speaker) > 0 and len(is_speaked_to) > 0:
            return is_speaker, is_speaked_to
        else:
            return None


def wc_matrix(args):
    matrix = args.characters
    if not isinstance(matrix, list):
        raise Exception("Invalid character data")
    if len(matrix) < 2:
        raise Exception("A matrix needs at least two characters to make sense")
    print(f"wc matrix: [{' ✖ '.join(matrix)}]")
    file_paths = list(filter_files(args.only_movies))
    lower_matrix = list(map(lambda x: x.strip().lower(), matrix))

    class Matrix:
        def __init__(self):
            self.dict = {}

        def add(self, first: str, second: str, amt: int):
            self.dict.setdefault(first, dict())
            self.dict[first].setdefault(second, 0)
            self.dict[first][second] += amt

        def merge(self, other: Matrix):
            for other_1st_key in other:
                for other_2nd_key in other[other_1st_key]:
                    self.add(other_1st_key, other_2nd_key, other[other_1st_key][other_2nd_key])

        def __getitem__(self, item: str):
            return self.dict[item]

        def __iter__(self):
            return iter(self.dict)

        def __len__(self):
            return len(self.dict)

        def print(self, file_name: Optional[str] = None):
            if len(self) == 0:
                print("No such combinations found")
            elif file_name:
                for first_key in self:
                    speaker = first_key
                    for second_key in self[first_key]:
                        speaked_to = second_key
                        print(f'{file_name};{speaker};{speaked_to};{self[first_key][second_key]}')
            else:
                for first_key in self:
                    speaker = first_key
                    for second_key in self[first_key]:
                        speaked_to = second_key
                        print(f'{speaker};{speaked_to};{self[first_key][second_key]}')

    result_matrix = Matrix()
    for path in file_paths:
        sub_wc = Matrix()
        reader = csv.reader(path.open('r', encoding='UTF-8'))
        for line in reader:
            rs = are_characters_in_line(line, lower_matrix, matrix if not args.dont_resolve_groups else None, resolve_groups=not args.dont_resolve_groups)
            if rs:
                is_speaker = rs[0]
                is_speaked_to = rs[1]
                if not args.dont_resolve_groups:
                    for sp in is_speaker:
                        for spkd in is_speaked_to:
                            sub_wc.add(sp, spkd, count_words(line))
                else:
                    sub_wc.add(line[0], line[1], count_words(line))
        if args.only_movies or args.group_per_movie:
            if len(sub_wc) > 0:
                sub_wc.print(path.name)
        result_matrix.merge(sub_wc)

    if not args.group_per_movie:
        result_matrix.print()


def convert(args):
    import re
    format = args.format

    class Format:
        def __init__(self, format: str):
            self.raw_format = format
            self.replacers: OrderedDict[int, Format.Replace] = OrderedDict()
            self.placeholder: List[Optional[str]] = []
            self.__parse_raw_format()

        class Replace:
            def __init__(self, range: Tuple[int, int], quote: Optional[str]=None):
                self.range = range
                self.quote = quote

        def __parse_raw_format(self):
            found_matches = re.finditer(r'\$((?P<number>[0-9]+)|(?P<part_id>partId))', self.raw_format)
            any_found = False
            last_end = 0
            for match in found_matches:
                any_found = True
                matched_group_name = next(x[0] for x in match.groupdict().items() if x[1] is not None)
                rnge = match.span(0)
                if matched_group_name == 'number':
                    part_id = int(match.group(1))
                    if part_id not in range(1, 9):
                        raise Exception(f"Invalid column number {part_id} not in range <1-8>!")

                    # check for surrounding quotes for escaping in self.parse
                    quote = None
                    if self.raw_format[rnge[0]-1] == self.raw_format[rnge[1]]:
                        quote = self.raw_format[rnge[1]]

                    self.replacers[part_id] = self.Replace(rnge, quote)

                elif matched_group_name == 'part_id':
                    self.replacers["part_id"] = self.Replace(rnge)
                    pass
                self.placeholder.append(self.raw_format[last_end:rnge[0]])
                self.placeholder.append(None)
                last_end = rnge[1]

            self.placeholder.append(self.raw_format[last_end:])
            if not any_found:
                raise Exception("Invalid format. No column numbers, e.g. \"$1\" found!")

        def parse(self, line: List[str], file_name: str, mappings: Optional[Dict[str, str]] = None):
            new_line = self.placeholder
            i = -1
            for key in self.replacers:
                i += 2
                if key == 'part_id':
                    value = str(file_names.index(file_name) + 1)
                else:
                    quote = self.replacers[key].quote
                    value = line[key-1]
                    if quote:
                        if args.auto_escape:
                            value = value.translate(str.maketrans({quote: f"\\{quote}"}))
                        elif args.sql_escape:
                            value = value.translate(str.maketrans({"'": "''"}))
                    if mappings:
                        if value in mappings:
                            value = mappings[value]
                new_line[i] = value
            return ''.join(new_line)
    file_paths = list(filter_files(args.only_movies))
    print(f'Format: "{format}"; files: {[x.name for x in file_paths]}')
    format = Format(format)

    mappings = None
    characters = None
    lower_characters = None
    if args.characters:
        characters = args.characters
        enum_characters = enumerate(characters)
        is_found_equal_sign = next(((i, x) for i, x in enum_characters if '=' in x), None)
        if is_found_equal_sign:
            i = is_found_equal_sign[0]
            x = is_found_equal_sign[1]
            orig, new = x.split('=')
            mappings = dict()
            mappings[orig] = new
            characters[i] = orig
            for i, x in enum_characters:
                if '=' in x:
                    orig, new = x.split('=')
                    mappings[orig] = new
                    characters[i] = orig

        lower_characters = list(map(lambda x: x.strip().lower(), args.characters))

    for path in file_paths:
        reader = csv.reader(path.open('r', encoding='UTF-8'))
        if args.group_per_movie:
            print(f'{path.name}:')
        if args.characters:
            for line in reader:
                rs = are_characters_in_line(
                    line,
                    lower_characters,
                    characters if not args.dont_resolve_groups else None,
                    resolve_groups=not args.dont_resolve_groups
                )
                if rs:
                    is_speaker = rs[0]
                    is_speaked_to = rs[1]
                    # losing info about groups right now
                    line[0] = is_speaker[0]
                    line[1] = is_speaked_to[0]
                    new_line = format.parse(line, path.name, mappings)
                    print(new_line)
        else:
            for line in reader:
                new_line = format.parse(line, path.name, mappings)
        if args.group_per_movie:
            print('\n')


if __name__ == "__main__":
    if not DATA.exists():
        raise Exception("Data folder does not exist")
    parser = argparse.ArgumentParser(
        description="stats about LA Times data"
    )
    subparsers = parser.add_subparsers(
        dest='subparser_name',
        help="following commands available"
    )

    word_count_parser = subparsers.add_parser(
        "word_count",
        help="count words",
        aliases=["wc"]
    )
    word_count_parser.add_argument(
        "--only-movies", "-f",
        nargs="*",
        default=None,
        type=int,
        choices=range(1, 9),
        help="Only which movies"
    )
    word_count_parser.add_argument(
        "character",
        type=str,
        help="Specify character, case-insensitive substring of CSV format!"
    )
    word_count_parser.set_defaults(func=wc)

    word_count_matrix_parser = subparsers.add_parser(
        "word_count_matrix",
        help="given a list of people create a matrix of word count spoken to each other",
        aliases=["wcm"]
    )
    word_count_matrix_parser.add_argument(
        "characters",
        type=str,
        nargs="+",
        help="Specify character, case-insensitive substring of CSV format!"
    )
    word_count_matrix_parser.add_argument(
        "--only-movies", "-f",
        nargs="*",
        default=None,
        type=int,
        choices=range(1, 9),
        help="Only which movies"
    )
    word_count_matrix_parser.add_argument(
        "--dont-resolve-groups", "--drg",
        action='store_const',
        const=True,
        help="Leave speaking to groups as is"
    )

    word_count_matrix_parser.add_argument(
        "--group-per-movie", "--gpm",
        action='store_const',
        const=True,
        help="Add another level to matrix by dividing the data for each movie separately"
    )

    word_count_matrix_parser.set_defaults(func=wc_matrix)

    convert_to_format_parser = subparsers.add_parser(
        "convert",
        help="convert to a format specified by you",
        aliases=["cvrt"]
    )
    convert_to_format_parser.add_argument(
        "format",
        type=str,
        help='Specify the given format, e.g. "($1,$2,$3,$4)" '
             'where commas and parentheses are left as is, but $1, $2 etc. '
             'are replaced with the given column numbers.'
             'Indexing starts at 1!'
             'You also have variables: $partId'
    )
    convert_to_format_parser.add_argument(
        "--only-movies", "-f",
        nargs="*",
        default=None,
        type=int,
        choices=range(1, 9),
        help="Only which movies"
    )
    # convert_to_format_parser.add_argument(
    #     "--output", "-o",
    #     nargs="?",
    #     default=None,
    #     required=False,
    #     help="Specify to write to file, if group per movie then multiple files"
    # )
    convert_to_format_parser.add_argument(
        "--group-per-movie", "--gpm",
        action='store_const',
        const=True,
        help="Group per movie"
    )
    convert_to_format_parser.add_argument(
        "--characters", "-c",
        nargs="*",
        help="Filter characters, case-insensitive substring of CSV format!"
    )
    convert_to_format_parser.add_argument(
        "--dont-resolve-groups", "--drg",
        action='store_const',
        const=True,
        help="Leave speaking to groups as is"
    )
    escape_group = convert_to_format_parser.add_mutually_exclusive_group()
    escape_group.add_argument(
        "--auto-escape", "--ae",
        action='store_const',
        const=True,
        help="Escape non-partid variabels if they're surrounded by the same characters on both sides"
    )
    escape_group.add_argument(
        "--sql-escape", "--se",
        action='store_const',
        const=True,
        help="Use '' instead of \\' to escape '"
    )

    convert_to_format_parser.set_defaults(func=convert)

    args = parser.parse_args()
    if args.subparser_name:
        args.func(args)
    else:
        parser.print_help()
        print(f"\nSupply a command!")
