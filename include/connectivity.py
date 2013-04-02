"""Internet/Network connectivity test cases for Commotion Wireless.

This code assumes the OS's "ping" tool will return 0 if it receives
at least one successful response.
"""

__author__ = "Ben West (ben@gowasabi.net)"
__version__ = "0.1"
__copyright__ = "Creative Commons BY-NC-SA v3.0"
__license__ = "GPL v3"

import socket, os, sys, struct, subprocess
import unittest
import common

class ConnectivityTest (unittest.TestCase):
    def pingLocalhost (self):
        """ Ping localhost. """
        self.response = subprocess.call('ping -c 1 127.0.0.1',
                                        shell=True,
                                        stdout=open('/dev/null', 'w'),
                                        stderr=subprocess.STDOUT)
        self.assertEqual(self.response, 0)
    def pingGateway (self):
        """ Ping Gateway. """
        self.gateway = common.get_default_gateway_linux()
	# If no default gateway found, try olsr gateway
	if self.gateway is None:
            self.gateway = common.get_olsr_gateway_linux()
        self.assertNotEqual(self.gateway, None, 'no default or olsr gateway found')
        self.response = subprocess.call('ping -c 3 ' + self.gateway,
                                        shell=True,
                                        stdout=open('/dev/null', 'w'),
                                        stderr=subprocess.STDOUT)
        self.assertEqual(self.response, 0, 'ping to ' + self.gateway + ' failed')
    def pingGoogle (self):
        """ Ping Google DNS. """
        self.response = subprocess.call('ping -c 3 8.8.8.8',
                                        shell=True,
                                        stdout=open('/dev/null', 'w'),
                                        stderr=subprocess.STDOUT)
        self.assertEqual(self.response, 0)

def suite():
    """ Define tests for this suite """
    suite = unittest.TestSuite()
    suite.addTest (ConnectivityTest("pingLocalhost"))
    suite.addTest (ConnectivityTest("pingGateway"))
    suite.addTest (ConnectivityTest("pingGoogle"))
    return suite
