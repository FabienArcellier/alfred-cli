import alfred


@alfred.command('ci', help="execute continuous integration process of alfred")
@alfred.option('-v', '--verbose', is_flag=True)
def ci(verbose: bool):
    alfred.invoke_command('alfred_check')
    if alfred.is_posix():
        alfred.invoke_command('lint', verbose=verbose)
    else:
        print("linter is not supported on non posix platform as windows")

    alfred.invoke_command('tests', verbose=verbose)


