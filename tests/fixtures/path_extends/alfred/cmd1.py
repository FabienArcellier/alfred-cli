import io

import alfred


@alfred.command("hello_world")
def hello_world_command():
    hello = alfred.sh("hello")
    alfred.run(hello)

    with io.open("hello.log", "r", encoding='utf-8') as filep:
        print(filep.read())
