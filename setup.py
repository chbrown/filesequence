from setuptools import setup
# import os
# import sys

setup(
    name='filesequence',
    version='0.1.1',
    packages=['filesequence'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'filesequence = filesequence:main',
        ],
    },
    test_suite='tests',
)
