#here are the necessary imports
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from io import StringIO
from vasttools.pipeline import Pipeline
from vasttools.query import Query

#function used to sort the classes in the catalogue into families
def family_sort(cms):
    AGN_Family=[
    'AGN',
    'AGN_Candidate',
    'QSO',
    'QSO_Candidate',
    'Seyfert',
    'Seyfert_1',
    'Seyfert_2',
    'Blazar',
    'BLLac',
    'Blazar_Candidate',
    'RadioG',
    'LINER'
    ]

    Unknown_Family=[
    'Unknown'
    ]

    Galaxy_Family=[
    'Galaxy',
    'EmG',
    'HII_G',
    'GroupG',
    'GinGroup',
    'GinCl',
    'GinPair',
    'BClG',
    'PartofG'
    ]

    Stars_Family=[
    'Star',
    'RRLyr',
    'Candidate_RRLyr',
    'EB*',
    'Candidate_EB*',
    'WD*',
    'LMXB',
    'CataclyV*',
    'low-mass*'
    ]

    Supernovae_Family=[
    'SN',
    'SN candidate'
    ]

    Radio_Family=[
    'Radio',
    'Radio(cm)'
    ]

    Multiwavelength_Family=[
    'Blue',
    'UV',
    'X'
    ]

    Solar_System_Family=[
    'Solar System',
    'Solar System MPC',
    'Solar System candidate',
    ]
    
    Source_Families=[] #define an empty array
    for i, row in cms.iterrows(): #'i' represents the first index in cmf.iterrows, 'row' is the second
        x=row['class'] #this pulls out the class column from eachrow
        for j in AGN_Family: #for all the classes listed in the AGN family
            if x==j: #if it matches the class of the row
                Source_Families.append('AGN') #add 'AGN' to the empty array
        else: #otherwise, check the other families to see if it matches
            for j in Unknown_Family:
                if x==j:
                    Source_Families.append('Unknown')
            else:
                for j in Galaxy_Family:
                    if x==j:
                        Source_Families.append('Galaxy')
                else:
                    for j in Stars_Family:
                        if x==j:
                            Source_Families.append('Star')
                    else:
                        for j in Supernovae_Family:
                            if x==j:
                                Source_Families.append('Supernova')
                        else:
                            for j in Radio_Family:
                                if x==j:
                                    Source_Families.append('Radio')
                            else:
                                for j in Multiwavelength_Family:
                                    if x==j:
                                        Source_Families.append('Multiwavelength')
                                else:
                                    for j in Solar_System_Family:
                                        if x==j:
                                            Source_Families.append('Solar System')

    cms['family']=Source_Families


#defining the photometry plotting function here to save having to rerun it everytime.
#have to load VAST run, the FINK requested sources AND the filtered candidate catalogue and feed them into the input
def plot_lightcurves(my_run,fsd,candidates,FINK_ID):#,xlim,vast_ylim,fink_ylim,):
    
    gs = gridspec.GridSpec(2,1) #sets up a 2x1 grid
    vast_gs = gs[1:2] #puts the VAST axis on the bottom
    
    vast_source=my_run.get_source(candidates[candidates['objectId'] == FINK_ID]['matched_id'].astype(int).values[0])
    
    fig = vast_source.plot_lightcurve(figsize=(15,6),mjd=True)
    vast_ax = fig.axes[0]
    vast_ax.set_title(None)
    
    vast_ax.set_position(vast_gs.get_position(fig))
    vast_ax.set_subplotspec(vast_gs)
    #vast_ax.set_xlim(xlim)
    #vast_ax.set_ylim(vast_ylim)
    
    ax_new = fig.add_subplot(211, sharex=vast_ax)
    ax_new.tick_params(labelbottom=False)
    plt.tight_layout()
    
    pdf=fsd[fsd['i:objectId'] == FINK_ID]
    
    colordic = {1: 'C0', 2: 'C1'}
    
    for filt in np.unique(pdf['i:fid']):
        maskFilt = pdf['i:fid'] == filt

        # The column `d:tag` is used to check data type
        maskValid = pdf['d:tag'] == 'valid'
        plt.errorbar(
            pdf[maskValid & maskFilt]['i:jd'].apply(lambda x: x - 2400000.5),
            pdf[maskValid & maskFilt]['i:magpsf'],
            pdf[maskValid & maskFilt]['i:sigmapsf'],
            ls = '', marker='o', color=colordic[filt]
        )

        maskUpper = pdf['d:tag'] == 'upperlim'
        plt.plot(
            pdf[maskUpper & maskFilt]['i:jd'].apply(lambda x: x - 2400000.5),
            pdf[maskUpper & maskFilt]['i:diffmaglim'],
            ls='', marker='^', color=colordic[filt], markerfacecolor='none'
        )

        maskBadquality = pdf['d:tag'] == 'badquality'
        plt.errorbar(
            pdf[maskBadquality & maskFilt]['i:jd'].apply(lambda x: x - 2400000.5),
            pdf[maskBadquality & maskFilt]['i:magpsf'],
            pdf[maskBadquality & maskFilt]['i:sigmapsf'],
            ls='', marker='v', color=colordic[filt]
        )

    plt.gca().invert_yaxis()
    plt.xlabel('Modified Julian Date')
    plt.ylabel('Magnitude')
    #plt.xlim(xlim)
    #plt.ylim(fink_ylim)
    plt.show()
    
