import os
import venv
import plumbum
from alfred.os import is_windows

venv1_path = os.path.realpath(os.path.join(os.getcwd(), 'products', 'product1', '.venv'))
venv.create(venv1_path)


root_dir = os.path.realpath(os.path.join(__file__, '..', '..', '..', '..', '..'))

if is_windows():
    python_venv = plumbum.local[os.path.join(venv1_path, 'Scripts', 'python.exe')]
else:
    python_venv = plumbum.local[os.path.join(venv1_path, 'bin', 'python')]

curl_cmd = plumbum.local['curl']
install_pip = curl_cmd["-sS", "https://bootstrap.pypa.io/get-pip.py"] | python_venv
install_pip()
python_venv['-m', 'pip', 'install', '--upgrade', root_dir]()
