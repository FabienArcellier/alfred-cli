import multiprocessing
import os

import fixtup

import alfred


def test_alfred_project_directory_should_return_the_directory_that_contains_alfred_yml():
    with fixtup.up("project"):
        wd = os.getcwd()
        os.chdir(os.path.join(wd, "alfred"))

        assert alfred.project_directory() == wd


def test_env_should_inject_environment_variable_in_subprocess():
    def task(queue):
        queue.put(0 if os.getenv("RANDOMVALUE") == "prod" else 1)

    with alfred.env(RANDOMVALUE="prod"):
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=task, args=(queue,))
        process.start()
        process.join()
        assert_result = queue.get()
        assert assert_result == 0


def test_env_should_inject_environment_variable_in_sh_invocation():
    with alfred.env(RANDOMVALUE="prod"):
        sh = alfred.sh("bash")
        result = sh.run(["-c", "echo $RANDOMVALUE"])
        assert result[1] == "prod\n"


def test_env_should_release_environment_variable_after_context():
    with alfred.env(RANDOMVALUE="prod"):
        pass

    assert "ENV" not in os.environ

