import pandas as pd

def clean_CPS_df(df):
    #Creating household IDs
    df['HH_ID'] = (df['HRHHID'].astype(str) + df['HRHHID2'].astype(str))

    #Creating individual IDs
    df['IND_ID_FINAL'] = (df['HRHHID'].astype(str)
                    + df['HRHHID2'].astype(str)
                    + df['PERRP'].astype(str)
                    + df['PESEX'].astype(str)
                    + df['PRTAGE'].astype(str)
                    + df['PULINENO'].astype(str))
    
    return df

def catch_up(directory):
    """
    directory --> string, url of the the csv
        - eg '../../src/csv/employed_adults_apr2020_jul2020.csv'
    
    returns --> pandas.DataFrame containing features of intereast
    
    dependencies: 
    packages: pandas
    functions: job_loss_categorization
    """
    # load in df
    df = pd.read_csv(directory, index_col=0)
    
    # feature list
    feature_list = [
    'HEHOUSUT', # type of housing unit to dummy 
    'HWHHWGT', # Household weight
    'GESTFIPS', # state codes
    "GTMETSTA", # Metropolitan or not 
    'HEFAMINC', # total family income < - TIM
    "HRNUMHOU", # total number of people living in the house hold
    'HRHTYPE', # household type eg civilian or married etc
    'PRTAGE', # person's age
    'PEMARITL', # marital status
    'PESEX', # gender 1 == male, 2 == female
    'PEEDUCA', # level of education see dict for coding
    'PTDTRACE', # race composition of the house. See data dict
    "PEHSPNON", # hispanic or not hispanic
    'PENATVTY', # country of birth ie US born or not
    "PRCITSHP", # citezen status
    "PRINUSYR", # Year since immigration -1== us born, else coded by decade
    "PRHRUSL", # Hours at work, dummy into full time or not full time
    "HUBUS", # Does anyone have a business or a farm? are you a business owner?
    "PEMJOT", # Do you have more than 1 job?
    "PEMJNUM", # how many jobs do you have?
    "PEHRFTPT", # Do you normally spend more than 35 hours a week at your main job?
    "PEHRRSN2", # what is the main reason you do not want to work 35 hours. Speaks to motivation of keeping job.
    "PEHRACTT", # sum of hours worked between all jobs
    "PRAGNA", # Agricultural industry yes or no
    "PRNMCHLD", # number of children less than 18 years old (-1 not a parent, 0-99 number of children)
    "PECYC", # How much college credit in years has the reference person recieved?
    "PECERT1", # Do you have a professional certification issued at state or federal level.
    "PRMJIND1", # industry cat
    "PRMJOCC1", # occupation cat
    'target',
    'HH_ID',
    'IND_ID_FINAL'
    ]
    
    # subset the data frame with our desired columns
    df = df[feature_list]
    
    # create target variable
    target = df.PREMPNOT_y.apply(job_loss_categorization)
                                        
    # append target to df
    df['target'] = target
    
    # drop future data
    to_drop = [column for column in df.columns if "_y" in column]
    df = df.drop(columns=to_drop)
    
    # remove _x from columns
    df.columns = [column.split("_")[0] for column in df.columns]
    
    
    
    # dummy var list for transformation
    list_of_dummyvars = [
        'PRCITSHP',
        'PEHRRSN2',
        'PRMJIND1',
        'PRMJOCC1', ## TIM ADDS HIS DUMMIES

    ]
    
    # Binning/transforming variables
    df = feature_changes(df)
    
    # Dummying variables
    df = feature_dummies(df, list_of_dummyvars)
    
    
    return df

    
def feature_transformations(df):
    # Applies transformations done by Tim
    df = tim_binning(df)
    
    # Immigrant recentness of entry
    # Transforms 'not in universe' to 0
    df['PRINUSYR'] = [0 if x == -1 else x for x in df['PRINUSYR']]
    
    # Usual hours worked weekly
    # Transforms categorical to ordinal categorical
    df['PRHRUSL'] = [3 if x == 7 else (2 if x == 8 else x) for x in df['PRHRUSL']]
    
    # Anyone in household with business or farm?
    # Makes into dummy by transforming value of 2 to 0
    df['HUBUS'] = [0 if x == 2 else x for x in df['HUBUS']]
    
    # How many jobs do you have?
    # Transforming -1 to 1 since our universe has employed people in it, also dropping PEMJO since irrelevant
    df['PEMJNUM'] = [1 if x == -1 else x for x in df['PEMJNUM']]
    df.drop(labels = 'PEMJOT', inplace = True)
    
    # Do you work 35 hours or more?
    # Tranforming 'No' and "hours vary" to 0
    df['PEHRFTPT'] = [0 if x in [2,3] else x for x in df['PEHRFTPT']]
    
    # In agricultural industry?
    # Transforming 'No' to 0
    df['PRAGNA'] = [0 if x == 2 else x for x in df['PRAGNA']]
    
    # Professional certification?
    # Transforming 'No' to 0
    df['PECERT1'] = [0 if x == 2 else x for x in df['PECERT1']]
    
    return df

def tim_binning(df):
    # Bin HEHOUSUT aka housing type
    def housing_cat(n):
        if n == 1:
            return 1
        elif n != 1:
            return 0
    df["HEHOUSUT"] = df.HEHOUSUT.apply(housing_cat)
    # bin GTMETSTA aka metro or not
    def metro_cat(n):
        if n == 1 or n==3: # three had most similar characteristics to 1
            return 1
        else:
            return 0
    df["GTMETSTA"] = df.GTMETSTA.apply(metro_cat)
    # bin PEMARITL aka marital status
    def marriage_cat(n):
        if n == 1: # binned all categories to either currently married or not
            return 1
        else:
            return 0
    df["PEMARITL"] = df.PEMARITL.apply(marriage_cat)
    # bin PEEDUCA aka education
    def education_cat(n):
        if n > 39: # completed highschool, we can be granular
            return n
        else:
            return 0 # didn't finish highschool
    df["PEEDUCA"] = df.PEEDUCA.apply(education_cat)
    # bin PTDTRACE aka race composition 
    def rcomp_cat(n):
        if n == 1:
            return 0
        elif n ==2:
            return 1
        else:
            return 3
    df["PTDTRACE"] = df.PTDTRACE.apply(rcomp_cat)
    # bin PENATVTY aka born in the USA
    def birth_cat(n):
        if n == 57: # born in the USA 
            return 1
        else:
            return 0
    df["PENATVTY"] = df.PENATVTY.apply(birth_cat)
    return df

def feature_dummies(df, list_of_dummyvars):
    
    # get dummies and drop first for reference category
    df_dummies = pd.get_dummies(df, columns=list_of_dummyvars, prefix=list_of_dummyvars, drop_first=True)
    
    return df_dummies

def job_loss_categorization(n):
    if n > 1:
        return 1
    else:
        return 0