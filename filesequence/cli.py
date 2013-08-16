import os
import sys
import argparse
import filesequence


def main():
    if 'COLUMNS' not in os.environ:
        from subprocess import Popen, PIPE
        # stty size writes '<rows> <columms>' to standard out
        dims = Popen(['stty', 'size'], stdout=PIPE).stdout.read().split()
        os.environ['COLUMNS'] = dims[1]

    parser = argparse.ArgumentParser(description='Write STDIN into a sequence of files, splitting only at newlines',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--limit', type=int, default=50000000,
        help='Maximum bytes per file')
    parser.add_argument('--pattern', type=str, default='split.%02d',
        help='Filename string pattern: generate filenames in sequence by interpolating `pattern %% indices.next()`')
    parser.add_argument('--version', action='version', version=filesequence.__version__)
    opts = parser.parse_args()

    filenames = filesequence.interpolator(opts.pattern, xrange(1000))

    if sys.stdin.isatty():
        raise IOError('You must provide input via STDIN')

    with filesequence.FileSequence(filenames, opts.limit) as output:
        for line in sys.stdin:
            output.write(line)

if __name__ == '__main__':
    main()
