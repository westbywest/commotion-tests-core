commotion-tests-core includes
=============================

In addition to common.py containing shared functions and global variables, this directory shall contain python modules that implement the Commotion Wireless test vectors described on these wiki pages:

* https://code.commotionwireless.net/projects/commotion/wiki/Testing#Mesh-Routing-Tech-Evaluations
* https://code.commotionwireless.net/projects/commotion/wiki/Testing#Testbed-Requirements-based-on-test-suite-defined-above
* https://code.commotionwireless.net/projects/commotion/wiki/Testing#Release-Candidate-Test-Regimen

To the best extent feasible, the modules in this subdirectory should run successfully under the following platforms:

* Python v2.7 under Debian/Ubuntu
* Python for Android (Py4A) app r5+ / Scripting Layer for Android (SL4A) app r6+
* Python-mini package under OpenWRT 12.09+ 

The goal is to have container scripts for each platform simply import this directory and call the modules as needed, with each module providing a unittest.testCase and a suite() function to return the suite of tests to run.

__author__ Ben West (ben@gowasabi.net)<br/>
__version__ 0.1<br/>
__copyright__ Creative Commons BY-NC-SA v3.0<br/>
__license__ GPL v3<br/>
