#!/usr/bin/env python

import argparse
from cpppo.server.enip.get_attribute import proxy_simple


DIRECTION_CW  = [('@0x23/1/0x0c=(BOOL)0', 'DINT')]
DIRECTION_CCW = [('@0x23/1/0x0c=(BOOL)1', 'DINT')]


def build_preset_command(offset=0):
    cmd = '@0x23/1/0x13=(DINT){}'.format(offset)
    return [(cmd, 'DINT')]


def send_command(host, command):
    proxy = proxy_simple(host)
    ret, = proxy.read(command)
    return ret


def debug(host, log):
    print('{0:15} {1}'.format(host, log))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        action='append',
                        required=True,
                        help='Encoder IP')

    parser.add_argument('--cw',
                        action='store_true',
                        required=False,
                        help='CW Motion increases counts')

    parser.add_argument('--ccw',
                        action='store_true',
                        required=False,
                        help='CCW Motion increases counts')

    parser.add_argument('--offset',
                        type=int,
                        required=False,
                        help='Sets the current position as this value')

    args = parser.parse_args()

    for host in args.host:
        if args.cw:
            ret = send_command(host, DIRECTION_CW)
            debug(host, 'Set direction CW: {}'.format(ret))
        elif args.ccw:
            ret = send_command(host, DIRECTION_CCW)
            debug(host, 'Set direction CCW: {}'.format(ret))

        if args.offset is not None:
            offset = args.offset
            cmd = build_preset_command(offset)
            ret = send_command(host, cmd)
            debug(host, 'Set offset(preset): {} {}'.format(offset, ret))

