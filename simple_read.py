#!/usr/bin/env python

import argparse
from cpppo.server.enip.get_attribute import proxy_simple


POSITION_QUERY = [('@0x23/1/0x0a', 'DINT')]


def read_encoder(host):
    proxy = proxy_simple(host)
    position, = proxy.read(POSITION_QUERY)
    return position[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        action='append',
                        required=True,
                        help='Encoder IP')

    args = parser.parse_args()

    for host in args.host:
        print('{0:15} {1}'.format(host, read_encoder(host)))
