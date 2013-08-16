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

print '2. Bump version in package.json and create tag. If you have any uncommitted changes, this will exit immediately. Commit and then re-run this file.'

call('npm', 'version', 'patch')

# alternatively, manually set the new version number and then run:
# import filesequence
# call('git', 'tag', '-a', 'v' + filesequence.__version__, '-m', filesequence.__version__)

print '3. Reinstall as the new version'

call('python', 'setup.py', 'develop')

print '4. Push (Github will automatically prepare the static version, if needed)'

call('git', 'push')

print '5. Publish (will be on PyPI, but not every setuptools incarnation will be able to get to it)'

call('python', 'setup.py', 'register')

print '6. Upload source distribution (which allows some of the older distutils / setuptools distribution to install it)'

call('python', 'setup.py', 'sdist', 'upload')

print '7. Check PyPI simple at https://pypi.python.org/simple/filesequence/ to ensure this package was uploaded'
