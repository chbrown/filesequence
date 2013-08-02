import os.path
import itertools
from filesequence import version

__version__ = version.__version__

# I want to export an 'open' function, but can't without overwriting the builtin
# global 'open', which I need for my own purposes. So, alias it here to 'builtin_open'.
builtin_open = open


class FileSequence(object):
    # `_current_file` is a file descriptor, set to None if it is not open
    _current_file = None
    # `_current_file_bytes` is the position we are at in `_current_file`
    _current_file_bytes = 0

    def __init__(self, filenames, limit, flag='w'):
        '''
        Initialize a new file_sequence object.

        filenames -- an iterable of filenames
        limit -- each file will contain stricly less than `limit` bytes
        flag -- can be 'r', 'r+', 'w', 'w+', 'a', or 'a+'

        TODO: currently only flags 'w' and 'a' are supported.
        '''
        if flag in ['r', 'r+']:
            msg = 'FileSequence is currently write/append-only'
            raise NotImplemented(msg)

        # coerce filenames into an iterator, so that we consume items permanently
        self.filenames = iter(filenames)
        self.limit = limit
        self.flag = flag

        if flag in ['a', 'a+']:
            # seek to the end of the data, the last existing file in the
            # sequence. If there are no files, self._current_index should be
            # None, meaning the next time we need to write, it should create
            # a new file.
            last_existing_filename = []
            for filename in self.filenames:
                if os.path.exists(filename):
                    last_existing_filename = [filename]
                else:
                    break
            # backtrack: push the latest unused value (the unopened file) back onto our filenames,
            #   as well as the file that demonstrated that it did not exist.
            # itertools.chain simply iterates through its iterable arguments, flattening
            self.filenames = itertools.chain(last_existing_filename + [filename], self.filenames)

    def __enter__(self):
        self.advance()
        return self

    def __exit__(self, type, value, traceback):
        # close the current file if there is one
        if self._current_file:
            self._current_file.close()

    def advance(self):
        # close the current file if there is one
        if self._current_file:
            self._current_file.close()

        # open the next file, possibly the first
        self._current_file = builtin_open(self.filenames.next(), self.flag)
        # get the position in the current file, possibly 0
        self._current_file_bytes = self._current_file.tell()

    def write(self, line):
        '''Line must be a string.'''
        line_len = len(line)
        if self._current_file_bytes + line_len > self.limit:
            # flush current file and start new one
            self.advance()

        self._current_file.write(line)
        self._current_file_bytes += line_len

    def tail(self, n=10):
        '''
        Just a little helper function to get the last few lines from the current file.
        Does not rewind into previous files.
        '''
        lines = []
        if self._current_file:
            # go to the beginning, in case we have _really_ long lines
            self._current_file.seek(0, 0)
            # just read everything into a list and take the last n. Not very efficient, but easy.
            lines = list(self._current_file)[-n:]
            # return whence we came from
            self._current_file.seek(self._current_file_bytes, 0)
        return lines


def open(*args, **kw):
    return FileSequence(*args, **kw)


def interpolator(pattern, indices):
    for index in indices:
        yield pattern % index


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Split STDIN into a sequence of files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--limit', type=int, default=50000000,
        help='Maximum bytes per file')
    parser.add_argument('--pattern', type=str, default='split.%02d',
        help='Filename string pattern: generate filenames in sequence by interpolating `pattern %% indices.next()`')
    parser.add_argument('--version', action='version', version=__version__)
    opts = parser.parse_args()

    filenames = interpolator(opts.pattern, xrange(1000))

    if sys.stdin.isatty():
        raise IOError('You must provide input via STDIN')

    with FileSequence(filenames, opts.limit) as output:
        for line in sys.stdin:
            output.write(line)
