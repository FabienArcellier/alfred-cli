import os
import shutil
import subprocess

poetry_path = shutil.which('poetry')
subprocess.run([poetry_path, 'install'], cwd=os.getcwd(), stdout=None, stderr=None)
