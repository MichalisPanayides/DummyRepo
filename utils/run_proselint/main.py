import pathlib
import subprocess
import sys

import proselint


def get_root_path():
    return pathlib.Path(__file__).absolute().parent.parent.parent


known_exceptions = {}

suggestions_to_ignore = {}

root = get_root_path()
exit_code = 0
for markdown_file_path in filter(
    lambda path: ".ipynb_checkpoints" not in str(path), root.glob("**/*tex")
):

    markdown = markdown_file_path.read_text()
    exceptions = known_exceptions.get(markdown_file_path.parent.name, set(()))

    for exception in exceptions:
        markdown = markdown.replace(markdown, exception)

    suggestions = proselint.tools.lint(markdown)
    ignored_suggestions = suggestions_to_ignore.get(
        markdown_file_path.parent.name, set(())
    )
    for suggestion in filter(
        lambda suggestion: suggestion[0] not in ignored_suggestions, suggestions
    ):
        print("Proselint suggests the following:")
        print(suggestion)
        exit_code = 1

sys.exit(exit_code)
