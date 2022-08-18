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


#Defining the photometry plotting function here to save having to rerun it everytime:

def plot_photometry(pdf):
    fig = plt.figure(figsize=(12, 5))

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
    plt.show()