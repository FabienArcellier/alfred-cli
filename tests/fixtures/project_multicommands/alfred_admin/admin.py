import alfred


@alfred.command("admin")
@alfred.option("--name")
def admin_command(name):
    print(f"hello world, {name}")
