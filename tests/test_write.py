import os
import random
import filesequence


def test_randoms(N=100000):
    '''Generating random integers'''
    limit = 1e6

    filenames = [
        'random.randint-01.txt', 'random.randint-02.txt',
        'random.randint-03.txt', 'random.randint-04.txt',
        'random.randint-05.txt', 'random.randint-06.txt',
        'random.randint-07.txt', 'random.randint-08.txt',
        'random.randint-09.txt']
    with filesequence.FileSequence(filenames, limit, 'w') as output:
        for line in xrange(N):
            integer = random.randint(0, 1e64)
            output.write(str(line) + '\t' + str(integer) + '\n')

    for filename in filenames[:-1]:
        assert os.path.getsize(filename) <= limit, 'File should be less than %d bytes' % limit

    assert not os.path.exists(filenames[-1]), '%d randoms should only take eight files' % N

    # teardown
    for filename in filenames[:-1]:
        os.remove(filename)
