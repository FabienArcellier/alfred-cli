import alfred


@alfred.command('ci', help="execute continuous integration process")
@alfred.option('-v', '--verbose', is_flag=True)
def ci(verbose: bool):
    alfred.invoke_command('lint', verbose=verbose)
    alfred.invoke_command('tests', verbose=verbose)
