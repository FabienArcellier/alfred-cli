from setuptools import setup
from setuptools import find_packages

setup(
    name='pyalfred',
    version='1.0.0',
    packages=find_packages(exclude=["*_tests.*", "*_tests"]),
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': [
            'alfred = alfred.cli:cli',
        ],
    },
    install_requires = [
        "click"
    ],
    extras_require={
        'dev': [
            'pylint',
            'coverage',
            'twine'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Console"
    ]
)
