###########################

Canon6dofFTsensorFH30020_ReubenPython3Class

Control class (including ability to hook to Tkinter GUI) to control/read 6-DOF force/torque data from the Canon FH-300-20 sensor.

https://canon.jp/business/solution/indtech/forcetorque-sensor

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision A, 06/17/2024

Verified working on:

Python 3.11.

Windows 11 64-bit

Raspberry Pi Buster

(may work on Mac in non-GUI mode, but haven't tested yet)

Note For test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.py:

1. In Windows, you can get each sensor's USB-serial-device serial number by following the instructions in the USBserialDevice_GettingSerialNumberInWindows.png screenshot in this folder.

2. In Windows, you can manually set the latency timer for each sensor by following the instructions in the USBserialDevice_SettingLatencyTimerManuallyInWindows.png screenshot in this folder.

###########################

########################### Python module installation instructions, all OS's

############

test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.py, ListOfModuleDependencies:

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies: ['ftd2xx', 'future.builtins', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'serial', 'serial.tools']

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies_TestProgram: []

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['numpy']

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies_All:['ftd2xx', 'future.builtins', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'serial', 'serial.tools']

For test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.py:

pip install psutil

pip install pyserial (NOT pip install serial).

pip install ftd2xx, ##https://pypi.org/project/ftd2xx/ #version 1.3.3 as of 11/08/23. For SetAllFTDIdevicesLatencyTimer function.

############

############

ExcelPlot_CSVdataLogger_ReubenPython3Code__Canon6dofFTsensorFH30020.py,

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies: ['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies_TestProgram: []

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies_NestedLayers: []

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies_All:['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

For ExcelPlot_CSVdataLogger_ReubenPython3Code__Canon6dofFTsensorFH30020.py:

pip install pywin32         #version 305.1 11/8/23

pip install xlwt            #version 1.3.0 as of 11/8/23

pip install xlutils         #version 2.0.0 as of 11/8/23

pip install xlsxwriter      #version 3.1.9 as of 11/08/2023. Might have to manually delete older version from /lib/site-packages if it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.

############

###########################

########################### FTDI installation instructions, Windows

(more to come)

###########################
