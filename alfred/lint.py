import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
SRC_PATH = os.path.realpath(os.path.join(ROOT_DIR, "src", "alfred"))


@alfred.command('lint', help="validate the source code using pylint")
@alfred.option('-v', '--verbose', is_flag=True, default=False)
def lint(verbose: bool):
    if verbose is False:
        alfred.run('pylint src/alfred')
    else:
        alfred.run('pylint --verbose --reports y src/alfred')


@alfred.command('alfred_check', help="validate that the project's alfred commands are functional")
def alfred_check():
    """
    checks that the project's alfred commands are functional
    """
    alfred.invoke_itself(['--check'])
