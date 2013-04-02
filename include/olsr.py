"""OLSR test cases for Commotion Wireless.

This code assumes the OS's "ping" tool will return 0 if it receives
at least one successful response.
"""

__author__ = "Ben West (ben@gowasabi.net)"
__version__ = "0.1"
__copyright__ = "Creative Commons BY-NC-SA v3.0"
__license__ = "GPL v3"

import socket, os, sys, struct, subprocess, StringIO
import unittest
import urllib2, json
import common

class OlsrTest (unittest.TestCase):
    def setUp (self):
        """ First check if active OLSRd process running.  This method would best be put in
            a setUpClass to avoid repeated execution, but requires Python 2.7+ for Android. """
        self.psFound = False
	self.pids = [self.pid for self.pid in os.listdir('/proc') if self.pid.isdigit()]
	for self.pid in self.pids:
            try:
                 self.cmdline = open(os.path.join('/proc', self.pid, 'cmdline'), 'rb').read()
                 #trim down command line
                 self.cmdline = self.cmdline[0:self.cmdline.find('\0')]
                 if self.cmdline.rfind('/') > 0 :
                     self.cmdline = self.cmdline[self.cmdline.rfind('/')+1:len(self.cmdline)]
                 if self.cmdline == common.globals['olsrdPsName'] :
                    self.psFound = True
                    break
            except:
                 #process may have ended, ignore
                 pass
    def jsonPlugin (self):
        """ Check if jsoninfo plugin is responding """
        self.assertTrue(self.psFound, "couldn't find OLSRd process")
        # This urllib2 syntax won't work in Python v3
	self.req = urllib2.Request('http://localhost:' + str(common.globals['olsrdJsoninfoPort']) + '/olsrd.conf')
        try:
            self.conf = urllib2.urlopen(self.req).read()
        except URLError as e:
            self.fail('error: ' + e.reason) 
        self.assertIsNotNone(self.conf, "couldn't retreive OLSRd config")
    def routesLinks (self):
        """ Check routes and links """
        self.assertTrue(self.psFound, "couldn't find OLSRd process")
        # This urllib2 syntax won't work in Python v3
	self.req = urllib2.Request('http://localhost:' + str(common.globals['olsrdJsoninfoPort']) + '/links')
        try:
            self.links = json.load(urllib2.urlopen(self.req))
        except Exception as e:
            self.fail('error: ' + e.reason) 
	self.req = urllib2.Request('http://localhost:' + str(common.globals['olsrdJsoninfoPort']) + '/routes')
        try:
            self.routes = json.load(urllib2.urlopen(self.req))
        except Exception as e:
            self.fail('error: ' + e.reason)
        # Use assertNotEqual for Python 2.6 compatibility
        self.assertNotEqual(self.links, None, "couldn't retreive OLSRd links")
        self.assertNotEqual(self.routes, None, "couldn't retreive OLSRd routes")
        print 'links=' + str(self.links['links'])
        print 'routes=' + str(self.routes['routes'])
        # Verify next hop exists and good link quality
	for self.route in self.routes['routes']:
            if self.route['destination'] == '0.0.0.0':
                for self.link in self.links['links']:
                    if self.route['gateway'] == self.link['remoteIP']:
                        self.assertEqual((float(self.link['linkQuality']) > common.globals['olsrMinNextHopLQ']), True, 'next-hop link quality ' + str(self.link['linkQuality']) + ' too low')
                else:
                    if (len(self.links['links']) == 0):
                        self.fail('found no OLSR links')
        else:
            if (len(self.routes['routes']) == 0):
                self.fail('found no OLSR routes')

def suite():
    """ Define tests for this suite """
    suite = unittest.TestSuite()
    suite.addTest (OlsrTest("jsonPlugin"))
    suite.addTest (OlsrTest("routesLinks"))
    return suite
