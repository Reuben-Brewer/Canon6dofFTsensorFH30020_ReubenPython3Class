# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 11/08/2023

Verified working on: Python 3.8 for Windows 8.1, 10, and 11 64-bit (haven't tested on Ubuntu, Raspberry Pi, or Mac yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import traceback
import time
import datetime
from collections import OrderedDict
from copy import deepcopy
import glob #For getting a list of files in a directory with a certain extension

import pandas
#########################################################

#########################################################
import win32com.client #for commanding Excel as a program
#########################################################

#########################################################
#For writing excel files.
import xlwt
#########################################################

#########################################################
#For copying excel file when we create the excel file. HAVE TO INSTALL SEPARATELY FROM XLWT/XLRD.
from xlutils.copy import copy
#########################################################

#########################################################
#http://xlsxwriter.readthedocs.io/chart.html FOR MAKING CHARTS
#XlsxWriter can only create new files. It cannot read or modify existing files. Can only handle xlsx files, not xls
import xlsxwriter
#########################################################

##########################################################################################################
##########################################################################################################
def OpenXLSsndCopyDataToLists(FileName_full_path):

    DataOrderedDict = OrderedDict()

    try:

        ##########################################################################################################
        workbook = pandas.ExcelFile(FileName_full_path)

        sheet = workbook.parse("Sheet1")

        NumberOfRows = sheet.shape[0]
        #print("NumberOfRows: " + str(NumberOfRows))

        NumberOfColumns = sheet.shape[1]
        #print("NumberOfColumns: " + str(NumberOfColumns))

        header_variable_name_list = sheet.columns.values.tolist()
        print("Detected the following variable names: " + str(header_variable_name_list))
        ##########################################################################################################

        ##########################################################################################################
        #DataFrame.at, Access a single value for a row/column pair by label.
        #DataFrame.iat, Access a single value for a row/column pair by integer position.

        ListOfColumnDataLists = []
        for column in range(0, NumberOfColumns):  # Iterate through columns
            ListOfColumnDataLists.append([])
        ##########################################################################################################

        ##########################################################################################################
        for row in range(0, NumberOfRows): # Iterate through rows
            for column in range(0, NumberOfColumns):  # Iterate through columns
                cell_value = sheet.iat[row, column]  # Get cell object by row, col
                ListOfColumnDataLists[column].append(cell_value)
        ##########################################################################################################

        ##########################################################################################################
        for column in range(0, NumberOfColumns):  # Iterate through columns
            DataOrderedDict[header_variable_name_list[column]] = ListOfColumnDataLists[column]
        ##########################################################################################################

        return DataOrderedDict

    except:
        exceptions = sys.exc_info()[0]
        print("OpenXLSsndCopyDataToLists, exceptions: %s" % exceptions)
        traceback.print_exc()
        return DataOrderedDict

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def CreateExcelChart(FileName_to_save_full_path, DataOrderedDictToWrite):

    #print("FileName_to_save_full_path: " + FileName_to_save_full_path)

    workbook = xlsxwriter.Workbook(FileName_to_save_full_path)
    worksheet = workbook.add_worksheet()

    ##########################################################################################################
    alphabetString = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    numerical_index = 0
    NumberOfDataRows = -1
    for key in DataOrderedDictToWrite:
        starting_cell_string_identifier = alphabetString[numerical_index] + "1"
        #print("DataOrderedDictToWrite[key]: " + str(DataOrderedDictToWrite[key]))
        worksheet.write_column(starting_cell_string_identifier, [key] + DataOrderedDictToWrite[key]) #
        NumberOfDataRows = len(DataOrderedDictToWrite[key])
        worksheet.set_column(numerical_index, numerical_index, 20) #set column width of current column to 20
        numerical_index = numerical_index + 1
    ##########################################################################################################

    Time_ExcelColumnLetter = "A"

    SumOfForcesFromAllSensors_ExcelColumnLetter = "B"

    Force0_ExcelColumnLetter = "C"

    Force1_ExcelColumnLetter = "D"

    Force2_ExcelColumnLetter = "E"

    SumOfForceDerivativesFromAllSensors_ExcelColumnLetter = "F"

    ForceDerivative0_ExcelColumnLetter = "G"

    ForceDerivative1_ExcelColumnLetter = "H"

    ForceDerivative2_ExcelColumnLetter = "I"

    SumOfAllForces_vs_Time_Xaxis_Chart_sheet = workbook.add_chartsheet("SumOfForces_vs_Time")
    SumOfAllForces_vs_Time_Xaxis_Chart = workbook.add_chart({'type': 'scatter'}) #http://xlsxwriter.readthedocs.io/example_chart_scatter.html
    SumOfAllForces_vs_Time_Xaxis_Chart.add_series({'name': 'SumOfForcesFromAllSensors_vs_Time','categories': "=Sheet1!$" + Time_ExcelColumnLetter + "$2:$" + Time_ExcelColumnLetter + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + SumOfForcesFromAllSensors_ExcelColumnLetter + "$2:$" + SumOfForcesFromAllSensors_ExcelColumnLetter + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
    SumOfAllForces_vs_Time_Xaxis_Chart.set_title ({'name': 'SumOfForcesFromAllSensors vs Time'})
    SumOfAllForces_vs_Time_Xaxis_Chart.set_x_axis({'name': 'Time'})
    SumOfAllForces_vs_Time_Xaxis_Chart.set_y_axis({'name': 'SumOfForcesFromAllSensors (lb)'})
    SumOfAllForces_vs_Time_Xaxis_Chart_sheet.set_chart(SumOfAllForces_vs_Time_Xaxis_Chart)

    workbook.close()
    time.sleep(0.05)

    pywin32_FileName_xls = FileName_to_save_full_path
    pywin32_FileName_xls = pywin32_FileName_xls.replace("/", "\\") #This line is needed or else the Excel file will give you an error.

    xl = win32com.client.Dispatch("Excel.Application")
    xl.DisplayAlerts = False
    wb = xl.Workbooks.Open(pywin32_FileName_xls)
    wb.SaveAs(pywin32_FileName_xls, FileFormat = 56)
    wb.Close()
    xl.Quit()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def animate(i):
    global DataOrderedDictFromOriginalFile
    global line

    line.set_data(DataOrderedDictFromOriginalFile["x"][i], DataOrderedDictFromOriginalFile["y"][i], DataOrderedDictFromOriginalFile["z"][i])  # update the data.

    return line
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    global DataOrderedDictFromOriginalFile
    global line

    global FileDirectory

    ##########################################################################################################
    try:
        if len(sys.argv) >= 2:
            ARGV_1 = sys.argv[1]

            print("ARGV_1: " + str(ARGV_1))
            FileDirectory = ARGV_1

        else:
            FileDirectory = os.getcwd() + "\\CSVfiles"

    except:
        exceptions = sys.exc_info()[0]
        print("Parsing ARGV_1, exceptions: %s" % exceptions, 0)
        traceback.print_exc()

    print("Using FileDirectory = " + str(FileDirectory))
    ##########################################################################################################

    ##########################################################################################################

    #########################################################
    print("$$$$$$$$$$$$$$$$")
    print("RUN THIS PROGRAM FROM COMMAND LINE LIKE THIS: 'python ExcelPlot_CSVdataLogger_ReubenPython3Code.py CSV-FILE-DIRECTORY-FULL-PATH'")
    print("$$$$$$$$$$$$$$$$")
    #########################################################

    #########################################################
    if FileDirectory.find(":") == -1:
        print("ERROR: You must specify the FULL path, starting from the disk drive like 'C:'")
        exit()()
    #########################################################

    #########################################################
    FileSuffixForChartFile = "_with_chart.xls"

    FileList_csv = glob.glob(FileDirectory + '/*.csv')
    FileList_xls = glob.glob(FileDirectory + '/*.xls')

    print("Found " + str(len(FileList_csv)) + " .csv files and " + str(len(FileList_xls)) + " .xls files.")
    #print("FileList_csv: " + str(FileList_csv))
    #print("FileList_xls: " + str(FileList_xls))
    #########################################################
    
    ##########################################################################################################
    for FileName_csv in FileList_csv:
        FileName_xls = FileName_csv.replace(".csv", ".xls")
        FileName_WITH_CHART_xls = FileName_csv.replace(".csv", FileSuffixForChartFile)

        ################################
        if FileName_xls not in FileList_xls: #Make sure we haven't already converted this csv to a xls file.
            print("Converting CSV file to xls file for " + FileName_csv)
            read_file = pandas.read_csv(FileName_csv)
            read_file.to_excel(FileName_xls, index=None, header=True, engine="xlsxwriter")
        else:
            print("xls file '" + FileName_xls + "' already exists so skipping csv-xls conversion.")
        ################################

        ################################
        if FileName_WITH_CHART_xls not in FileList_xls: #Make sure we haven't already created a chart file for this csv.

            print("Creating xls chart file for " + FileName_csv)

            DataOrderedDictFromOriginalFile = OpenXLSsndCopyDataToLists(FileName_xls)

            CreateExcelChart(FileName_WITH_CHART_xls, DataOrderedDictFromOriginalFile)

        else:
            print("xls chart file already exists so skipping for " + FileName_csv)
        ################################


    ##########################################################################################################

##########################################################################################################
##########################################################################################################

