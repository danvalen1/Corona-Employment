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
    df = pd.read_csv('../../src/csv/employed_adults_apr2020_jul2020.csv', index_col=0)
    
    # create target variable
    target = df.PREMPNOT_y.apply(job_loss_categorization)
                                        
    # append target to df
    df['target'] = target
    
    # drop future data
    to_drop = [column for column in df.columns if "_y" in column]
    df = df.drop(columns=to_drop)
    
    # remove _x from columns
    df.columns = [column.split("_")[0] for column in df.columns]
    
    # feature list
    feature_list = [
    'HEHOUSUT', # type of housing unit to dummy DONE
    'HWHHWGT', # Household weight
    'GESTFIPS', # state codes
    "GTMETSTA", # Metropolitan or not DONE
    'HEFAMINC', # total family income 
    "HRNUMHOU", # total number of people living in the house hold
    'HRHTYPE', # household type eg civilian or married etc
    'PERRP', # relationship to reference, -1, 40 and 41
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
    "PRMJOCC1", # industry cat
    'target'
    ]
    
    # subset the data frame with our desired columns
    df = df[feature_list]
    
    return df