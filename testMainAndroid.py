"""Top-level script for Commotion-Android test suite.
https://commotionwireless.net/projects/android

This script will run the Commotion Wireless suite of functional
tests on the Mesh Tether app and its environment.

Requisites to run these tests:

* AndroidOS v2.3+, rooted
* Superuser app & binary, or equivalent, v3.1.3+
* Python for Android (Py4A) app r5+ 
    https://code.google.com/p/python-for-android/
* Scripting Layer for Android (SL4A) app r6+ 
    https://code.google.com/p/android-scripting/
* Mesh Tether app, minimum version XXXX
"""
__author__ = "Ben West (ben@gowasabi.net)"
__version__ = "0.1"
__copyright__ = "Creative Commons BY-NC-SA v3.0"
__license__ = "GPL v3"

import sys, types, time, unittest, StringIO, string, datetime
import android

# Import test cases
import include.connectivity as connectivityTests
import include.olsr as olsrTests

# Import common functions and globals
import include.common as common

droid = android.Android()

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

def dialogFileSave (filePath, fileContents):
  """ Save contents to file specified, allowing user to edit
      filename/path before committing. """
  filePath = droid.dialogGetInput('Save Results to File', 'Choose file name', filePath).result
  if result is not None:
    print filePath
    with open(filePath,'w') as outf:
      outf.write(fileContents)
      outf.close()

def dialogSendEmail (msgContent):
  """ Send contents in an email, asking user to specify recipient """
  #Whether this works may depend on user's version of AndroidOS
  addr = ''
  droid.sendEmail(addr,'Commotion Test Log ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), msgContent)

if __name__ == '__main__':
  #Capture test ouputs
  testOutput = StringIO.StringIO()
  tee = TeeFile(testOutput)

  #Create test runner and run test suites
  runner = unittest.TextTestRunner(stream=tee,verbosity=2)
  connectivitySuite = connectivityTests.suite()
  olsrSuite = olsrTests.suite()
  runner.run (connectivitySuite)
  runner.run (olsrSuite)

  #Open dialog to send testOutput somewhere meaningful
  testResults = testOutput.getvalue()
  tee.close()
  title = "Test Results: " + testResults.split('\n')[-2]
  droid.dialogCreateAlert(title)
  droid.dialogSetSingleChoiceItems(['Save to File',
                                    'Send Email'])
  droid.dialogSetPositiveButtonText('Make It So')
  droid.dialogSetNeutralButtonText('Cancel')
  droid.dialogShow()
  response = droid.dialogGetResponse().result
  if response.has_key("which"):
    result=response["which"]
    if result=="positive":
      selected=droid.dialogGetSelectedItems().result.pop()
      if selected == 0:
        filePath = '/sdcard/commotion-test-log-' + datetime.datetime.now().strftime('%Y%m%d-%H%M') + '.txt'
        dialogFileSave (filePath, testResults)
      elif selected == 1:
        dialogSendEmail (testResults)
      else:
        print 'Undefined selection.'

      
