"""Shared functions used in test cases for Commotion Wireless.

This code assumes the OS's "ping" tool will return 0 if it receives
at least one successful response.
"""

__author__ = "Ben West (ben@gowasabi.net)"
__version__ = "0.1"
__copyright__ = "Creative Commons BY-NC-SA v3.0"
__license__ = "GPL v3"

import socket, os, sys, struct, subprocess

# Some global variables
globals = dict ( olsrdPsName = 'olsrd',
                 olsrdJsoninfoPort = 9090,
                 olsrdTxtinfoPort = 2006,
                 olsrMinNextHopLQ = 0.3) #A next-hop LQ below this value fails

def get_default_gateway_linux():
    """Read the default IPv4 gateway directly from /proc."""
    with open('/proc/net/route') as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def get_olsr_gateway_linux():
    """Read the IPv4 gateway assigned by OLSRd from /proc. This gateway will
       be the entry with netmask 255.255.255.255. """
    with open('/proc/net/route') as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[2] != '00000000' and fields[7] == 'FFFFFFFF':
               return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

