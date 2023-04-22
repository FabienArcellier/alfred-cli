import os

import alfred


@alfred.command('docs:html', help="build documentation in html format")
def docs_html():
    make = alfred.sh('make')
    directory = alfred.project_directory()
    os.chdir(os.path.join(directory, 'docs'))
    alfred.run(make, 'html')
