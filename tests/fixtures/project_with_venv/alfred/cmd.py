import alfred


@alfred.command('hello')
def hello():
    cowsay = alfred.sh(['cowsay', 'cowsay.exe'], 'cowsay is missing')
    alfred.run(cowsay, ["hello"])

