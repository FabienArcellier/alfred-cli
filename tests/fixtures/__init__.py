import os
import shutil
import tempfile

from contextlib import contextmanager

SCRIPT_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))


@contextmanager
def clone_fixture(fixture_name, working_dir=None):
  tmp_prefix = '{0}_{1}'.format(fixture_name, '_')
  working_directory = tempfile.mktemp(prefix=tmp_prefix) if not working_dir else working_dir
  template_working_directory = os.path.join(SCRIPT_DIRECTORY_PATH, fixture_name)

  if not os.path.isdir(template_working_directory):
    fixtures_list = [d for d in os.listdir(SCRIPT_DIRECTORY_PATH) if
                        os.path.isdir(os.path.join(SCRIPT_DIRECTORY_PATH, d))]
    raise Exception('the fixture {0} does not exists in fixtures : {1}'.format(fixture_name, fixtures_list))

  previous_working_dir = os.getcwd()
  shutil.copytree(template_working_directory, working_directory)
  try:
    os.chdir(working_directory)
    yield working_directory
  finally:
    os.chdir(previous_working_dir)
    shutil.rmtree(working_directory)
