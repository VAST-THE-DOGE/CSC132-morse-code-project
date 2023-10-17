# CSC132-morse-code-project

#Setup#
!!!This setup is very work in progress so there will be errors and gaps in the setup process along with changes!!!
Github download link: https://github.com/VAST-THE-DOGE/CSC132-morse-code-project/tree/7ad6daefc76f621abdf81c7464d594cfec24b733/download
1. Make sure you have a system running the RPi OS that has the GPIO library installed.
2. Install the script in the desktop folder of your RPi.
3. Setup your GPIO pins and change the pin values at the top of the script to the correct pins. The SENSOR is used for input and the IR_LED and the RED_LED are used for output.
4. Change any additional settings to your needs.
5. Verify that the script works as expected by running and testing it.
6. If the script works then continue, if not then follow the troubleshooting at the bottom of the readme.
7. !More to be added!

#Info#
This is a script designed to be used on the Raspberry Pi to receive on/off input and to translate it into Morse Code and then into English.
The script also does this in reverse by translating English into Morse Code and sending it via any LED or system that uses on/off GPIO.

#troubleshooting#
This is not implemented yet, so  fill out a bug report and submit it and we will try to fix the problem. Furthermore, make sure to update to the newest version regularly since each version has a chance to fix the bug that you are dealing with.
Github bug report link: https://github.com/VAST-THE-DOGE/CSC132-morse-code-project/blob/7ad6daefc76f621abdf81c7464d594cfec24b733/.github/ISSUE_TEMPLATE/bug_report.md
