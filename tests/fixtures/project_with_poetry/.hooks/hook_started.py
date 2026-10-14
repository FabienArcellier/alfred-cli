import os
import shutil
import subprocess

poetry_path = shutil.which('poetry')
env = dict(os.environ)
env.pop('VIRTUAL_ENV', None)
subprocess.run([poetry_path, 'install'], cwd=os.getcwd(), stdout=None, stderr=None, env=env)
