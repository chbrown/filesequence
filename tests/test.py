import os
import random
import shutil
import tempfile
import subprocess

import filesequence


here = os.path.dirname(__file__) or os.curdir
cli_filepath = os.path.join(here, '..', 'filesequence', 'cli.py')


class Tempdir():
    def __init__(self, name=None):
        if name is None:
            name = 'tmp-%d' % random.randrange(1000000)
        self.path = os.path.join(tempfile.gettempdir(), name)
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def __enter__(self):
        # pushd
        self.previous_wd = os.getcwd()
        os.chdir(self.path)
        return self

    def __exit__(self, type, value, traceback):
        # clean up
        shutil.rmtree(self.path)
        # popd
        os.chdir(self.previous_wd)


def test_randoms(N=100000, limit=1000000):
    '''Generating random integers'''

    filenames = [
        'randint-01.txt',
        'randint-02.txt',
        'randint-03.txt',
        'randint-04.txt',
        'randint-05.txt',
        'randint-06.txt',
        'randint-07.txt',
        'randint-08.txt',
        'randint-09.txt']

    with Tempdir():
        with filesequence.FileSequence(filenames, limit, 'w') as output:
            for line in xrange(N):
                integer = random.randint(0, 1e64)
                output.write(str(line) + '\t' + str(integer) + '\n')

        output_filenames = os.listdir('.')
        assert len(output_filenames) == 8, '%d randoms should only take eight files' % N
        for filename in output_filenames:
            assert os.path.getsize(filename) <= limit, 'File should be less than %d bytes' % limit


def test_append(N=100000, limit=1000000):
    '''Generating random integers in two sequences'''

    filenames = ['randint-%02d.txt' % i for i in range(100)]

    with Tempdir():
        with filesequence.FileSequence(filenames, limit, 'w') as output:
            for line in xrange(N / 2):
                integer = random.randint(0, 1e64)
                output.write(str(line) + '\t' + str(integer) + '\n')

        print 'First pass done'
        for filename in os.listdir('.'):
            print filename, os.path.getsize(filename)

        with filesequence.FileSequence(filenames, limit, 'a') as output:
            for line in xrange(N / 2, N):
                integer = random.randint(0, 1e64)
                output.write(str(line) + '\t' + str(integer) + '\n')

        print 'Second pass done'
        for filename in os.listdir('.'):
            print filename, os.path.getsize(filename)

        output_filenames = os.listdir('.')
        assert len(output_filenames) == 8, '%d randoms should only take eight files' % N
        for filename in output_filenames:
            assert os.path.getsize(filename) <= limit, 'File should be less than %d bytes' % limit


def test_mobydick_write(limit=1000):
    '''Calling filesequence with subprocess'''
    input_file = open(os.path.join(here, 'mobydick.txt'), 'r')

    with Tempdir():
        # print 'Using tempdir:', dirpath
        subprocess.check_call(['python', cli_filepath,
            '--limit', str(limit),
            '--pattern', 'mobydick.part%02d'], stdin=input_file)

        filenames = os.listdir('.')
        assert 12 < len(filenames) <= 14, '1kb splits should take 13--14 files.'
        for filename in filenames:
            assert os.path.getsize(filename) <= limit, '%s should be less than %d bytes' % (filename, limit)
