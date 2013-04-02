commotion-tests-core
====================

This repo is a cross-platform Python implementation of test vectors for the Commotion Wireless packages, minus any platform-specific packaging.  This repo is intended to be included as a submodule in other repos that contain the platform-specific packaging and environment.

The test vectors are described in the wiki pages below:

* https://code.commotionwireless.net/projects/commotion/wiki/Testing#Mesh-Routing-Tech-Evaluations
* https://code.commotionwireless.net/projects/commotion/wiki/Testing#Testbed-Requirements-based-on-test-suite-defined-above
* https://code.commotionwireless.net/projects/commotion/wiki/Testing#Release-Candidate-Test-Regimen

To launch the tests manually, have your Python intepreter execute either of the scripts in this directory, depending on your platform.

* testMainLinux.py (for Debian/Ubuntu and OpenWRT)
* testMainAndroid.py (for Android)

To the best extent feasible, this test code should run successfully under the following platforms:

* Python v2.7+ under Debian/Ubuntu
* Python for Android (Py4A) app r5+ / Scripting Layer for Android (SL4A) app r6+
* Python-mini package under OpenWRT 12.09+

... and test the following Commotion Wireless packages, respectively:

* commotion-mesh-applet package for GNOME/MATE/Cinnamon
* Mesh Testher Android app
* Commotion-OpenWRT DR1 firmware

__author__ Ben West (ben@gowasabi.net)<br/>
__version__ 0.1<br/>
__copyright__ Creative Commons BY-NC-SA v3.0<br/>
__license__ GPL v3<br/>
