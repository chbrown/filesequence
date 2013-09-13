import sys
import argparse
import filesequence
import logging


def main():
    parser = argparse.ArgumentParser(
        description='Write STDIN into a sequence of files, splitting only at newlines',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--limit', type=int, default=50000000,
        help='Maximum bytes per file')
    parser.add_argument('--pattern', type=str, default='split.%02d',
        help='Filename string pattern: generate filenames in sequence by interpolating (%%) '
        'this pattern with an autoincrementing integer [0, 1000)')
    parser.add_argument('--version', action='version', version=filesequence.__version__)
    parser.add_argument('--verbose', action='store_true', help='Print debug messages')
    opts = parser.parse_args()

    loglevel = logging.INFO if opts.verbose else logging.VERBOSE
    logging.basicConfig(format='%(levelname)s: %(message)s', level=loglevel)

    filenames = filesequence.interpolator(opts.pattern, xrange(1000))
    logging.debug('Writing to sequence: %s', ', '.join(filesequence.interpolator(opts.pattern, range(3))))

    if sys.stdin.isatty():
        raise IOError('You must provide input via STDIN')

    with filesequence.FileSequence(filenames, opts.limit) as output:
        for line in sys.stdin:
            output.write(line)

if __name__ == '__main__':
    main()
