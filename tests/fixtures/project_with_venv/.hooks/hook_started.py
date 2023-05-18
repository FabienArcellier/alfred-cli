import os
import venv
import plumbum

from alfred.interpreter import venv_python_path

venv1_path = os.path.realpath(os.path.join(os.getcwd(), '.venv'))
venv.create(venv1_path)

python_venv_path = venv_python_path(venv1_path)
python_venv = plumbum.local[python_venv_path]
curl_cmd = plumbum.local['curl']
install_pip = curl_cmd["-sS", "https://bootstrap.pypa.io/get-pip.py"] | python_venv
install_pip()
