LCC - A Lambda Calculus To Python Compiler

Lcc is a learning project, I got into it simply for fun and education.
It's a simple Lambda calculus compiler that emits python code.

The structure is as follows:
    - main.py is the command line interface. It accepts an input file and an optional output file.
    - main.py calls compiler.py to compile the code.
    - compiler.py tokenizes the text using lexical.py, it then parses the tokens using syntactical.py
    - compiler.py calls validation and emitting methods on the resulting ast.Program object.
    - ast.py is where the heavy lifting occurs, in the form of `to_python` methods, that emit python code,
      and `validate_free_variables` method that raise an error if unbound variables are present.

As stated, this is a learning project for me. I would love to learn even more from your contributions.
Feel free to comment, offer improvements and implement them.
Just to clarify, general code review is welcome, even if it's not directly related to the project's domain.

Here are some ideas of my own for enhancements:
    - Improve comments and documentation
    - Create and integrate a small standard library with natural numbers and a minimal text encoding
    - Use the aforementioned text encoding to create input and output for the resulting programs.

Thank you all in advance,
ronyhe