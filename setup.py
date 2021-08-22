from setuptools import setup
from setuptools import find_packages

setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Console"
    ],
    extras_require={
        'dev': [
            'decorator',
            'pylint',
            'coverage',
            'twine'
        ]
    },
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': [
            'alfred = alfred.cli:cli',
        ],
    },
    include_package_data=True,
    install_requires = [
        "click",
        "plumbum",
        "PyYAML"
    ],
    name='pyalfred',
    package_dir={'': 'src'},
    package_data={
        'resources': ['src/alfred/resources/*'],
    },
    packages=find_packages(where="src", exclude=["tests.*", "tests"]),
    version='1.0.0'
)
