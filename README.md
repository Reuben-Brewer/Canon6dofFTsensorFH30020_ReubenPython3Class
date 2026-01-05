###########################

Canon6dofFTsensorFH30020_ReubenPython3Class

Control class (including ability to hook to Tkinter GUI) to control/read 6-DOF force/torque data from the Canon FH-300-20 sensor.

https://canon.jp/business/solution/indtech/forcetorque-sensor

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision D, 01/05/2026

Verified working on:

Python 3.11/12/13.

Windows 10/11 64-bit

Raspberry Pi Bookworm

(may work on Mac in non-GUI mode, but haven't tested yet)

Note For test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.py:

1. In Windows, you can get each sensor's USB-serial-device serial number by following the instructions in the USBserialDevice_GettingSerialNumberInWindows.png screenshot in this folder.

2. In Windows, you can manually set the latency timer for each sensor by following the instructions in the USBserialDevice_SettingLatencyTimerManuallyInWindows.png screenshot in this folder.

###########################

########################### Python module installation instructions, all OS's

############

test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.py, ListOfModuleDependencies:

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies: ['ftd2xx', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths', 'serial', 'serial.tools']

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['CSVdataLogger_ReubenPython3Class', 'EntryListWithBlinking_ReubenPython2and3Class', 'keyboard', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths']

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['EntryListWithBlinking_ReubenPython2and3Class', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths']

Canon6dofFTsensorFH30020_ReubenPython3Class, ListOfModuleDependencies_All:['CSVdataLogger_ReubenPython3Class', 'EntryListWithBlinking_ReubenPython2and3Class', 'ftd2xx', 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class', 'keyboard', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil', 'pyautogui', 'ReubenGithubCodeModulePaths', 'serial', 'serial.tools']

For test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.py:

pip install pyserial (NOT pip install serial).

pip install ftd2xx, ##https://pypi.org/project/ftd2xx/ #version 1.3.3 as of 11/08/23. For SetAllFTDIdevicesLatencyTimer function.

############

############

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies:

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies: ['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies_TestProgram: []

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies_NestedLayers: []

ExcelPlot_CSVdataLogger_ReubenPython3Code_Canon6dofFTsensorFH30020.py, ListOfModuleDependencies_All:['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

pip install pywin32=311

pip install xlsxwriter==3.2.9 #Might have to manually delete older version from /lib/site-packages if it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.

pip install xlutils==2.0.0

pip install xlwt==1.3.0

############

###########################

########################### FTDI installation instructions, Windows

(more to come)

###########################
