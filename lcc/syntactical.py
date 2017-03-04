from lcc import lexical
from lcc.ast import Program, Variable, Application, Literal
from lcc.general_parser import GeneralParser
from lcc.lexical import Kind
from lcc.utils import LccError


class Parser(GeneralParser):
    def __init__(self, tokens):
        super().__init__(tokens, eof=lexical.EOF_TOKEN)
        self.declarations = dict()
        self.main_expression = None

    def parse_program(self):
        if self.current_kind_is(Kind.name):
            name = self.consume()
            if self.current_kind_is(Kind.equals):
                self.consume()
                declaration_value = self.consume_expression()
                self.declarations[name.text] = declaration_value
                self.parse_program()
            else:
                self.main_expression = self.consume_expression_that_starts_with_a_name(name)
        else:
            self.main_expression = self.consume_expression()

        self.ensure_kind(Kind.eof)
        return Program(self.declarations, self.main_expression)

    def current_kind_is(self, kind):
        return self.current.kind == kind

    def consume_expression(self):
        if self.current_kind_is(Kind.name):
            name = self.consume()
            expression = self.consume_expression_that_starts_with_a_name(name)
        elif self.current_kind_is(Kind.left_paren):
            self.consume()
            expression = self.consume_expression()
            self.ensure_kind(Kind.right_paren)
        else:
            raise LccError('Unexpected token {}'.format(self.current))

        if self.current_kind_is(Kind.left_bracket):
            self.consume()
            argument = self.consume_expression()
            self.ensure_kind(Kind.right_bracket)
            return Application(expression, argument)
        else:
            return expression

    def ensure_kind(self, kind):
        self.ensure(lambda token: token.kind == kind)

    def consume_expression_that_starts_with_a_name(self, name):
        variable = Variable(name.text)
        if self.current_kind_is(Kind.arrow):
            self.consume()
            body = self.consume_expression()
            return Literal(variable, body)
        else:
            return variable
