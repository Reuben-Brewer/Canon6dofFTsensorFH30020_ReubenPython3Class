# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Software Revision C, 09/27/2024

Verified working on: Python 3.11 for Windows 11 64-bit and Raspberry Pi Buster (may work on Mac in non-GUI mode, but haven't tested yet).
'''

__author__ = 'reuben.brewer'

##########################################
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
#import binascii
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import queue as Queue
##########################################

##########################################
from future.builtins import input as input
########################################## "sudo pip3 install future" (Python 3)

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

#########################################################

##########################
import serial #___IMPORTANT: pip install pyserial (NOT pip install serial).
from serial.tools import list_ports
##########################

##########################
global ftd2xx_IMPORTED_FLAG
ftd2xx_IMPORTED_FLAG = 0
try:
    import ftd2xx #https://pypi.org/project/ftd2xx/ 'pip install ftd2xx', current version is 1.3.1 as of 05/06/22. For SetAllFTDIdevicesLatencyTimer function
    ftd2xx_IMPORTED_FLAG = 1

except:
    exceptions = sys.exc_info()[0]
    print("**********")
    print("********** Canon6dofFTsensorFH30020_ReubenPython3Class __init__: ERROR, failed to import ftdtxx, Exceptions: %s" % exceptions + " ********** ")
    print("**********")
##########################

#########################################################

class Canon6dofFTsensorFH30020_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### Canon6dofFTsensorFH30020_ReubenPython3Class __init__ starting. ####################")

        self.PrintAllReceivedSerialMessageForDebuggingFlag = 0

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.SerialObject = serial.Serial()
        self.SerialConnectedFlag = 0
        self.SerialTimeoutSeconds = 0.5
        self.SerialParity = serial.PARITY_NONE
        self.SerialStopBits = serial.STOPBITS_ONE
        self.SerialByteSize = serial.EIGHTBITS
        self.SerialRxBufferSize = round(35*1.1) #36 bytes per message
        self.SerialTxBufferSize = round(35*1.1) #36 bytes per message
        self.SerialPortNameCorrespondingToCorrectSerialNumber = "default"
        self.DedicatedTxThread_TxMessageToSend_Queue = Queue.Queue()
        self.SerialStrToTx_LAST_SENT = ""

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromDedicatedTxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedTxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread_2 = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = -11111.0

        self.LastTimeHeartbeatWasSent_CalculatedFromDedicatedTxThread = -11111.0

        self.CurrentTime_CalculatedFromDedicatedRxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedRxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = -11111.0
        
        self.CurrentTime_CalculateMeasurementForceDerivative = -11111.0
        self.LastTime_CalculateMeasurementForceDerivative = -11111.0
        self.DataStreamingDeltaT_CalculateMeasurementForceDerivative = -11111.0
        #########################################################
        #########################################################

        self.Checksum_ErrorCounter = 0
        self.FilterFrequencyHz_Received = -1

        '''
        ４-４-１. Standard Binary Output: A total of 21 bytes are output for each output.
        ４-４-２. Simple Binary Output: A total of 15 bytes are output for each output.
        ４-４-３. Standard ASCII Output: A total of 36 bytes are output for each output.
        ４-４-４. Simple ASCII Output: A total of 30 bytes are output for each output.
        '''

        self.StreamingModeAcceptableValuesAndSettingsDict = dict([("Binary_Standard_Oneshot", dict([("NumberOfBytesPerMessage", 21), ("SerialCommandToStartContinuousStreaming", "A")])),
                                                                            ("Binary_Standard_Continuous", dict([("NumberOfBytesPerMessage", 21), ("SerialCommandToStartContinuousStreaming", "B")])),
                                                                            ("Binary_Simple_Oneshot", dict([("NumberOfBytesPerMessage", 15), ("SerialCommandToStartContinuousStreaming", "C")])),
                                                                            ("Binary_Simple_Continuous", dict([("NumberOfBytesPerMessage", 15), ("SerialCommandToStartContinuousStreaming", "D")]))])
                                                                            #("ASCII_Standard_Oneshot", dict([("NumberOfBytesPerMessage", 36), ("SerialCommandToStartContinuousStreaming", "P")])), #IMPLEMENT ASCII LATER
                                                                            #("ASCII_Standard_Continuous",dict([("NumberOfBytesPerMessage", 36), ("SerialCommandToStartContinuousStreaming", "Q")])),
                                                                            #("ASCII_Simple_Oneshot", dict([("NumberOfBytesPerMessage", 30), ("SerialCommandToStartContinuousStreaming", "R")])),
                                                                            #("ASCII_Simple_Continuous", dict([("NumberOfBytesPerMessage", 30), ("SerialCommandToStartContinuousStreaming", "S")]))])

        self.FilterFrequencyCutoffHzAcceptableValuesAndSettingsDict = dict([(1, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "7")])),
                                                                    (5, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "6")])),
                                                                    (10, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "5")])),
                                                                    (50, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "4")])),
                                                                    (100, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "3")])),
                                                                    (500, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "2")])),
                                                                    (1000, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "1")])),
                                                                    (5000, dict([("SerialCommandToSetFilterFrequencyCutoffHz", "0")]))])

        print("self.StreamingModeAcceptableValuesAndSettingsDict: " + str(self.StreamingModeAcceptableValuesAndSettingsDict))

        self.SerialBaudRateAcceptableValues = [57600, 115200, 921600]
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        self.CurrentMeasurementForce_lb = -11111.0
        self.LastMeasurementForce_lb = -11111.0

        self.ResetTare_EventNeedsToBeFiredFlag = 0
        self.ResetTare_EventHasHappenedFlag = 0

        self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag = 1 #Set to 1 so that the filter will get set at the start of the program
        self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag = 0

        self.FlushSerial_EventNeedsToBeFiredFlag = 0
        
        self.MostRecentDataDict = dict()

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber_USBtoSerialConverter" in setup_dict:
            self.DesiredSerialNumber_USBtoSerialConverter = setup_dict["DesiredSerialNumber_USBtoSerialConverter"]

        else:
            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: ERROR, must initialize object with 'DesiredSerialNumber_USBtoSerialConverter' argument.")
            return

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: DesiredSerialNumber_USBtoSerialConverter: " + str(self.DesiredSerialNumber_USBtoSerialConverter))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SerialBaudRate" in setup_dict:
            self.SerialBaudRate = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("SerialBaudRate", setup_dict["SerialBaudRate"], self.SerialBaudRateAcceptableValues[0], self.SerialBaudRateAcceptableValues[-1]))

            if self.SerialBaudRate not in self.SerialBaudRateAcceptableValues:
                print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: Error, SerialBaudRate must be contained in the set " + str(self.SerialBaudRateAcceptableValues))
                return

        else:
            self.SerialBaudRate = self.SerialBaudRateAcceptableValues[-1]

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: SerialBaudRate: " + str(self.SerialBaudRate))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedRxThread_TimeToSleepEachLoop" in setup_dict:
            self.DedicatedRxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedRxThread_TimeToSleepEachLoop", setup_dict["DedicatedRxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedRxThread_TimeToSleepEachLoop = 0.005

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: DedicatedRxThread_TimeToSleepEachLoop: " + str(self.DedicatedRxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedTxThread_TimeToSleepEachLoop" in setup_dict:
            self.DedicatedTxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedTxThread_TimeToSleepEachLoop", setup_dict["DedicatedTxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedTxThread_TimeToSleepEachLoop = 0.005

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: DedicatedTxThread_TimeToSleepEachLoop: " + str(self.DedicatedTxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ResetTareAtStartOfProgramFlag" in setup_dict:
            self.ResetTareAtStartOfProgramFlag = self.PassThrough0and1values_ExitProgramOtherwise("ResetTareAtStartOfProgramFlag", setup_dict["ResetTareAtStartOfProgramFlag"])
        else:
            self.ResetTareAtStartOfProgramFlag = 1

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: ResetTareAtStartOfProgramFlag: " + str(self.ResetTareAtStartOfProgramFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "StreamingModeString" in setup_dict:
            StreamingModeString_temp = setup_dict["StreamingModeString"]

            if StreamingModeString_temp in self.StreamingModeAcceptableValuesAndSettingsDict:
                self.StreamingModeString = StreamingModeString_temp

            else:
                print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: StreamingModeString must be contained within" + str(self.StreamingModeAcceptableValuesAndSettingsDict))
                return

        else:
            self.StreamingModeString = "Binary_Simple_Continuous"

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: StreamingModeString: " + str(self.StreamingModeString))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FilterFrequencyCutoffHz" in setup_dict:
            self.FilterFrequencyCutoffHz = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FilterFrequencyCutoffHz", setup_dict["FilterFrequencyCutoffHz"], 1, 5000))

            if self.FilterFrequencyCutoffHz not in self.FilterFrequencyCutoffHzAcceptableValuesAndSettingsDict:
                print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: Error, FilterFrequencyCutoffHz must be contained in the set " + str(self.FilterFrequencyCutoffHzAcceptableValuesAndSettingsDict))
                return

        else:
            self.FilterFrequencyCutoffHz = 1000

        print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: FilterFrequencyCutoffHz: " + str(self.FilterFrequencyCutoffHz))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromDedicatedTxThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                             ("DataStreamingFrequency_CalculatedFromDedicatedRxThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            if ftd2xx_IMPORTED_FLAG == 1:
                self.SetAllFTDIdevicesLatencyTimer()
            #########################################################

            #########################################################
            self.FindAssignAndOpenSerialPort()
            #########################################################

            #########################################################
            if self.SerialConnectedFlag != 1:
                return
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("Canon6dofFTsensorFH30020_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedRxThread_ThreadingObject = threading.Thread(target=self.DedicatedRxThread, args=())
        self.DedicatedRxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        time.sleep(0.1) #unicorn, delay Tx thread so that Rx thread can get ready to read from serial device and not miss any filter queries from the sensor
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedTxThread_ThreadingObject = threading.Thread(target=self.DedicatedTxThread, args=())
        self.DedicatedTxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        time.sleep(0.25)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __del__(self):
        pass
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetAllFTDIdevicesLatencyTimer(self, FTDI_LatencyTimer_ToBeSet = 1):

        FTDI_LatencyTimer_ToBeSet = self.LimitNumber_IntOutputOnly(1, 16, FTDI_LatencyTimer_ToBeSet)

        FTDI_DeviceList = ftd2xx.listDevices()
        print("FTDI_DeviceList: " + str(FTDI_DeviceList))

        if FTDI_DeviceList != None:

            for Index, FTDI_SerialNumber in enumerate(FTDI_DeviceList):

                #################################
                try:
                    if sys.version_info[0] < 3: #Python 2
                        FTDI_SerialNumber = str(FTDI_SerialNumber)
                    else:
                        FTDI_SerialNumber = FTDI_SerialNumber.decode('utf-8')

                    FTDI_Object = ftd2xx.open(Index)
                    FTDI_DeviceInfo = FTDI_Object.getDeviceInfo()

                    '''
                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          ", DeviceInfo: " +
                          str(FTDI_DeviceInfo))
                    '''

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not open FTDI device, Exceptions: %s" % exceptions)
                #################################

                #################################
                try:
                    FTDI_Object.setLatencyTimer(FTDI_LatencyTimer_ToBeSet)
                    time.sleep(0.005)

                    FTDI_LatencyTimer_ReceivedFromDevice = FTDI_Object.getLatencyTimer()
                    FTDI_Object.close()

                    if FTDI_LatencyTimer_ReceivedFromDevice == FTDI_LatencyTimer_ToBeSet:
                        SuccessString = "succeeded!"
                    else:
                        SuccessString = "failed!"

                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          " commanded setLatencyTimer(" +
                          str(FTDI_LatencyTimer_ToBeSet) +
                          "), and getLatencyTimer() returned: " +
                          str(FTDI_LatencyTimer_ReceivedFromDevice) +
                          ", so command " +
                          SuccessString)

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not set/get Latency Timer, Exceptions: %s" % exceptions)
                #################################

        else:
            print("SetAllFTDIdevicesLatencyTimer ERROR: FTDI_DeviceList is empty, cannot proceed.")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FindAssignAndOpenSerialPort(self):
        self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Finding all serial ports...")

        ##############
        SerialNumberToCheckAgainst = str(self.DesiredSerialNumber_USBtoSerialConverter)
        if self.my_platform == "linux" or self.my_platform == "pi":
            SerialNumberToCheckAgainst = SerialNumberToCheckAgainst[:-1] #The serial number gets truncated by one digit in linux
        else:
            SerialNumberToCheckAgainst = SerialNumberToCheckAgainst
        ##############

        ##############
        SerialPortsAvailable_ListPortInfoObjetsList = serial.tools.list_ports.comports()
        ##############

        ###########################################################################
        SerialNumberFoundFlag = 0
        for SerialPort_ListPortInfoObjet in SerialPortsAvailable_ListPortInfoObjetsList:

            SerialPortName = SerialPort_ListPortInfoObjet[0]
            Description = SerialPort_ListPortInfoObjet[1]
            VID_PID_SerialNumber_Info = SerialPort_ListPortInfoObjet[2]
            self.MyPrint_WithoutLogFile(SerialPortName + ", " + Description + ", " + VID_PID_SerialNumber_Info)

            if VID_PID_SerialNumber_Info.find(SerialNumberToCheckAgainst) != -1 and SerialNumberFoundFlag == 0: #Haven't found a match in a prior loop
                self.SerialPortNameCorrespondingToCorrectSerialNumber = SerialPortName
                SerialNumberFoundFlag = 1 #To ensure that we only get one device
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Found serial number " + SerialNumberToCheckAgainst + " on port " + self.SerialPortNameCorrespondingToCorrectSerialNumber)
                #WE DON'T BREAK AT THIS POINT BECAUSE WE WANT TO PRINT ALL SERIAL DEVICE NUMBERS WHEN PLUGGING IN A DEVICE WITH UNKNOWN SERIAL NUMBE RFOR THE FIRST TIME.
        ###########################################################################

        ###########################################################################
        if(self.SerialPortNameCorrespondingToCorrectSerialNumber != "default"): #We found a match

            try: #Will succeed as long as another program hasn't already opened the serial line.

                self.SerialObject = serial.Serial(self.SerialPortNameCorrespondingToCorrectSerialNumber, self.SerialBaudRate, timeout=self.SerialTimeoutSeconds, parity=self.SerialParity, stopbits=self.SerialStopBits, bytesize=self.SerialByteSize)
                self.SerialObject.set_buffer_size(rx_size=self.SerialRxBufferSize, tx_size=self.SerialTxBufferSize)
                self.SerialConnectedFlag = 1
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Serial is connected and open on port: " + self.SerialPortNameCorrespondingToCorrectSerialNumber)

            except:
                self.SerialConnectedFlag = 0
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: ERROR: Serial is physically plugged in but IS IN USE BY ANOTHER PROGRAM.")

        else:
            self.SerialConnectedFlag = -1
            self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: ERROR: Could not find the serial device. IS IT PHYSICALLY PLUGGED IN?")
        ###########################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedTxThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread - self.LastTime_CalculatedFromDedicatedTxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedTxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedTxThread", DataStreamingFrequency_CalculatedFromDedicatedTxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedTxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedRxThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread - self.LastTime_CalculatedFromDedicatedRxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedRxThread", DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedRxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CalculateMeasurementForceDerivative(self):

        try:
            self.CurrentTime_CalculateMeasurementForceDerivative = self.getPreciseSecondsTimeStampString()
            
            self.DataStreamingDeltaT_CalculateMeasurementForceDerivative = self.CurrentTime_CalculateMeasurementForceDerivative - self.LastTime_CalculateMeasurementForceDerivative

            ##########################################################################################################
            if self.DataStreamingDeltaT_CalculateMeasurementForceDerivative != 0.0:
                MeasurementForceDerivative_lbPerSec_raw = (self.CurrentMeasurementForce_lb - self.LastMeasurementForce_lb)/self.DataStreamingDeltaT_CalculateMeasurementForceDerivative

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("ForceDerivative", MeasurementForceDerivative_lbPerSec_raw)]))
                MeasurementForceDerivative_lbPerSec_filtered = ResultsDict["ForceDerivative"]["Filtered_MostRecentValuesList"][0]

                MeasurementForceDerivative_DictOfConvertedValues = self.ConvertForceToAllUnits(MeasurementForceDerivative_lbPerSec_filtered, "lb")

                self.LastTime_CalculateMeasurementForceDerivative = self.CurrentTime_CalculateMeasurementForceDerivative

                return MeasurementForceDerivative_DictOfConvertedValues
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("CalculateMeasurementForceDerivative, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertBytesObjectToString(self, InputBytesObject):

        try:
            if sys.version_info[0] < 3:  # Python 2
                OutputString = str(InputBytesObject)

            else:
                OutputString = InputBytesObject.decode('utf-8')

            return OutputString

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertBytesObjectToString, Exceptions: %s" % exceptions)
            #traceback.print_exc()
            return ""

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SendSerialStrToTx(self, SerialStrToTx):

        if self.SerialConnectedFlag == 1:

            try:

                if SerialStrToTx[-1] != "\r":
                    SerialStrToTx = SerialStrToTx + "\r"

                SerialStrToTx = SerialStrToTx

                self.SerialObject.write(SerialStrToTx.encode('utf-8'))

                self.SerialStrToTx_LAST_SENT = SerialStrToTx

                self.MostRecentDataDict["SerialStrToTx_LAST_SENT"] = self.SerialStrToTx_LAST_SENT

            except:
                exceptions = sys.exc_info()[0]
                print("SendSerialStrToTx, exceptions: %s" % exceptions)

        else:
            print("SendSerialStrToTx: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################
    
    ########################################################################################################## 
    ##########################################################################################################
    def StartVariableStreaming(self, StreamingModeString = "Binary_Simple"):

        if self.SerialConnectedFlag == 1:
            try:

                StreamingModeString = str(StreamingModeString)

                if StreamingModeString in self.StreamingModeAcceptableValuesAndSettingsDict:
                    StringToTx = self.StreamingModeAcceptableValuesAndSettingsDict[StreamingModeString]["SerialCommandToStartContinuousStreaming"]

                    self.DedicatedTxThread_TxMessageToSend_Queue.put(StringToTx)
                    
                    self.StreamingModeString = StreamingModeString

                    return 1
                else:
                   print("StartVariableStreaming: Error, StreamingModeString of " + StreamingModeString + " not in self.StreamingModeAcceptableValuesAndSettingsDict = " + str(self.StreamingModeAcceptableValuesAndSettingsDict))
                return 0

            except:
                exceptions = sys.exc_info()[0]
                print("StartVariableStreaming, exceptions: %s" % exceptions)
                return 0

        else:
            print("StartVariableStreaming: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################
    
    ########################################################################################################## 
    ##########################################################################################################
    def StopVariableStreaming(self):

        if self.SerialConnectedFlag == 1:
            try:

                StringToTx = "E"

                self.DedicatedTxThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("StopVariableStreaming, exceptions: %s" % exceptions)

        else:
            print("StopVariableStreaming: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTare(self):

        if self.SerialConnectedFlag == 1:
            try:
                
                StringToTx = "O"

                self.ResetTare_EventHasHappenedFlag = 1
                
                self.DedicatedTxThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("ResetTare, exceptions: %s" % exceptions)

        else:
            print("ResetTare: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetFilterFrequencyCutoffHz(self, FilterFrequencyCutoffHz, SendImmediatelyInsteadOfAddingToQueueFlag = 1):

        if self.SerialConnectedFlag == 1:
            try:

                if FilterFrequencyCutoffHz in self.FilterFrequencyCutoffHzAcceptableValuesAndSettingsDict:

                    StringToTx = self.FilterFrequencyCutoffHzAcceptableValuesAndSettingsDict[FilterFrequencyCutoffHz]["SerialCommandToSetFilterFrequencyCutoffHz"]

                    if SendImmediatelyInsteadOfAddingToQueueFlag == 0:
                        self.DedicatedTxThread_TxMessageToSend_Queue.put(StringToTx)
                    else:
                        self.SendSerialStrToTx(StringToTx + "/r")

                    self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag = 1

                    print("SetFilterFrequencyCutoffHz event happened, StringToTx: " + str(StringToTx))

                    return 1

                else:
                    print("SetFilterFrequencyCutoffHz: Error, FilterFrequencyCutoffHz = " + str(FilterFrequencyCutoffHz) + " is not within set " + str(self.FilterFrequencyCutoffHzAcceptableValuesAndSettingsDict))
                    return 0

            except:
                exceptions = sys.exc_info()[0]
                print("SetFilterFrequencyCutoffHz, exceptions: %s" % exceptions)

        else:
            print("SetFilterFrequencyCutoffHz: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetFilterFrequencyCutoffHz(self, SendImmediatelyInsteadOfAddingToQueueFlag = 1):

        if self.SerialConnectedFlag == 1:
            try:

                StringToTx = "F"

                if SendImmediatelyInsteadOfAddingToQueueFlag == 0:
                    self.DedicatedTxThread_TxMessageToSend_Queue.put(StringToTx)
                else:
                    self.SendSerialStrToTx(StringToTx + "/r")

                print("GetFilterFrequencyCutoffHz event fired!")
                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("GetFilterFrequencyCutoffHz, exceptions: %s" % exceptions)

        else:
            print("GetFilterFrequencyCutoffHz: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertForceFromIntegerToN(self, InputValue, SimpleFlag = 1):

        try:

            if SimpleFlag == 1:
                OutputValue = (InputValue - 8192) * 300.0 / 1639

            else:
                OutputValue = (InputValue - 524288) * 300.0 / 262144
        
            return OutputValue

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("ConvertForceFromIntegerToNewtons InputValue: " + str(InputValue) + ", exceptions: %s" % exceptions)
            return -11111.0
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertMomentFromIntegerToNm(self, InputValue, SimpleFlag = 1):

        try:
            if SimpleFlag == 1:
                OutputValue = (InputValue - 8192) * 20.0 / 1639

            else:
                OutputValue = (InputValue - 524288) * 20.0 / 262144

            return OutputValue

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("ConvertMomentFromBinaryToNewtons InputValue: " + str(InputValue) + ", exceptions: %s" % exceptions)
            return -11111.0
            # traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedTxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedTxThread for Canon6dofFTsensorFH30020_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################

        #########################################################
        #########################################################
        for Counter in range(0,5):
            self.StopVariableStreaming()
            time.sleep(0.002)

        self.StartVariableStreaming(self.StreamingModeString)

        if self.ResetTareAtStartOfProgramFlag == 1:
            time.sleep(0.25)
            self.ResetTare_EventNeedsToBeFiredFlag = 1
        #########################################################
        #########################################################

        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedTxThread
            ##########################################################################################################

            ########################################################################################################## These should be outside of the queue and heartbeat
            ##########################################################################################################

            ##########################################################################################################
            if self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag == 0 and self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag == 0:
                if self.StreamingModeString.find("Oneshot") != -1:
                    self.StartVariableStreaming(self.StreamingModeString) #Have to Tx a query to get new data if we're in Oneshot mode
            ##########################################################################################################

            ##########################################################################################################
            if self.FlushSerial_EventNeedsToBeFiredFlag == 1:
                self.SerialObject.reset_input_buffer()
                self.FlushSerial_EventNeedsToBeFiredFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.ResetTare_EventNeedsToBeFiredFlag == 1:
                self.ResetTare()
                self.ResetTare_EventNeedsToBeFiredFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag == 0 and self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag == 1:
                for Counter in range(0, 2):
                    self.GetFilterFrequencyCutoffHz() #DO THIS BEFORE SetFilterFrequencyCutoffHz
                    #time.sleep(0.002)
                self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag == 1 and self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag == 0:
                for Counter in range(0, 1):
                    self.SetFilterFrequencyCutoffHz(self.FilterFrequencyCutoffHz)
                    #time.sleep(0.002)
                self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ###############################################
            ###############################################
            ###############################################
            if self.DedicatedTxThread_TxMessageToSend_Queue.qsize() > 0:
                try:

                    ##########################################################################################################
                    TxDataToWrite = self.DedicatedTxThread_TxMessageToSend_Queue.get()

                    if TxDataToWrite[-1] != "\r":
                        TxDataToWrite = TxDataToWrite + "\r"

                    #print("TxDataToWrite: " + str(TxDataToWrite))
                    self.SendSerialStrToTx(TxDataToWrite)
                    ##########################################################################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Canon6dofFTsensorFH30020_ReubenPython3Class, DedicatedTxThread, Inner Exceptions: %s" % exceptions)
                    traceback.print_exc()

            ###############################################
            ###############################################
            ###############################################
            
            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_DedicatedTxThread_Filtered()

            if self.DedicatedTxThread_TimeToSleepEachLoop > 0.0:
                if self.DedicatedTxThread_TimeToSleepEachLoop > 0.001:
                    time.sleep(self.DedicatedTxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                else:
                    time.sleep(self.DedicatedTxThread_TimeToSleepEachLoop)
            ###############################################
            ###############################################
            ###############################################

        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedTxThread for Canon6dofFTsensorFH30020_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedRxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedRxThread for Canon6dofFTsensorFH30020_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedRxThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag == 1 or self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag == 1: #Look at both flags, not just 1.
                    NumberOfBytesPerMessage = 30*2 #Maybe needs to be higher, more like 30
                else:
                    NumberOfBytesPerMessage = self.StreamingModeAcceptableValuesAndSettingsDict[self.StreamingModeString]["NumberOfBytesPerMessage"]

                #print("NumberOfBytesPerMessage: " + str(NumberOfBytesPerMessage))
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.StreamingModeString.find("Simple") != -1:
                    SimpleFlag = 1
                else:
                    SimpleFlag = 0
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.StreamingModeString.find("ASCII") != -1:
                    RxMessage = self.SerialObject.read_until(b'\n')
                else:
                    RxMessage = self.SerialObject.read(NumberOfBytesPerMessage)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                try:

                    if len(RxMessage) > 0:

                        ##########################################################################################################
                        ##########################################################################################################
                        RxMessageString = str(RxMessage)
                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        if self.PrintAllReceivedSerialMessageForDebuggingFlag == 1:
                            print("RxMessage Len = " + str(len(RxMessage)),
                                  ", ByteLen = " + str(len(RxMessage)) +
                                  ", Message = " + str(RxMessage))
                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        MatchIndex_1 = RxMessageString.find("Cutoff frequency: ")
                        MatchIndex_2 = RxMessageString.find("Hz")
                        if MatchIndex_1 != -1 and MatchIndex_2 != -1:

                            FilterFrequencyHz_Received_Str = RxMessageString[MatchIndex_1:MatchIndex_2+2]
                            print("FilterFrequencyHz_Received_Str: " + str(FilterFrequencyHz_Received_Str))

                            FilterFrequencyHz_Received_Str = str(FilterFrequencyHz_Received_Str.replace("Cutoff frequency: ","").replace("Hz","").replace("b","").replace("'","")) #Why is the string including the b' ' ?
                            try:
                                self.FilterFrequencyHz_Received = int(FilterFrequencyHz_Received_Str)
                            except:
                                #self.FilterFrequencyHz_Received = -1
                                pass

                            print("RxMessageString: " + RxMessageString + ", FilterFrequencyHz_Received_Str: " + str(FilterFrequencyHz_Received_Str) + ", len = " + str(len(FilterFrequencyHz_Received_Str)) + ", type = " + str(type(FilterFrequencyHz_Received_Str)))
                            #for i in FilterFrequencyHz_Received_Str:
                            #    print(i)
                            print("FilterFrequencyHz_Received: " + str(self.FilterFrequencyHz_Received))

                            self.FlushSerial_EventNeedsToBeFiredFlag = 1
                        ##########################################################################################################
                        ##########################################################################################################

                        ########################################################################################################## unicorn
                        ##########################################################################################################
                        if len(RxMessage) == NumberOfBytesPerMessage:

                            NewDataFlag = 0

                            ##########################################################################################################
                            if self.StreamingModeString.find("Binary_Simple") != -1:

                                Header_IntegerNoUnits = RxMessage[0]
                                Fx_IntegerNoUnits = (RxMessage[2] << 8) + RxMessage[1]
                                Fy_IntegerNoUnits = (RxMessage[4] << 8) + RxMessage[3]
                                Fz_IntegerNoUnits = (RxMessage[6] << 8) + RxMessage[5]
                                Mx_IntegerNoUnits = (RxMessage[8] << 8) + RxMessage[7]
                                My_IntegerNoUnits = (RxMessage[10] << 8) + RxMessage[9]
                                Mz_IntegerNoUnits = (RxMessage[12] << 8) + RxMessage[11]
                                Status_IntegerNoUnits = RxMessage[13]
                                ChecksumReceived_IntegerNoUnits = RxMessage[14]

                                NewDataFlag = 1

                            ##########################################################################################################

                            ##########################################################################################################
                            elif self.StreamingModeString.find("Binary_Standard") != -1:

                                Header_IntegerNoUnits = RxMessage[0]
                                Fx_IntegerNoUnits = (RxMessage[3] << 16) + (RxMessage[2] << 8) + RxMessage[1]
                                Fy_IntegerNoUnits = (RxMessage[6] << 16) + (RxMessage[5] << 8) + RxMessage[4]
                                Fz_IntegerNoUnits = (RxMessage[9] << 16) + (RxMessage[8] << 8) + RxMessage[7]
                                Mx_IntegerNoUnits = (RxMessage[12] << 16) + (RxMessage[11] << 8) + RxMessage[10]
                                My_IntegerNoUnits = (RxMessage[15] << 16) + (RxMessage[14] << 8) + RxMessage[13]
                                Mz_IntegerNoUnits = (RxMessage[18] << 16) + (RxMessage[17] << 8) + RxMessage[16]
                                Status_IntegerNoUnits = RxMessage[19]
                                ChecksumReceived_IntegerNoUnits = RxMessage[20]

                                NewDataFlag = 1

                            ##########################################################################################################

                            ##########################################################################################################
                            Fx_N = self.ConvertForceFromIntegerToN(Fx_IntegerNoUnits, SimpleFlag=SimpleFlag)
                            Fy_N = self.ConvertForceFromIntegerToN(Fy_IntegerNoUnits, SimpleFlag=SimpleFlag)
                            Fz_N = self.ConvertForceFromIntegerToN(Fz_IntegerNoUnits, SimpleFlag=SimpleFlag)
                            Mx_Nm = self.ConvertMomentFromIntegerToNm(Mx_IntegerNoUnits, SimpleFlag=SimpleFlag)
                            My_Nm = self.ConvertMomentFromIntegerToNm(My_IntegerNoUnits, SimpleFlag=SimpleFlag)
                            Mz_Nm = self.ConvertMomentFromIntegerToNm(Mz_IntegerNoUnits, SimpleFlag=SimpleFlag)
                            ##########################################################################################################

                            ##########################################################################################################
                            Checksum_Computed = 0
                            for Index in range(0, NumberOfBytesPerMessage - 1): #Exclude the "SUM" byte
                                Checksum_Computed = Checksum_Computed + int(RxMessage[Index])

                            Checksum_Computed = (Checksum_Computed & 0x00ff)  # Takes only the bottom byte

                            #print("Checksum_Computed: " + str(Checksum_Computed) + ", ChecksumReceived_IntegerNoUnits: " + str(ChecksumReceived_IntegerNoUnits))

                            if Checksum_Computed == ChecksumReceived_IntegerNoUnits:
                                NewDataFlag = 1
                            else:
                                NewDataFlag = 0
                                self.Checksum_ErrorCounter = self.Checksum_ErrorCounter + 1
                                #print("Canon6dofFTsensorFH30020_ReubenPython3Class: CHECKSUM ERROR") #unicorn
                            ##########################################################################################################

                            ##########################################################################################################
                            if NewDataFlag == 1:
                                self.MostRecentDataDict["Header"] = Header_IntegerNoUnits
                                self.MostRecentDataDict["Fx"] = Fx_N
                                self.MostRecentDataDict["Fy"] = Fy_N
                                self.MostRecentDataDict["Fz"] = Fz_N
                                self.MostRecentDataDict["Mx"] = Mx_Nm
                                self.MostRecentDataDict["My"] = My_Nm
                                self.MostRecentDataDict["Mz"] = Mz_Nm
                                self.MostRecentDataDict["FTlist"] = [Fx_N, Fy_N, Fz_N, Mx_Nm, My_Nm, Mz_Nm]
                                self.MostRecentDataDict["Status"] = Status_IntegerNoUnits


                                self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedRxThread
                                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedTxThread

                                self.MostRecentDataDict["ResetTare_EventHasHappenedFlag"] = self.ResetTare_EventHasHappenedFlag

                                self.MostRecentDataDict["Checksum_ErrorCounter"] = self.Checksum_ErrorCounter

                                self.MostRecentDataDict["FilterFrequencyHz_Received"] = self.FilterFrequencyHz_Received
                            ##########################################################################################################

                            ##########################################################################################################
                            self.UpdateFrequencyCalculation_DedicatedRxThread_Filtered()
                            ##########################################################################################################

                            ##########################################################################################################
                            if self.DedicatedRxThread_TimeToSleepEachLoop > 0.0:
                                if self.DedicatedRxThread_TimeToSleepEachLoop > 0.001:
                                    time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                                else:
                                    time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop)
                            ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        else:
                            if self.PrintAllReceivedSerialMessageForDebuggingFlag == 1:
                                print("RxMessage Len = " + str(len(RxMessage)),
                                      ", ByteLen = " + str(len(RxMessage)) +
                                      ", Message = " + str(RxMessage))
                        ##########################################################################################################
                        ##########################################################################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("DedicatedRxThread, RxMessage: " + str(RxMessage) + ", Exceptions: %s" % exceptions)
                    traceback.print_exc()
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedRxThread, Exceptions: %s" % exceptions)
                #traceback.print_exc()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedRxThread for Canon6dofFTsensorFH30020_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Canon6dofFTsensorFH30020_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for Canon6dofFTsensorFH30020_ReubenPython3Class object.")

        #################################################
        #################################################
        self.root = parent
        self.parent = parent
        #################################################
        #################################################

        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################

        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLabelWidth = 30
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                        "\nUSBtoSerialConverter Serial Number: " + str(self.DesiredSerialNumber_USBtoSerialConverter)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=0, column=1, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ButtonsFrame = Frame(self.myFrame)
        self.ButtonsFrame.grid(row = 1, column = 0, padx = 10, pady = 10, rowspan = 1, columnspan = 2)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ResetTare_Button = Button(self.ButtonsFrame, text="Reset Tare", state="normal", width=20, bg=self.TKinter_LightYellowColor, command=lambda: self.ResetTare_Button_Response())
        self.ResetTare_Button.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################
        
        #################################################
        #################################################
        self.FlushSerial_Button = Button(self.ButtonsFrame, text="Flush Serial", state="normal", width=20, command=lambda: self.FlushSerial_Button_Response())
        self.FlushSerial_Button.grid(row=0, column=1, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################
        
        #################################################
        #################################################
        self.SetFilterFrequencyCutoffHz_Button = Button(self.ButtonsFrame, text="SetFilterHz", state="normal", width=20, command=lambda: self.SetFilterFrequencyCutoffHz_Button_Response())
        self.SetFilterFrequencyCutoffHz_Button.grid(row=0, column=2, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
        #################################################
        #################################################

        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTare_Button_Response(self):

        self.ResetTare_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ResetTare_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FlushSerial_Button_Response(self):

        self.FlushSerial_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("FlushSerial_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetFilterFrequencyCutoffHz_Button_Response(self):

        self.SetFilterFrequencyCutoffHz_EventNeedsToBeFiredFlag = 1
        self.SetFilterFrequencyCutoffHz_EventHasHappenedFlag = 0

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                    NumberOfDecimalsPlaceToUse = 5,
                                                                                                    NumberOfEntriesPerLine = 1,
                                                                                                    NumberOfTabsBetweenItems = 3)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Canon6dofFTsensorFH30020_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
            ##########################################################################################################

            ##########################################################################################################
            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0
            ##########################################################################################################

        return ProperlyFormattedStringForPrinting
    ##########################################################################################################
    ##########################################################################################################
