#! /usr/bin/python3

import sys
import time


def easy():
    for i in range(100):
        time.sleep(1)
        sys.stdout.write("\r%d%%" % i)
        sys.stdout.flush()


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    # https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
    """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """

    # fix for finishing at 99%:
    iteration += 1

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def test_print_progress():
    for i in range(1, 100):
        print_progress(i, 100, prefix='prefix', suffix='suffix', bar_length=10)
        time.sleep(.1)


test_print_progress()
