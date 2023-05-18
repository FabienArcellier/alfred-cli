import alfred


@alfred.command('hello')
def hello():
    hello = alfred.sh('hello', 'hello is missing')
    alfred.run(hello, [])

