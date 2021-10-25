"""
Created on Mon Mar 22 11:19:59 2021
Updated 8/29/21
SIPLibrary Generator
Version 1

This Python script allows a user to create PM.org 3.0 libraries to be read in
by ChanceCalc and the SIPmath tools in Excel. The output is a PM.org 3.0 Library
in a .xlsx or .json format.

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
        boundedness : str
            Uses the same format as metalog.fit : boundedness 
            of metalog distribution. Can take values 'u' for unbounded, 'sl' for 
            semi-bounded lower, 'su' for semi-bounded upper and 'b' for bounded 
            on both sides.
        bounds : list of up to 2 int values
            bounds of metalog distribution. Depending on boundedness 
            argument can take zero, one or two values.
        term_saved : int value bewteen 2 and 30 
            Sets the number of A coefficients (N value) used for fitting the 
            SIPs.
        seeds : rng
            If left empty, the default is to create a seeds where the entity = 1, 
            the varId = a random int between 1 and 10,000,000, seed3 = 0 and 
            seed4 = 0. MakeHDRrngs is an included helper function to create the
            rng dictionary for specific seeds.
        setupInputs : dict
            Input for the N terms, boudedness, and bounds of each SIP to be used
            for the resulting library.

@author: Aaron Brown. Credits to Sergey Kim, Reidar Brumer Bratvold for their 
metalog implementation, and Shaun Doheney for the original SIPlibrary work, from
which this is largely based.
"""
import scipy
import pandas as pd
import numpy as np
from metalog import metalog
import json
from datetime import date
import xlsxwriter

def HDRrngGenerator(x, entity = 1, varid = [], seed3 = 0, seed4 = 0):
    if varid == []:
        varId = np.random.randint(1,10000001)
    else:
        varId = varid
    if isinstance(entity, list) and len(entity) < x:
        print("Entity needs to be a single integer value or a list at least as long as x.")
    else:
        if isinstance(entity, int) and (isinstance(varid, int) or varid == []) and isinstance(seed3, int) and isinstance(seed4, int):
            rngs=list()
            for i in range(x):
                rngs.append({'name':'hdr'+str(i+1),
                           'function':'HDR_2_0',
                           'arguments':{'counter':'PM_Index',
                               'entity': entity,
                               'varId': varId+i,
                               'seed3': seed3,
                               'seed4': seed4}
                           })
        elif isinstance(entity, list) and (isinstance(varid, list) and varid != []) and isinstance(seed3, list) and isinstance(seed4, list) and len(entity) == len(varid) and len(varid) == len(seed3) and len(seed3) == len(seed4):
            rngs=list()
            for i in range(x):
                rngs.append({'name':'hdr'+str(i+1),
                           'function':'HDR_2_0',
                           'arguments':{'counter':'PM_Index',
                               'entity': entity[i],
                               'varId': varId[i],
                               'seed3': seed3[i],
                               'seed4': seed4[i]}
                           })
        elif isinstance(entity, list) and (isinstance(varid, list) and varid != []) and isinstance(seed3, int) and isinstance(seed4, int):
            rngs=list()
            for i in range(x):
                rngs.append({'name':'hdr'+str(i+1),
                           'function':'HDR_2_0',
                           'arguments':{'counter':'PM_Index',
                               'entity': entity[i],
                               'varId': varId[i],
                               'seed3': seed3,
                               'seed4': seed4}
                           })
        elif isinstance(entity, list) and (isinstance(varid, int) or varid == []) and isinstance(seed3, int) and isinstance(seed4, int):
            rngs=list()
            for i in range(x):
                rngs.append({'name':'hdr'+str(i+1),
                           'function':'HDR_2_0',
                           'arguments':{'counter':'PM_Index',
                               'entity': entity[i],
                               'varId': varId+1,
                               'seed3': seed3,
                               'seed4': seed4}
                           })
        else:
            print("Parameters are not in the correct formats (int, list) or aren't in a supportted configuration.")
    with open('HDRseeds.json', 'w') as json_file:
        json.dump(rngs, json_file, indent=4)
    print(rngs)
    return(rngs)

