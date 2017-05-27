#!/usr/bin/env python

import time
import argparse
import threading

from cpppo.server.enip.get_attribute import proxy_simple
from cpppo.server.enip import poll

POSITION_QUERY = [('@0x23/1/0x0a', 'DINT')]


def failure(exc):
    print(exc)


def process(par, val):
    print("%s: %16s == %r" % (time.ctime(), par, val))
process.done = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        required=True,
                        help='Encoder IP')

    parser.add_argument('--interval',
                        type=int,
                        default=1000,
                        help='Polling interval in milliseconds')

    args = parser.parse_args()
    cycle = args.interval / 1000

    poller = threading.Thread(
        target=poll.poll, kwargs={
            'proxy_class':  proxy_simple,
            'address':      (args.host, 44818),
            'cycle':        cycle,
            'timeout':      0.5,
            'process':      process,
            'failure':      failure,
            'params':       POSITION_QUERY,
        })
    poller.start()

    try:
        poller.join()
    except KeyboardInterrupt:
        process.done = True
