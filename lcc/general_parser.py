from lcc.utils import LccError


class _EofClass:
    def __str__(self):
        return '<EOF Object>'
_EOF = _EofClass()


class GeneralParser:
    """ A base class for parsers.

    This class yields the provided eof when the inputs are exhausted,
    so using it as an iterator might loop indefinitely.
    This class does not assume the items being parsed are text characters.
    """
    def __init__(self, inputs, eof=_EOF):
        self.eof = eof
        self._inputs = iter(inputs)
        self._advance()

    def consume(self):
        current = self.current
        self._advance()

        return current

    def _advance(self):
        try:
            self.current = next(self._inputs)
        except StopIteration:
            self.current = self.eof

    def ensure(self, predicate, message=None):
        current = self.current

        try:
            valid = predicate(current)
        except TypeError:
            valid = current == predicate

        if valid:
            self.consume()
            return current
        else:
            try:
                actual_message = message(current)
            except TypeError:
                if message is None:
                    actual_message = '{} does not comply with the supplied predicate'.format(current)
                else:
                    actual_message = message
            raise LccError(actual_message)

    def current_is_eof(self):
        return self.current == self.eof
