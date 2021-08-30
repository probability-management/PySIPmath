# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 21:26:21 2021

SIPLibrary Generator

This Python script allows a user to easily output SIPs that are created
in Python as a dataframe to Excel users.  The output is an Excel .xlsx file
that is readable as a SIPmath Tools library file.  

This version requires the SIP data to be provided as a single dataframe
without metadata.  Metadata can be provided separately as an optional argument
to create a SIPmath Tools library file containing metadata.

This script requires that 'numpy' be installed within the Python
environment you are running the script in.

This file contains the following function:
    
    * SIPLibraryGenerator - returns completion notification with file output to WD

Parameters
        ----------
        SIPdata : df
            Dataframe of SIPs without metadata
        file_name : str
            The name of the output file ending in .xlsx
        author : str
            The name of the author
        SIPmetadata : df, optional
            Dataframe of the SIP metadata

@author: Shaun Doheney
"""

import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_range_abs

def SIP2library(SIPdata, file_name, author, SIPmetadata = []):

    # We probably need to add a check here to ensure that data are valid
    # And that the SIP dataframe does not contain metadata
    # but here goes version 1...    
    df_int = SIPdata
    
    # Ensure that the index names are defined as trial names starting at 1
    df_int.index = np.arange(1, len(df_int) + 1)
    
    # The number of trials (rows) in the data
    N = len(df_int)
    
    # Do we have metadata to include?
    # If so, how many rows of metadata are there?
    df_meta = SIPmetadata
    metadata = len(df_meta)
    df = df_int.append(df_meta)

    # Now we are ready to start building the XLSX SIP Library worksheet
    PM_Lib_Provenance = author
    workbookname = file_name
    workbook = xlsxwriter.Workbook(workbookname)
    worksheet = workbook.add_worksheet('Library')
    worksheet.write('A1', 'PM_Trials')
    worksheet.write('B1', N)
    worksheet.write('A2', 'PM_Lib_Provenance')
    worksheet.write('B2', PM_Lib_Provenance)

    # Only if there is metadata included
    if len(df_meta) > 0:
        worksheet.write(3, 3, 'Meta Data')
        worksheet.write(3, 4, 'Index')
        metaoffsetrow = 4
        metaoffsetcol = 3
        
        # Write metadata labels
        for i in range(metadata):
            worksheet.write(i + metaoffsetrow, metaoffsetcol, df.index[N + i])
    
        # Write metadata index value
        for i in range(metadata):
            worksheet.write(i + metaoffsetrow, metaoffsetcol + 1, N + i + 1)
    
    # Now start entering the SIP data
    offsetrow = metadata + 6
    offsetcol = 1
    
    # Write the indices for the SIP data
    format1 = workbook.add_format({'num_format': '@'})
    for i in range(len(df)):
        worksheet.write(i + offsetrow, offsetcol, df.index[i], format1)
    
    # Write the SIP Names
    for i in range(len(df.columns)):
        worksheet.write(offsetrow - 1, i + offsetcol+1, df.columns[i], format1)
    
    # Write the SIP data
    for i in range(len(df)):
        for j in range(len(df.columns)):
            worksheet.write(i + offsetrow, j+offsetcol+1, df.iloc[i][j])
            
    # Finally, define some global/workbook names.
    workbook.define_name('PM_Trials', '=Library!$B$1')
    workbook.define_name('PM_Lib_Provenance', '=Library!$B$2')
    if len(df_meta) > 0:
        cell_range1 = xl_range_abs(metaoffsetrow, metaoffsetcol,
                                   metaoffsetrow + metadata - 1, metaoffsetcol)
        cell_range2 = "=Library!"+cell_range1 # I'm sure there's a better way, but it works
        workbook.define_name('PM_Meta', cell_range2)
        cell_range3 = xl_range_abs(metaoffsetrow, metaoffsetcol + 1,
                                   metaoffsetrow + metadata - 1, metaoffsetcol + 1)
        cell_range4 = "=Library!"+cell_range3 # I'm sure there's a better way, but it works
        workbook.define_name('PM_Meta_Index', cell_range4)

    for i in range(len(df.columns)):
        cell_range5 = xl_range_abs(offsetrow, offsetcol + 1 + i,
                                   offsetrow + N - 1, offsetcol + 1 + i)
        cell_range6 = "=Library!"+cell_range5 # I'm sure there's a better way, but it works
        workbook.define_name(df.columns[i], cell_range6)
    
    for i in range(len(df.columns)):
        cell_range7 = xl_range_abs(offsetrow, offsetcol + 1 + i,
                                   offsetrow + N - 1, offsetcol + 1 + i)
        cell_range8 = "=Library!"+cell_range7 # I'm sure there's a better way, but it works
        workbook.define_name(df.columns[i] + '.MD', cell_range8)
    
    workbook.close()
    print("Done! SIP Library saved successfully to your current working directory.")

# Now lets see if our function works!
# First, create all of the required inputs:

import pandas as pd

# How many trials do you want in your SIP Library?
N = 11

# Generate a few SIPs:
SIP_1 = np.random.normal(40, 10, N)
SIP_2 = np.random.normal(40, 10, N)
SIP_3 = np.random.normal(40, 10, N)
SIP_4 = np.random.normal(40, 10, N)
SIP_5 = np.random.normal(40, 10, N)

# Create a single dataframe containing all of the SIPs:
Data_Frame = pd.DataFrame({'SIP_1': SIP_1, 'SIP_2': SIP_2,
                      'SIP_3': SIP_3, 'SIP_4': SIP_4, 'SIP_5': SIP_5})

# Python indexing starts at 0 and we want our index names to start at 1.
# My function will do this automatically, but for completion, I do it here, too
Data_Frame.index = {1,2,3,4,5,"...", 996, 997, 998, 999, 1000}

# Create the optional metadate dataframe
Meta_Data = pd.DataFrame(Data_Frame.describe())

# You can enter the file name as a text string as an argument,
# But I prefer to use variables whenever possible
file_name1 = "SIP_Library_no_metadata.xlsx"
file_name2 = "SIP_Library_with_metadata.xlsx"

# Similarly, you can enter the author name as a text string as an argument,
# But I prefer to use variables whenever possible
author = "Shaun Doheney"

# Now that you've created all the required (and optional) inputs,
# You're ready to test the function.
# This tests the case where you do not include metadata:
SIPLibraryGenerator(Data_Frame, file_name1, author)

# This tests the case where you do include metadata:
SIPLibraryGenerator(Data_Frame, file_name2, author, Meta_Data)