def Json(SIPdata, file_name, author, SIPmetadata = [], dependence = 'independent', boundedness = 'u', bounds = [0, 1], term_saved = 5, seeds = [], setupInputs = []):
    if (seeds != [] and len(seeds) < len(SIPdata.columns)):
        print("RNG list length must be equal to or greater than the number of SIPs.")
    elif (setupInputs != [] and len(setupInputs["bounds"]) != len(SIPdata.columns)):
        print("List length of the input file must be equal to the number of SIPs.")
    else:
        slurp = SIPdata #Assigning some useful variables
        sip_count = len(slurp.columns)
        
        if seeds == []: #This section will create a random seed value for each SIP, or use an input 'rng' list
            rand = np.random.randint(1,10000001)
            Seeds = [1, rand, 0, 0]    
            rngs=list()
            for i in range(sip_count):
                rngs.append({'name':'hdr'+str(i+1),
                           'function':'HDR_2_0',
                           'arguments':{'counter':'PM_Index',
                               'entity': Seeds[0],
                               'varId': Seeds[1]+i,
                               'seed3': Seeds[2],
                               'seed4': Seeds[3]}
                           })
        else:
            rngs=seeds
        
         #More set up to hold the copula information
        rng = list()
        for i in range(sip_count):
            rng.append('hdr'+str(i+1))
        copulaLayer = list()
        for i in range(sip_count):
            copulaLayer.append('c'+str(i+1))
        
        arguments={'correlationMatrix':{'type':'globalVariables',
                        'value':'correlationMatrix'},
                   'rng' : rng}
        
        copdict = {'arguments':arguments,
                   'function':'GaussianCopula',
                   'name':'Gaussian',
                   'copulaLayer' : copulaLayer}
        
        copula=list()
        copula.append(copdict)
        rng=rngs
        
        if dependence == 'dependent': #Holds the RNG and copula data if applicable
            oui ={'rng':rng,
                  'copula':copula}
        else:
            oui ={'rng':rng}
        
        if SIPmetadata == []: #If the describe function is being used for default metadata, then the names are being changed for the visual layer
            slurp_meta = pd.DataFrame(slurp.describe())
            renames = slurp_meta.index.values
            renames[4] = 'P25'
            renames[5] = 'P50'
            renames[6] = 'P75'
        else:
            slurp_meta = SIPmetadata
            
        if setupInputs == []:
            boundednessin = [boundedness] * sip_count
            if boundedness == 'u':
                boundsin = [[0,1]] * sip_count
            else:
                boundsin = [bounds] * sip_count
            termsin = [term_saved] * sip_count
        else:
            boundednessin = setupInputs['boundedness']
            boundsin = setupInputs['bounds']
            for i in range(sip_count):
                if boundednessin[i] == 'u':
                    boundsin[i] = [0,1]
            termsin = setupInputs['term_saved']
    
    
        metadata = slurp_meta.to_dict()
        
        sips=list()#Set up for the SIPs
        
        if dependence == 'dependent':#This section creates the metalogs for each SIP, and has a different version for the indepedent vs dependent case
            for i in range(sip_count):
                mfitted = metalog.fit(np.array(slurp.iloc[:,i]).astype(float), bounds = boundsin[i], boundedness = boundednessin[i], term_limit = termsin[i], term_lower_bound = termsin[i])
                interp = scipy.interpolate.interp1d(mfitted['M'].iloc[:,1],mfitted['M'].iloc[:,0])
                interped = interp(np.linspace(min(mfitted['M'].iloc[:,1]),max(mfitted['M'].iloc[:,1]),25)).tolist()
                a_coef = mfitted['A'].iloc[:,1].to_list()
                metadata[slurp.columns[i]].update({'density':interped})
                if boundednessin[i] == 'u':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'copula',
                               'name':'Gaussian',
                               'copulaLayer':'c'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                if boundednessin[i] == 'sl':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'copula',
                               'name':'Gaussian',
                               'copulaLayer':'c'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'lowerBound':boundsin[i][0],
                                     'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                if boundednessin[i] == 'su':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'copula',
                               'name':'Gaussian',
                               'copulaLayer':'c'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'upperBound':boundsin[i][0],
                                     'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                if boundednessin[i] == 'b':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'copula',
                               'name':'Gaussian',
                               'copulaLayer':'c'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'lowerBound':boundsin[i][0],
                                     'upperBound':boundsin[i][1],
                                     'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                sips.append(sipdict)
        else:
            for i in range(sip_count):
                mfitted = metalog.fit(np.array(slurp.iloc[:,i]).astype(float), bounds = boundsin[i], boundedness = boundednessin[i], term_limit = termsin[i], term_lower_bound = termsin[i])
                interp = scipy.interpolate.interp1d(mfitted['M'].iloc[:,1],mfitted['M'].iloc[:,0])
                interped = interp(np.linspace(min(mfitted['M'].iloc[:,1]),max(mfitted['M'].iloc[:,1]),25)).tolist()
                a_coef = mfitted['A'].iloc[:,1].to_list()
                metadata[slurp.columns[i]].update({'density':interped})
                if boundednessin[i] == 'u':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'rng',
                               'name':'hdr'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                if boundednessin[i] == 'sl':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'rng',
                               'name':'hdr'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'lowerBound':boundsin[i][0],
                                     'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                if boundednessin[i] == 'su':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'rng',
                               'name':'hdr'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'upperBound':boundsin[i][0],
                                     'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                if boundednessin[i] == 'b':
                    sipdict = {'name':slurp.columns[i],
                        'ref':{'source':'rng',
                               'name':'hdr'+str(i+1)},
        	     	    'function':'Metalog_1_0',
                        'arguments':{'lowerBound':boundsin[i][0],
                                     'upperBound':boundsin[i][1],
                                     'aCoefficients':a_coef},
                        'metadata':metadata[slurp.columns[i]]}
                sips.append(sipdict)          
        
        corrdata = pd.DataFrame(np.tril(slurp.corr()))#Creating the lower half of a correlation matrix for the copula section if applicable
        corrdata.columns = slurp.columns
        corrdata.index = slurp.columns
        stackdf = corrdata.stack()
        truncstackdf = stackdf[stackdf.iloc[:] != 0]
        counter = truncstackdf.count()
    
        matrix = list()
        
        
        for i in range(counter): #Gets our correlations in the correct format
            matrix.append({'row':truncstackdf.index.get_level_values(0)[i],
                  'col':truncstackdf.index.get_level_values(1)[i],
                  'value':truncstackdf[i]})
            
        
        value = {'columns' : slurp.columns.to_list(),
                 'rows' : slurp.columns.to_list(),
                 'matrix' : matrix}
        
        if dependence == 'dependent':#No global variables are added to the independent case
            globalVariables = list()
            globalVariables.append({'name':'correlationMatrix',
                                    'value':value})   
            
            finaldict = {'name' : file_name,
                         'objectType': 'sipModel',
                         'libraryType': 'SIPmath_3_0',
                         'dateCreated' : date.today().strftime("%m-%d-%Y"),
                         'globalVariables':globalVariables,
                         'provenance' : author,
                         'U01' : oui,
                         'sips':sips,
                         'version':'1'}
        else:
            finaldict = {'name' : file_name,
                         'objectType': 'sipModel',
                         'libraryType': 'SIPmath_3_0',
                         'dateCreated' : date.today().strftime("%m-%d-%Y"),
                         'provenance' : author,
                         'U01' : oui,
                         'sips':sips,
                         'version':'1'}
        
        with open(file_name, 'w') as json_file:#Outputs the file to the current directory
            json.dump(finaldict, json_file, indent=4)
        print("Done! 3.0 SIP Library saved successfully to your current working directory.")

