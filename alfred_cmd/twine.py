import os
import shutil

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
DIST_PATH = os.path.realpath(os.path.join(ROOT_DIR, "dist"))


@alfred.command('twine', help="push the package to pypi")
def twine():
    twine = alfred.sh('twine', "twine is not installed")

    alfred.invoke_command('dist')
    alfred.run(twine, ['upload', os.path.join(DIST_PATH, '*')])


@alfred.command('dist', help="build distributions for alfred in dist/")
def dist():
    python = alfred.sh('python', "python is not installed")
    os.chdir(ROOT_DIR)
    if os.path.isdir(DIST_PATH):
        shutil.rmtree(DIST_PATH)

    alfred.run(python, ['setup.py', 'bdist_wheel', 'sdist'])
