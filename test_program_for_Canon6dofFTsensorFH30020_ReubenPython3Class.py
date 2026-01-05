# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 01/05/2026

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm (may work on Mac in non-GUI mode, but haven't tested yet).
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
##########################################

##########################################
from Canon6dofFTsensorFH30020_ReubenPython3Class import *
from CSVdataLogger_ReubenPython3Class import *
from EntryListWithBlinking_ReubenPython2and3Class import *
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import math
import traceback
import keyboard
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

##########################################################################################################
##########################################################################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global Canon6dofFTsensorFH30020_Object
    global Canon6dofFTsensorFH30020_OPEN_FLAG
    global SHOW_IN_GUI_Canon6dofFTsensorFH30020_FLAG
    global Canon6dofFTsensorFH30020_MostRecentDict
    global Canon6dofFTsensorFH30020_MostRecentDict_Label

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:

        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            Canon6dofFTsensorFH30020_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(Canon6dofFTsensorFH30020_MostRecentDict, NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=3, NumberOfTabsBetweenItems=1)
            #########################################################

            #########################################################
            if Canon6dofFTsensorFH30020_OPEN_FLAG == 1 and SHOW_IN_GUI_Canon6dofFTsensorFH30020_FLAG == 1:
                Canon6dofFTsensorFH30020_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if EntryListWithBlinking_OPEN_FLAG == 1:
                EntryListWithBlinking_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_Object.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_MostRecentDict_IsSavingFlag

    print("ExitProgram_Callback event fired!")

    if CSVdataLogger_MostRecentDict_IsSavingFlag == 0:
        EXIT_PROGRAM_FLAG = 1
    else:
        print("ExitProgram_Callback, ERROR! Still saving data.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    global Canon6dofFTsensorFH30020_Object
    global Canon6dofFTsensorFH30020_OPEN_FLAG

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_Canon6dofFTsensorFH30020
    global Tab_MyPrint
    global Tab_CSVdataLogger

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_Canon6dofFTsensorFH30020 = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_Canon6dofFTsensorFH30020, text='   FT   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_Canon6dofFTsensorFH30020 = root
        Tab_MyPrint = root
        Tab_CSVdataLogger = root
        #################################################

    ##########################################################################################################

    #################################################
    #################################################
    global Canon6dofFTsensorFH30020_MostRecentDict_Label
    Canon6dofFTsensorFH30020_MostRecentDict_Label = Label(Tab_MainControls, text="Canon6dofFTsensorFH30020_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    Canon6dofFTsensorFH30020_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ButtonsFrame
    ButtonsFrame = Frame(Tab_MainControls)
    ButtonsFrame.grid(row = 1, column = 0, padx = 10, pady = 10, rowspan = 1, columnspan = 1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ResetTare_Button
    ResetTare_Button = Button(ButtonsFrame, text="Reset Tare", state="normal", width=20, command=lambda: ResetTare_Button_Response())
    #ResetTare_Button.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    if Canon6dofFTsensorFH30020_OPEN_FLAG == 1:
        Canon6dofFTsensorFH30020_Object.CreateGUIobjects(TkinterParent=Tab_Canon6dofFTsensorFH30020)
    #################################################
    #################################################

    #################################################
    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.CreateGUIobjects(TkinterParent=Tab_MainControls)
    #################################################
    #################################################

    #########################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.CreateGUIobjects(TkinterParent=Tab_CSVdataLogger)
    #################################################
    #################################################

    #########################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.CreateGUIobjects(TkinterParent=Tab_MyPrint)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ResetTare_Button_Response():
    global ResetTare_EventNeedsToBeFiredFlag

    ResetTare_EventNeedsToBeFiredFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 0

    global USE_Canon6dofFTsensorFH30020_FLAG
    USE_Canon6dofFTsensorFH30020_FLAG = 1

    global USE_EntryListWithBlinking_FLAG
    USE_EntryListWithBlinking_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_Canon6dofFTsensorFH30020_FLAG
    SHOW_IN_GUI_Canon6dofFTsensorFH30020_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1

    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_Canon6dofFTsensorFH30020
    global GUI_COLUMN_Canon6dofFTsensorFH30020
    global GUI_PADX_Canon6dofFTsensorFH30020
    global GUI_PADY_Canon6dofFTsensorFH30020
    global GUI_ROWSPAN_Canon6dofFTsensorFH30020
    global GUI_COLUMNSPAN_Canon6dofFTsensorFH30020
    GUI_ROW_Canon6dofFTsensorFH30020 = 0

    GUI_COLUMN_Canon6dofFTsensorFH30020 = 0
    GUI_PADX_Canon6dofFTsensorFH30020 = 1
    GUI_PADY_Canon6dofFTsensorFH30020 = 1
    GUI_ROWSPAN_Canon6dofFTsensorFH30020 = 1
    GUI_COLUMNSPAN_Canon6dofFTsensorFH30020 = 1

    global GUI_ROW_EntryListWithBlinking
    global GUI_COLUMN_EntryListWithBlinking
    global GUI_PADX_EntryListWithBlinking
    global GUI_PADY_EntryListWithBlinking
    global GUI_ROWSPAN_EntryListWithBlinking
    global GUI_COLUMNSPAN_EntryListWithBlinking
    GUI_ROW_EntryListWithBlinking = 1

    GUI_COLUMN_EntryListWithBlinking = 0
    GUI_PADX_EntryListWithBlinking = 1
    GUI_PADY_EntryListWithBlinking = 1
    GUI_ROWSPAN_EntryListWithBlinking = 1
    GUI_COLUMNSPAN_EntryListWithBlinking = 1

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 2

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 3

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1100

    global root_height
    root_height = 1080

    global TabControlObject
    global Tab_MainControls
    global Tab_Canon6dofFTsensorFH30020
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global ResetTare_EventNeedsToBeFiredFlag
    ResetTare_EventNeedsToBeFiredFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global Canon6dofFTsensorFH30020_Object

    global Canon6dofFTsensorFH30020_OPEN_FLAG
    Canon6dofFTsensorFH30020_OPEN_FLAG = 0

    global Canon6dofFTsensorFH30020_MostRecentDict
    Canon6dofFTsensorFH30020_MostRecentDict = dict()

    global Canon6dofFTsensorFH30020_MostRecentDict_Time
    Canon6dofFTsensorFH30020_MostRecentDict_Time = 0.0

    global Canon6dofFTsensorFH30020_MostRecentDict_FTlist
    Canon6dofFTsensorFH30020_MostRecentDict_FTlist = [-11111.0]*6
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_Object

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0

    global CSVdataLogger_MostRecentDict_IsSavingFlag
    CSVdataLogger_MostRecentDict_IsSavingFlag = 0
    #################################################
    #################################################

    ####################################################
    ####################################################
    global LowPassFilterForDictsOfLists_Object

    global LowPassFilterForDictsOfLists_OPEN_FLAG
    LowPassFilterForDictsOfLists_OPEN_FLAG = -1

    global LowPassFilterForDictsOfLists_MostRecentDict
    LowPassFilterForDictsOfLists_MostRecentDict = dict()

    global FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda
    FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda = 0.98
    
    global Raw_1
    Raw_1 = 0.0

    global Filtered_1
    Filtered_1 = 0.0
    ####################################################
    ####################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object

    global EntryListWithBlinking_OPEN_FLAG
    EntryListWithBlinking_OPEN_FLAG = -1

    global EntryListWithBlinking_MostRecentDict
    EntryListWithBlinking_MostRecentDict = dict()

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber = 0

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = -1

    EntryWidth = 10
    LabelWidth = 40
    FontSize = 8
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_Object

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global Canon6dofFTsensorFH30020_GUIparametersDict
    Canon6dofFTsensorFH30020_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_Canon6dofFTsensorFH30020_FLAG),
                                                        ("EnableInternal_MyPrint_Flag", 0),
                                                        ("NumberOfPrintLines", 10),
                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                        ("GUI_ROW", GUI_ROW_Canon6dofFTsensorFH30020),
                                                        ("GUI_COLUMN", GUI_COLUMN_Canon6dofFTsensorFH30020),
                                                        ("GUI_PADX", GUI_PADX_Canon6dofFTsensorFH30020),
                                                        ("GUI_PADY", GUI_PADY_Canon6dofFTsensorFH30020),
                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_Canon6dofFTsensorFH30020),
                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_Canon6dofFTsensorFH30020)])

    global Canon6dofFTsensorFH30020_SetupDict
    Canon6dofFTsensorFH30020_SetupDict = dict([("GUIparametersDict", Canon6dofFTsensorFH30020_GUIparametersDict),
                                                ("DesiredSerialNumber_USBtoSerialConverter", "FT8J3FOOA"), #FT8J3FOOA #FT8J8TNUA
                                                ("SerialBaudRate", 115200), #[57600, 115200, 921600], A continuous output cycle changes according to a baud rate. 921600 bps: 2kHz, 115200bps:250Hz, 57600bps:125Hz.
                                                ("NameToDisplay_UserSet", "Canon6dofFTsensorFH30020"),
                                                ("DedicatedRxThread_TimeToSleepEachLoop", 0.001),
                                                ("DedicatedTxThread_TimeToSleepEachLoop", 0.010),
                                                ("DedicatedTxThread_TxMessageToSend_Queue_MaxSize", 1),
                                                ("ResetTareAtStartOfProgramFlag", 1),
                                                ("StreamingModeString", "Binary_Standard_Oneshot"), #Binary_Standard_Oneshot, #Binary_Standard_Continuous
                                                ("FilterFrequencyCutoffHz", 100)]) # 1, 5, 10, 50, 100, 500, 1000, 5000

    if USE_Canon6dofFTsensorFH30020_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            Canon6dofFTsensorFH30020_Object = Canon6dofFTsensorFH30020_ReubenPython3Class(Canon6dofFTsensorFH30020_SetupDict)
            Canon6dofFTsensorFH30020_OPEN_FLAG = Canon6dofFTsensorFH30020_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("Canon6dofFTsensorFH30020_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################
    
    #################################################
    #################################################
    if USE_Canon6dofFTsensorFH30020_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if Canon6dofFTsensorFH30020_OPEN_FLAG != 1:
                print("Failed to open Canon6dofFTsensorFH30020_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global CSVdataLogger_GUIparametersDict
    CSVdataLogger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                            ("EnableInternal_MyPrint_Flag", 1),
                                            ("NumberOfPrintLines", 10),
                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                            ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                            ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                            ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                            ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                            ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    CSVdataLogger_SetupDict_VariableNamesForHeaderList = ["Time (S)",
                                                        "Fx (N)",
                                                        "Fy (N)",
                                                        "Fz (N)",
                                                        "Mx (Nm)",
                                                        "My (Nm)",
                                                        "Mz (Nm)"]

    print("CSVdataLogger_SetupDict_VariableNamesForHeaderList: " + str(CSVdataLogger_SetupDict_VariableNamesForHeaderList))

    global CSVdataLogger_SetupDict
    CSVdataLogger_SetupDict = dict([("GUIparametersDict", CSVdataLogger_GUIparametersDict),
                                    ("NameToDisplay_UserSet", "CSVdataLogger"),
                                    ("CSVfile_DirectoryPath", "C:\\CSVfiles"),
                                    ("FileNamePrefix", "CSV_file_"),
                                    ("VariableNamesForHeaderList", CSVdataLogger_SetupDict_VariableNamesForHeaderList),
                                    ("MainThread_TimeToSleepEachLoop", 0.002),
                                    ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_Object = CSVdataLogger_ReubenPython3Class(CSVdataLogger_SetupDict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ####################################################
    ####################################################
    try:
        global LowPassFilterForDictsOfLists_DictOfVariableFilterSettings
        LowPassFilterForDictsOfLists_DictOfVariableFilterSettings = dict([("FTlist", dict([("UseMedianFilterFlag", 0),
                                                                                              ("UseExponentialSmoothingFilterFlag", 1),
                                                                                              ("ExponentialSmoothingFilterLambda", FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda)]))]) #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        LowPassFilterForDictsOfLists_SetupDict = dict([("DictOfVariableFilterSettings", LowPassFilterForDictsOfLists_DictOfVariableFilterSettings)])

        LowPassFilterForDictsOfLists_Object = LowPassFilterForDictsOfLists_ReubenPython2and3Class(LowPassFilterForDictsOfLists_SetupDict)
        LowPassFilterForDictsOfLists_OPEN_FLAG = LowPassFilterForDictsOfLists_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

    except:
        exceptions = sys.exc_info()[0]
        print("LowPassFilterForDictsOfLists_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
    ####################################################
    ####################################################

    #################################################
    #################################################
    if 1:
        if EXIT_PROGRAM_FLAG == 0:
            if LowPassFilterForDictsOfLists_OPEN_FLAG != 1:
                print("Failed to open LowPassFilterForDictsOfLists_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global EntryListWithBlinking_GUIparametersDict
    EntryListWithBlinking_GUIparametersDict = dict([("UseBorderAroundThisGuiObjectFlag", 0),
                                                    ("GUI_ROW", GUI_ROW_EntryListWithBlinking),
                                                    ("GUI_COLUMN", GUI_COLUMN_EntryListWithBlinking),
                                                    ("GUI_PADX", GUI_PADX_EntryListWithBlinking),
                                                    ("GUI_PADY", GUI_PADY_EntryListWithBlinking),
                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_EntryListWithBlinking),
                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_EntryListWithBlinking)])

    global EntryListWithBlinking_Variables_ListOfDicts
    EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda"),
                                                         ("Type", "float"),
                                                         ("StartingVal", FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda),
                                                         ("MinVal", 0.0),
                                                         ("MaxVal", 1.0),
                                                         ("EntryBlinkEnabled", 0),
                                                         ("EntryWidth", EntryWidth),
                                                         ("LabelWidth", LabelWidth),
                                                         ("FontSize", FontSize)])]

    global EntryListWithBlinking_SetupDict
    EntryListWithBlinking_SetupDict = dict([("GUIparametersDict", EntryListWithBlinking_GUIparametersDict),
                                          ("EntryListWithBlinking_Variables_ListOfDicts", EntryListWithBlinking_Variables_ListOfDicts),
                                          ("DebugByPrintingVariablesFlag", 0),
                                          ("LoseFocusIfMouseLeavesEntryFlag", 0)])
    
    if USE_EntryListWithBlinking_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            EntryListWithBlinking_Object = EntryListWithBlinking_ReubenPython2and3Class(EntryListWithBlinking_SetupDict)
            EntryListWithBlinking_OPEN_FLAG = EntryListWithBlinking_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_Object __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_EntryListWithBlinking_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if EntryListWithBlinking_OPEN_FLAG != 1:
                print("Failed to open EntryListWithBlinking_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPrint_GUIparametersDict
    MyPrint_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_SetupDict
    MyPrint_SetupDict = dict([("NumberOfPrintLines", 10),
                            ("WidthOfPrintingLabel", 200),
                            ("PrintToConsoleFlag", 1),
                            ("LogFileNameFullPath", os.path.join(os.getcwd(), "TestLog.txt")),
                            ("GUIparametersDict", MyPrint_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_SetupDict)
            MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("GraphCanvasWidth", 900),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GraphCanvasWindowTitle", "Canon6dofFTsensorFH30020_ReubenPython3Class"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])


    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Fx_N", "Fy_N", "Fz_N", "Mx_Nm", "My_Nm", "Mz_Nm"]),
                                                                                                        ("MarkerSizeList", [2]*6),
                                                                                                        ("LineWidthList", [2]*6),
                                                                                                        ("IncludeInXaxisAutoscaleCalculationList", [1]*6),
                                                                                                        ("IncludeInYaxisAutoscaleCalculationList", [1]*6),
                                                                                                        ("ColorList", ["Red", "Green", "Blue", "Black", "Purple", "Orange"])])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 100),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 5.0),
                                                            ("Y_min", -5.0),
                                                            ("Y_max", 5.0),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("GraphNumberOfLeadingZeros", 0),
                                                            ("GraphNumberOfDecimalPlaces", 3),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder")),
                                                            ("KeepPlotterWindowAlwaysOnTopFlag", 0),
                                                            ("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", 0),
                                                            ("AllowResizingOfWindowFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
        Tab_MainControls = None
        Tab_Canon6dofFTsensorFH30020 = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("Starting main loop 'test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if CSVdataLogger_OPEN_FLAG == 1:

            CSVdataLogger_MostRecentDict = CSVdataLogger_Object.GetMostRecentDataDict()

            if "Time" in CSVdataLogger_MostRecentDict:
                CSVdataLogger_MostRecentDict_Time = CSVdataLogger_MostRecentDict["Time"]
                CSVdataLogger_MostRecentDict_IsSavingFlag = CSVdataLogger_MostRecentDict["IsSavingFlag"]
                #print("CSVdataLogger_MostRecentDict: " + str(CSVdataLogger_MostRecentDict))
        ###################################################
        ###################################################

        #################################################### GET's
        ####################################################

        ###################################################
        if EntryListWithBlinking_OPEN_FLAG == 1:

            EntryListWithBlinking_MostRecentDict = EntryListWithBlinking_Object.GetMostRecentDataDict()

            if "DataUpdateNumber" in EntryListWithBlinking_MostRecentDict and EntryListWithBlinking_MostRecentDict["DataUpdateNumber"] != EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last:
                EntryListWithBlinking_MostRecentDict_DataUpdateNumber = EntryListWithBlinking_MostRecentDict["DataUpdateNumber"]
                #print("DataUpdateNumber = " + str(EntryListWithBlinking_MostRecentDict_DataUpdateNumber) + ", EntryListWithBlinking_MostRecentDict: " + str(EntryListWithBlinking_MostRecentDict))

                if EntryListWithBlinking_MostRecentDict_DataUpdateNumber > 1:
                    FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda = EntryListWithBlinking_MostRecentDict["FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda"]

                    if LowPassFilterForDictsOfLists_OPEN_FLAG == 1:
                        LowPassFilterForDictsOfLists_DictOfVariableFilterSettings["FTlist"]["ExponentialSmoothingFilterLambda"] = FTlist_LowPassFilterForDictsOfLists_ExponentialSmoothingFilterLambda
                        LowPassFilterForDictsOfLists_Object.AddOrUpdateDictOfVariableFilterSettingsFromExternalProgram(LowPassFilterForDictsOfLists_DictOfVariableFilterSettings)

        ###################################################

        ###################################################
        EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = EntryListWithBlinking_MostRecentDict_DataUpdateNumber
        ###################################################

        ####################################################
        ####################################################

        ################################################### GET's
        ###################################################
        if Canon6dofFTsensorFH30020_OPEN_FLAG == 1:

            Canon6dofFTsensorFH30020_MostRecentDict = Canon6dofFTsensorFH30020_Object.GetMostRecentDataDict()
            #print("Canon6dofFTsensorFH30020_MostRecentDict: " + str(Canon6dofFTsensorFH30020_MostRecentDict))

            if "Time" in Canon6dofFTsensorFH30020_MostRecentDict:
                Canon6dofFTsensorFH30020_MostRecentDict_Time = Canon6dofFTsensorFH30020_MostRecentDict["Time"]
                Canon6dofFTsensorFH30020_MostRecentDict_FTlist = Canon6dofFTsensorFH30020_MostRecentDict["FTlist"]
                #print("Time: " + str(Canon6dofFTsensorFH30020_MostRecentDict_Time) + ", FTlist: " + str(Canon6dofFTsensorFH30020_MostRecentDict_FTlist))

        ###################################################
        ###################################################

        #################################################### GET's
        ####################################################
        if LowPassFilterForDictsOfLists_OPEN_FLAG == 1:

            LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("FTlist", Canon6dofFTsensorFH30020_MostRecentDict_FTlist)])) #Update data

            LowPassFilterForDictsOfLists_MostRecentDict = LowPassFilterForDictsOfLists_Object.GetMostRecentDataDict() #Get latest data
            #print("LowPassFilterForDictsOfLists_MostRecentDict: " + str(LowPassFilterForDictsOfLists_MostRecentDict))

            if "FTlist" in LowPassFilterForDictsOfLists_MostRecentDict:
                Raw_1 = LowPassFilterForDictsOfLists_MostRecentDict["FTlist"]["Raw_MostRecentValuesList"]
                Filtered_1 = LowPassFilterForDictsOfLists_MostRecentDict["FTlist"]["Filtered_MostRecentValuesList"]

        ####################################################
        ####################################################

        ################################################### SET's
        ###################################################
        if Canon6dofFTsensorFH30020_OPEN_FLAG == 1:

            if ResetTare_EventNeedsToBeFiredFlag == 1:
                Canon6dofFTsensorFH30020_Object.ResetTare()
                ResetTare_EventNeedsToBeFiredFlag = 0

        ###################################################
        ###################################################

        #################################################### SET's
        ####################################################
        if Canon6dofFTsensorFH30020_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1:

            ####################################################
            ListToWrite = []
            ListToWrite.append(CurrentTime_MainLoopThread)

            for Index in range(0, 6):
                ListToWrite.append(Canon6dofFTsensorFH30020_MostRecentDict_FTlist[Index])
            ####################################################

            CSVdataLogger_Object.AddDataToCSVfile_ExternalFunctionCall(ListToWrite)
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
            try:
                ####################################################
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"]/1000.0 + 0.001:
                            
                            MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Fx_N", "Fy_N", "Fz_N"],
                                                                                                            [CurrentTime_MainLoopThread]*3,
                                                                                                            [Canon6dofFTsensorFH30020_MostRecentDict_FTlist[0], 
                                                                                                             Canon6dofFTsensorFH30020_MostRecentDict_FTlist[1], 
                                                                                                             Canon6dofFTsensorFH30020_MostRecentDict_FTlist[2]])

                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class, if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1: SET's, Exceptions: %s" % exceptions)
                # traceback.print_exc()
        ####################################################
        ####################################################

        time.sleep(0.003)
        
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_Canon6dofFTsensorFH30020_ReubenPython3Class.")

    #################################################
    if Canon6dofFTsensorFH30020_OPEN_FLAG == 1:
        Canon6dofFTsensorFH30020_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if LowPassFilterForDictsOfLists_OPEN_FLAG == 1:
        LowPassFilterForDictsOfLists_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################