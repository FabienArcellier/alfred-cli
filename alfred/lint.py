import os

import click

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
SRC_PATH = os.path.realpath(os.path.join(ROOT_DIR, "src"))


@alfred.command(click, 'lint', help="execute pylint validation over source code")
@click.option('-v', '--verbose', is_flag=True)
def lint(verbose: bool):
    python = alfred.sh('pylint', "pylint is not installed")
    os.chdir(ROOT_DIR)
    args = []

    if verbose:
        args.append('-v')

    args.append('src/alfred')

    if args:
        alfred.run(python, args)
