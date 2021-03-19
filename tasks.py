""" `invoke` tasks used to make and quality-check this article. """

import pathlib
import re
import subprocess
import sys
from collections import Counter
from difflib import SequenceMatcher

from invoke import task

import known


@task
def compile(c, engine="xelatex"):
    """ Compile the LaTeX document. """

    c.run(f"latexmk writting/Long_text.tex")


@task
def spellcheck(c):
    """
    Check spelling
    """

    book = list(pathlib.Path().glob("**/*.tex"))
    exit_codes = [0]
    for path in book:
        latex = path.read_text()
        aspell_output = subprocess.check_output(
            ["aspell", "-t", "--list", "--lang=en_GB"], input=latex, text=True
        )
        incorrect_words = set(aspell_output.split("\n")) - {""} - known.words
        if len(incorrect_words) > 0:
            print(f"In {path} the following words are not known: ")
            for string in sorted(incorrect_words):
                print(string)
            exit_codes.append(1)
    sys.exit(max(exit_codes))