def plot_cutouts(my_run,fsd,candidates,FINK_ID,vast_epoch=1):
    
    #defining column array for cutouts
    cutouts=[
    'b:cutoutScience_stampData',
    'b:cutoutTemplate_stampData',
    'b:cutoutDifference_stampData'
    ]

    fsd_source=fsd[fsd['i:objectId'] == FINK_ID]
    vast_source=my_run.get_source(candidates[candidates['objectId'] == FINK_ID]['matched_id'].astype(int).values[0])
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))

    for col in cutouts:
        data = fsd_source[col].values[0]
        axes[cutouts.index(col)].imshow(np.arcsinh(data))
        
    cutout = vast_source.show_png_cutout(vast_epoch)
    all_cutouts = vast_source.show_all_png_cutouts(columns=3, figsize=(10,10))

    #This function takes in the crossmatched catalogue, the run from VAST and the eta and v threshholds calculated from
    #eta_v_analysis():
    
def eta_v_candidate_filter(cms,my_run,eta_thresh,v_thresh):
    
    #list of VAST ids:
    matched_ids=cms['matched_id'].astype(int).to_list()
    #this creates an arrray of sources from my_run that have the same ids as the catalogue, with the necessary eta and v
    #information
    sel=my_run.sources[my_run.sources.index.isin(matched_ids)]
    
    #we already got the VAST info on our crossmatched sources through sel. we just need to filter for the highly variable
    #sources based on the eta and v threshholds we calculated before:
    candidate_sel = sel[(sel['eta_peak'] >= eta_thresh) & (sel['v_peak'] >= v_thresh)]

    #getting the sel_candidate ids is squirrely, since they're the row INDEX of the dataframe. 
    #passing eta_v_candidates['id'] will not work. The below code pulls out those index values as a string list:
    candidate_ids=candidate_sel.index.values.astype('str').tolist()

    #then we just check how many objects in cmf have an id that match the candidate ids
    candidate_cms=cms[cms['matched_id'].isin(candidate_ids)]
    print('There are',len(candidate_cms),'candidate sources:')
    
    return candidate_cms

#This function will take the crossmatch catalogue and filter out sources that do not have good overlap in Optical and Radio. Please make sure that you convert all time observations into Modified Julian Dates (MJD), and that column names
#for FINK and VAST line up with whats requested in the function. feel free to modify the function as well for your own convenience.

def lightcurve_overlap_filter(cms,fsd,vsd,O,R,dt=0):
    
    #defining empty Overlap array, which will store Booliean values
    Overlap = []

    if O <= 1 or R <= 1:
        raise Exception('Please choose a minimum optical & radio observation overlap count greater than 1')
    if dt < 0:
        raise Exception ('Please choose a dt >= 0')

    #this takes the FINK and VAST IDs from the crossmatch catalogue and puts them into a dataframe, resetting the index.
    cml = pd.DataFrame({"FINK ID": cms['objectId'], "VAST ID": cms['matched_id']}).reset_index()

    #this drops the 'index' column leftover from cms_candidates
    cml.drop('index', inplace=True, axis=1)
    cml['VAST ID']=cml['VAST ID'].astype(int)

    ftd = pd.DataFrame({"i:objectId": fsd['i:objectId'], "i:mjd":fsd['i:mjd']})
    vtd = pd.DataFrame({"source": vsd['source'], "time_mjd": vsd['time_mjd']})

    #i represents the index of the row selelcted in cml. x and y are then the FINK and VAST IDs of that row respectively
    for i in cml.index.to_list():
        FINK_ID,VAST_ID = cml.iloc[[i]]['FINK ID'][i], cml.iloc[[i]]['VAST ID'][i]

        #these are all the rows in fsd that have the same FINK ID as the selected row in cml
        ftd_temp = ftd[ftd['i:objectId'] == FINK_ID]
        ftd_temp = ftd_temp.sort_values('i:mjd').reset_index()
        ftd_temp.drop('index', inplace=True, axis=1)

        #these are all the rows in vsd that have the same VAST ID as the selected row in cml
        vtd_temp = vtd[vtd['source'] == VAST_ID]
        vtd_temp = vtd_temp.sort_values('time_mjd').reset_index()
        vtd_temp.drop('index', inplace=True, axis=1)

        # j represents the jth index in ftd_temp. start is the start date at the jth row, end is the row O-1 steps ahead.
        for j in ftd_temp.index.to_list():

            #if we've reached the end of the list and the loop hasnt broken, it means we havent found any good overlap.
            if j+O-1 > ftd_temp.index.to_list()[-1]:
                Overlap.append(False)
                break

            start, end = ftd_temp.iloc[[j]]['i:mjd'][j], ftd_temp.iloc[[j+O-1]]['i:mjd'][j+O-1]
            #this checks which points in vtd_temp are within the range between start and end, +- dt incase an observation is slightly out of this range
            overlap_temp = vtd_temp['time_mjd'].between(start-dt,end+dt)

            #If the number of points wthin that range is >= R, we have good overlap!
            if len(overlap_temp[overlap_temp==True]) >= R:
                Overlap.append(True)
                break
    
    cml['Overlap']=Overlap
    print('Of the',Overlap.count(False)+Overlap.count(True),'Sources that have been analyzed,',Overlap.count(True),'of them have good overlap:')
    
    return cml
