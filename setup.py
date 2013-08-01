from setuptools import setup

setup(
    name='filesequence',
    version='0.1.1',
    description='Python HTTP for Humans.',
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    author='Christopher Brown',
    author_email='io@henrian.com',
    url='https://github.com/chbrown/filesequence',
    packages=['filesequence'],
    package_dir={
        'filesequence': 'filesequence'
    },
    package_data={
        None: ['LICENSE']
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
