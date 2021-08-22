import os

import click
import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
TESTS_PATH = os.path.realpath(os.path.join(ROOT_DIR, "tests"))


@alfred.command(click, 'tests', help="validate alfred with unit testing")
def tests():
    alfred.invoke_command(tests_units)
    alfred.invoke_command(tests_acceptances)


@alfred.command(click, 'tests:units', help="validate alfred with unit testing")
@click.option('-v', '--verbose', is_flag=True)
def tests_units(verbose: bool):
    python = alfred.sh('python')
    os.chdir(TESTS_PATH)
    args = ['-m', 'unittest', 'discover', 'units']

    if verbose:
        args.append('-v')

    if args:
        alfred.run(python, args)


@alfred.command(click, 'tests:acceptances', help="validate alfred with acceptances testing")
@click.option('-v', '--verbose', is_flag=True)
def tests_acceptances(verbose: bool):
    python = alfred.sh('python')
    os.chdir(TESTS_PATH)
    args = ['-m', 'unittest', 'discover', 'acceptances']

    if verbose:
        args.append('-v')

    if args:
        alfred.run(python, args)
