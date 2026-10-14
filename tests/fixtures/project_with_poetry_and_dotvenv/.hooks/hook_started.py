import os
import shutil
import subprocess
import sys
import venv

# a project-local virtual environment that the dotvenv plugin detects
venv.create(os.path.join(os.getcwd(), '.venv'), with_pip=False)

# the poetry virtual environment is created in the cache (see poetry.toml in-project = false)
# so that poetry resolves to a path different from the project-local .venv
poetry_path = shutil.which('poetry')
env = dict(os.environ)
env.pop('VIRTUAL_ENV', None)
subprocess.run([poetry_path, 'env', 'use', sys.executable], cwd=os.getcwd(), stdout=None, stderr=None, env=env)
