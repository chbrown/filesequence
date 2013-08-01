from setuptools import setup

__version__ = 'N/A'
execfile('filesequence/version.py')  # overwrites __version__ global

setup(
    name='filesequence',
    version=__version__,
    description='Write to an indexed sequence of files using the standard Python file API',
    long_description=open('.README.rst').read(),
    license=open('LICENSE').read(),
    author='Christopher Brown',
    author_email='io@henrian.com',
    url='https://github.com/chbrown/filesequence',
    packages=['filesequence'],
    package_dir={
        'filesequence': 'filesequence'
    },
    package_data={
        '': ['LICENSE']
    },
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'filesequence = filesequence:main',
        ],
    },
    zip_safe=True,
)
