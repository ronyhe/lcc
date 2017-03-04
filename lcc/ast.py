from collections import namedtuple

from lcc.utils import LccError


class UnboundVariableError(LccError):
    pass


# noinspection PyClassHasNoInit
class Program(namedtuple('Program', 'declarations, main_expression')):
    def validate_free_variables(self):
        prebound_variables = {key for key in self.declarations.keys()}
        for name, expression in self.declarations.items():
            try:
                expression.validate_free_variables(prebound_variables)
            except UnboundVariableError as unbound:
                raise UnboundVariableError('Problem at declaration of "{}": {}'.format(name, str(unbound)))

        self.main_expression.validate_free_variables(prebound_variables)

    def to_python(self):
        lines = []
        for name, expression in self.declarations.items():
            line = '{} = {}'.format(name, expression.to_python())
            lines.append(line)
        lines.append('')
        lines.append('')
        lines.append('if __name__ == "__main__":')
        main = '    ' + self.main_expression.to_python().replace('\n', '\n    ')
        lines.append(main)
        return '\n'.join(lines)


# noinspection PyClassHasNoInit
class Application(namedtuple('Application', 'target, argument')):
    def validate_free_variables(self, already_bound_names):
        self.target.validate_free_variables(already_bound_names)
        self.argument.validate_free_variables(already_bound_names)

    def to_python(self):
        target, argument = self
        return '({})({})'.format(target.to_python(), argument.to_python())


# noinspection PyClassHasNoInit
class Literal(namedtuple('Literal', 'argument, body')):
    def validate_free_variables(self, already_bound_names):
        new_names = already_bound_names.union({self.argument.name})
        self.body.validate_free_variables(new_names)

    def to_python(self):
        argument, body = self
        return 'lambda {}: ({})'.format(argument.to_python(), body.to_python())


# noinspection PyClassHasNoInit
class Variable(namedtuple('Value', 'name')):
    def validate_free_variables(self, already_bound_names):
        name = self.name
        if name not in already_bound_names:
            raise UnboundVariableError('Unbound variable "{}"'.format(name))

    def to_python(self):
        return self.name
