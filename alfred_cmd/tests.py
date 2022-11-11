import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
TESTS_PATH = os.path.realpath(os.path.join(ROOT_DIR, "tests"))


@alfred.command('tests', help="validate alfred with all the automatic testing")
@alfred.option('-v', '--verbose', is_flag=True)
def tests(verbose: bool):
    alfred.invoke_command('tests:units', verbose=verbose)
    alfred.invoke_command('tests:acceptances', verbose=verbose)


@alfred.command('tests:units', help="validate alfred with unit testing")
@alfred.option('-v', '--verbose', is_flag=True)
def tests_units(verbose: bool):
    python = alfred.sh('python')
    args = ['-m', 'unittest', 'discover', 'tests/units']

    if verbose:
        args.append('-v')

    if args:
        alfred.run(python, args)


@alfred.command('tests:acceptances', help="validate alfred with acceptances testing")
@alfred.option('-v', '--verbose', is_flag=True)
def tests_acceptances(verbose: bool):
    python = alfred.sh('python')
    args = ['-m', 'unittest', 'discover', 'tests/acceptances']

    if verbose:
        args.append('-v')

    if args:
        alfred.run(python, args)
