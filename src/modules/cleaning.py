import pandas as pd

def clean_CPS_df(df):
    #Concatenate HRHHID numbers
    
    ## Important
    df['HH_ID'] = (df['HRHHID'].astype(str) + df['HRHHID2'].astype(str))
    
    df['IND_ID'] = (df['HRHHID'].astype(str)
                    + df['HRHHID2'].astype(str)
                    + df['PERRP'].astype(str))
    
    df['IND_ID_SEX_AGE'] = (df['HRHHID'].astype(str)
                    + df['HRHHID2'].astype(str)
                    + df['PERRP'].astype(str)
                    + df['PESEX'].astype(str)
                    + df['PRTAGE'].astype(str))
    
    ## Important
    df['IND_ID_FINAL'] = (df['HRHHID'].astype(str)
                    + df['HRHHID2'].astype(str)
                    + df['PERRP'].astype(str)
                    + df['PESEX'].astype(str)
                    + df['PRTAGE'].astype(str)
                    + df['PULINENO'].astype(str))
    
    return df