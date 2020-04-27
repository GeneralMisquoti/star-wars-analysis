from __future__ import annotations

import argparse
from utils import file_names
from pathlib import Path
import csv
from typing import List, Optional
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
            if file_name:
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
            speaker = line[0].strip().lower()
            speaked_to = line[1].strip().lower()
            if not args.dont_resolve_groups:
                is_speaker = [matrix[i] for i, x in enumerate(lower_matrix) if x in speaker]
                is_speaked_to = [matrix[i] for i, x in enumerate(lower_matrix) if x in speaked_to]
                if len(is_speaker) > 0 and len(is_speaked_to) > 0:
                    for sp in is_speaker:
                        for spkd in is_speaked_to:
                            sub_wc.add(sp, spkd, count_words(line))
            else:
                is_speaker = [x for x in lower_matrix if x in speaker]
                is_speaked_to = [x for x in lower_matrix if x in speaked_to]
                if len(is_speaker) > 0 and len(is_speaked_to) > 0:
                    sub_wc.add(line[0], line[1], count_words(line))
        if args.only_movies:
            if len(sub_wc) > 0:
                sub_wc.print(path.name)
            else:
                for i, first in enumerate(matrix)[:-1]:
                    for second in matrix[i+1:]:
                        print(f'{path.name};{first};{second};0')
        result_matrix.merge(sub_wc)

    result_matrix.print()


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
        "--dont-resolve-groups",
        action='store_const',
        const=True,
        help="Leave speaking to groups as is"
    )
    word_count_matrix_parser.set_defaults(func=wc_matrix)

    args = parser.parse_args()
    if args.subparser_name:
        args.func(args)
    else:
        parser.print_help()
        print(f"\nSupply a command!")
