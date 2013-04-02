"""Top-level script for Commotion-Mesh-Applet test suite.
https://github.com/opentechinstitute/commotion-mesh-applet

This script will run the Commotion Wireless suite of functional
tests on the Commotion-Mesh-Applet and its host OS (e.g. Debian,
Ubuntu).

Requisites to run these tests:

* Debian/Ubuntu Linux OS or derivative
* GNOME 3, GNOME 3 Classic, GNOME 2, Cinnamon, KDE, or MATE 
window manager
* Python v2.7
* commotion-mesh-applet app, minimum version XXXX
"""
__author__ = "Ben West (ben@gowasabi.net)"
__version__ = "0.1"
__copyright__ = "Creative Commons BY-NC-SA v3.0"
__license__ = "GPL v3"

import sys, types, time, unittest, StringIO, string, datetime

# Import test cases
import include.connectivity as connectivityTests
import include.olsr as olsrTests

# Import common functions and globals
import include.common as common

class TeeFile(object):
  """ Class to mimic 'tee' UNIX tool; write both to file and stderr.
      Assumes file object parameter, already opened for writing. """
  def __init__(self, theFile):
    self.file = theFile
    self.stderr = sys.stderr
    sys.stderr = self
  def close(self):
    if self.stderr is not None:
      sys.stderr = self.stderr
      self.stderr = None
    if self.file is not None:
      self.file.close()
      self.file = None
  def write(self, data):
    self.file.write(data)
    self.stderr.write(data)
  def flush(self):
    self.file.flush()
    self.stderr.flush()
  def __del__(self):
    self.close()

if __name__ == '__main__':
  #Capture test ouputs
  testOutput = StringIO.StringIO()
  tee = TeeFile(testOutput)

  #Create test runner and run test suites 
  runner = unittest.TextTestRunner(stream=tee,verbosity=2)
  connectivitySuite = connectivityTests.suite()
  olsrSuite = olsrTests.suite()
  #runner.run (connectivitySuite)
  runner.run (olsrSuite)

  #Write testOutput somewhere meaningful, if desired
  #testResults = testOutput.getvalue()
  #summary = testResults.split('\n')[-2]
  #filePath = 'commotion-test-log-' + datetime.datetime.now().strftime('%Y%m%d-%H%M') + '.txt'
  #with open(filePath,'w') as outf:
  #  outf.write(fileContents)
  #  outf.close()

  tee.close()

