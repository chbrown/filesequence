from setuptools import setup, find_packages
import json


def npm_to_setuptools(package):
    '''This is a one-off but could be refactored into some packaging helper.'''
    author = package.pop('author')
    # rename and collapse a few of the fields
    kw = dict(url=package.pop('homepage'), author=author['name'], author_email=author['email'])
    # don't use license or repository values from the package.json spec
    kw.update((key, str(value)) for key, value in package.items() if key not in ['license', 'repository'])
    return kw

package = json.load(open('package.json'))
kw = npm_to_setuptools(package)

setup(
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'filesequence = filesequence.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Filesystems',
        'Topic :: Text Processing :: General',
    ],
    tests_require=[
        'nose',
    ],
    test_suite='nose.collector',
    **kw
)
