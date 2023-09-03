import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
SRC_PATH = os.path.realpath(os.path.join(ROOT_DIR, "src", "alfred"))


@alfred.command('lint', help="validate the source code using pylint")
@alfred.option('-v', '--verbose', is_flag=True)
def lint(verbose: bool):
    pylint = alfred.sh('pylint', "pylint is not installed")
    os.chdir(ROOT_DIR)
    args = []

    if verbose:
        args.append('-v')
        args += ['-r', 'y']

    args.append(SRC_PATH)

    if args:
        alfred.run(pylint, args)


@alfred.command('alfred_check', help="validate that the project's alfred commands are functional")
def alfred_check():
    """
    checks that the project's alfred commands are functional
    """
    alfred.invoke_itself(['--check'])
