import string
from collections import namedtuple
from enum import Enum

from lcc.general_parser import GeneralParser


Kind = Enum('Kind', 'left_paren, right_paren, left_bracket, right_bracket, arrow, equals, name, eof')

Token = namedtuple('Token', 'text, kind')

SINGLES = {
    '(': Kind.left_paren,
    ')': Kind.right_paren,
    '[': Kind.left_bracket,
    ']': Kind.right_bracket,
    '>': Kind.arrow,
    '=': Kind.equals,
}


EOF_TOKEN = Token('<EOF_TOKEN>', Kind.eof)


class Lexer(GeneralParser):
    def next_token(self):
        while not self.current_is_eof() and self.current.isspace():
            self.consume()

        if self.current_is_eof():
            return EOF_TOKEN

        for single_char, kind in SINGLES.items():
            if self.current == single_char:
                self.consume()
                return Token(single_char, kind)

        if self.current_is_a_valid_char_for_a_name():
            chars = []
            while not self.current_is_eof() and self.current_is_a_valid_char_for_a_name():
                chars.append(self.consume())

            text = ''.join(chars)
            return Token(text, Kind.name)

    def current_is_a_valid_char_for_a_name(self):
        return self.current in string.ascii_lowercase

    def __iter__(self):
        token = self.next_token()
        while not token == EOF_TOKEN:
            yield token
            token = self.next_token()
