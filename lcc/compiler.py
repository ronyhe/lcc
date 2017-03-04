from lcc import lexical, syntactical


def run_compile(source_text):
    lexer = lexical.Lexer(source_text)
    parser = syntactical.Parser(lexer)
    program = parser.parse_program()
    program.validate_free_variables()
    python = program.to_python()
    return python