def Xlsx(SIPdata, file_name, author, SIPmetadata = [], boundedness = 'u', bounds = [0, 1], term_saved = 5, seeds = [1,1,0,0]):
    slurp = SIPdata
    sip_count = len(slurp.columns)
    slurp.index = np.arange(1, len(slurp)+1)
    
    if SIPmetadata == []:
        slurp_meta = pd.DataFrame(slurp.describe())
    else:
        slurp_meta = SIPmetadata
    
    metalen = len(slurp_meta)
    
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet('Library')
    
    #Writing all the cells that hold either static names or SIP specific meta data
    worksheet.write('A1', 'PM_Property_Names')
    worksheet.write('A2', 'PM_Trials')
    worksheet.write('A3', 'PM_Lib_Provenance')
    worksheet.write('A4', 'PM_SIP_Names')
    worksheet.write('A5', 'PM_Meta')
    worksheet.write('A6', 'PM_Meta_Index')
    worksheet.write('A7', 'PM_NumCholesky')
    worksheet.write('A8', 'PM_NumMeta')
    worksheet.write('A9', 'PM_NumDensity')
    worksheet.write('A10', 'PM_NumCoeffs')
    worksheet.write('A11', 'PM_SIPmath')
    
    worksheet.write('B1', 'PM_Property_Values')
    worksheet.write('B2', 'F Inverse')
    worksheet.write('B3', author)
    worksheet.write('B4', ','.join(slurp.columns))
    worksheet.write('B5', 'Unused in 3.0')
    worksheet.write('B6', 'Unused in 3.0')
    worksheet.write('B7', sip_count)
    worksheet.write('B8', metalen)
    worksheet.write('B9', 25)
    worksheet.write('B10', 16)
    worksheet.write('B11', '3.2b')
    
    worksheet.write('C1', 'PM_Row_Header_1')
    worksheet.write('C2', 'Name')
    worksheet.write('C3', 'Type (SIP or F Inverse)')
    worksheet.write('C4', 'Terms')
    worksheet.write('C5', 'Bound')
    worksheet.write('C8', 'Cholesky')
    worksheet.write('C'+str(8+sip_count), 'HDR')
    worksheet.write('C'+str(12+sip_count), 'MetaData')
    worksheet.write('C'+str(12+sip_count+metalen), 'Density')
    worksheet.write('C'+str(37+sip_count+metalen), 'A_Coef')
    
    worksheet.write('D1', 'PM_Row_Header_1')
    worksheet.write('D6', 'Lower')
    worksheet.write('D7', 'Upper')
    for i in range(sip_count):
        worksheet.write('D'+str(i+8), slurp.columns[i])
    worksheet.write('D'+str(8+sip_count), 'Entity')
    worksheet.write('D'+str(9+sip_count), 'Var ID')
    worksheet.write('D'+str(10+sip_count), 'Option1')
    worksheet.write('D'+str(11+sip_count), 'Option2')
    for i in range(metalen):
        worksheet.write('D'+str(i+12+sip_count), slurp_meta.index[i])
    for i in range(1,26):
        worksheet.write('D'+str(i+11+sip_count+metalen), 'Density'+str(i))
    for i in range(1,term_saved+1):
        worksheet.write('D'+str(i+36+sip_count+metalen), 'A_'+str(i))
    
    #Adding the Cholesky Matrix
    cholmatrix = np.transpose(np.linalg.cholesky(slurp.corr()))
    
    for row_num, row_data in enumerate(cholmatrix):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num+7, col_num+4, col_data)
    
    #This section adds seeds based on either the default or the input. The default
    #is to randomly pick a starting Var ID and iterate it onwards +1. It adds 
    #+1 to each var ID to make the base seeds independent.
    if seeds == [1,1,0,0]:
        rand = np.random.randint(1,10000001)
        for i in range(sip_count):
            worksheet.write(7+sip_count, 4+i, seeds[0])
            worksheet.write(8+sip_count, 4+i, rand+i)
            worksheet.write(9+sip_count, 4+i, seeds[2])
            worksheet.write(10+sip_count, 4+i, seeds[3])
    else:
        for i in range(sip_count):
            worksheet.write(7+sip_count, 4+i, seeds[0])
            worksheet.write(8+sip_count, 4+i, seeds[1]+i)
            worksheet.write(9+sip_count, 4+i, seeds[2])
            worksheet.write(10+sip_count, 4+i, seeds[3])
    
    #Adding the metadata
    for i in range(sip_count):
        for j in range(metalen):
            worksheet.write(11+sip_count+j, 4+i, slurp_meta.iloc[j,i])
    
    #Running metalog calculations, adding them to the worksheet
    for i in range(sip_count):
        mfitted = metalog.fit(np.array(slurp.iloc[:,i]), bounds = bounds, boundedness = boundedness, term_limit = term_saved, term_lower_bound = term_saved)
        worksheet.write(0, 4+i, 'Variable_'+str(i+1))
        worksheet.write(1, 4+i, slurp.columns[i])
        worksheet.write(2, 4+i, 'F Inverse')
        worksheet.write(3, 4+i, term_saved)
        worksheet.write(4, 4+i, boundedness)
        worksheet.write(5, 4+i, bounds[0])
        worksheet.write(6, 4+i, bounds[1])
        
        interp = scipy.interpolate.interp1d(mfitted['M'].iloc[:,1],mfitted['M'].iloc[:,0])
        interped = interp(np.linspace(min(mfitted['M'].iloc[:,1]),max(mfitted['M'].iloc[:,1]),25))
        
        for j in range(25):
            worksheet.write(11+sip_count+metalen+j, 4+i, interped[j])
        
        for j in range(term_saved):
            worksheet.write(36+sip_count+metalen+j, 4+i, mfitted['A'].iat[j,1])
        
    workbook.close()
    print("Done! 3.0 SIP Library saved successfully to your current working directory.")
