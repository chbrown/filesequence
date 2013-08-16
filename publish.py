import sys
import subprocess

noop = '-n' in sys.argv


def call(*args):
    print '\n    ' + ' '.join(args) + '\n'
    if not noop:
        returncode = subprocess.call(args)
        if returncode:
            print 'system call failed, exiting'
            exit(returncode)


print "1. Convert latest README Markdown to reStructuredText, because PyPI can't handle anything but reStructuredText"

call('pandoc', 'README.md', '-o', 'README.rst')

print '2. Commit your (staged) changes'

call('git', 'commit')

print '3. Increase version in package.json'

call('npm', 'version', 'patch')

print '4. Reinstall as the new version'

call('python', 'setup.py', 'develop')

print '5. Tag latest'

import filesequence
call('git', 'tag', '-a', 'v' + filesequence.__version__, '-m', filesequence.__version__)

print '6. Push (Github will automatically prepare the static version, if needed)'

call('git', 'push')

print '7. Publish (will be on PyPI, but not every setuptools incarnation will be able to get to it)'

call('python', 'setup.py', 'register')

print '8. Upload source distribution (which allows some of the older distutils / setuptools distribution to install it)'

call('python', 'setup.py', 'sdist', 'upload')

print '9. Check PyPI simple at https://pypi.python.org/simple/filesequence/ to ensure this package was uploaded'
