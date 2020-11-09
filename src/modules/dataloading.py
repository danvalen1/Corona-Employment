import requests
import zipfile
import pandas as pd
import re
import os
import sys
import waybackpy
from datetime import datetime
from dateutil.parser import parse
import urllib

# Global Variables
archive_age_limit = 30

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'

def CPS_raw(targetdir, list_of_mmmyyyy, series):
    """Retrieves monthly CPS data from 1998 onwards.
    
            Parameters:
                targetdir (str): String indicating where data should be saved.
                list_of_mmmyyyy (list of str): List of month-years of data 
                to be retrieved (e.g., sep2020)
                series (list of str): List of variables of interest
        
            Returns:
                df (pandas data frame): Dataframe of all data listed in list_of_mmmyyyy 
                constrained by series.
    """

    # Begin stack of data with series of intereest
    dfs=[]
    
    # loops through data to get individual dataframes
    for mmmyyyy in list_of_mmmyyyy:
        # converts input to lowercase
        mmmyyyy = mmmyyyy.lower()
        
        # Retrieves variables of interest for given month
        dd_sel_var = CPS_vars(targetdir, mmmyyyy, series)
            
        # Saves CPS data for given month
        targetfile = targetdir + f'CPS-{mmmyyyy}.zip'

        # URL for given month
        url = f'https://www2.census.gov/programs-surveys/cps/datasets/{mmmyyyy[-4:]}/basic/{mmmyyyy[0:3] + mmmyyyy[5:7]}pub.zip'

        # Extract files and return locations  
        file_locs = URL_DL_ZIP(targetfile, targetdir, url)
        
        
        # Convert raw data into a list of tuples
        data_final = [tuple
                      (
                          (-1
                           # Account for insertion of chars in .dat file 
                           if 
                           (
                               not(RepresentsInt(line[i[1]:i[2]]))
                           )
                           else int(line[i[1]:i[2]])
                              
                          )
                          for i in dd_sel_var
                      ) 
                      for line in open(file_locs[0], 'rb')]

        # Convert to pandas dataframe, add variable ids as heading
        CPS_df = pd.DataFrame(data_final, columns=[v[0] for v in dd_sel_var])
            
        dfs.append(CPS_df)
    
    # Merge stack
    df = pd.concat(dfs)
     
    return df

def CPS_vars(targetdir, mmmyyyy, series):
    """Retrieves all variables for a given month of CPS data. Can be constrained by series.
    
            Parameters:
                targetdir (str): String indicating where data should be saved.
                mmmyyyy (str): Month-year of data to be retrieved (e.g., sep2020).
                series (list of str): List of variables of interest.
        
            Returns:
                dd_sel_vars (list of tuples): List of tuples containing key data for reading 
                out data into dataframe variables.
    """
    
    ## Download relevant data dictionary 
    # Parsing out mmmyyyy for use
    yyyy = int(mmmyyyy[-4:])
    mmmyy = mmmyyyy[0:3] + mmmyyyy[5:7]
    mmm = mmmyyyy[0:3]
    monthdict = {'jan': 1, 
                 'feb': 2, 
                 'mar': 3, 
                 'apr': 4, 
                 'may': 5,
                 'jun': 6,
                 'jul': 7,
                 'aug': 8,
                 'sep': 9,
                 'oct': 10,
                 'nov': 11,
                 'dec': 12}
    # Relevant URLs
    if yyyy == 2020: 
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2020/basic/2020_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt'
    elif yyyy > 2016:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2017/basic/January_2017_Record_Layout.txt'
    elif yyyy > 2014:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2015/basic/January_2015_Record_Layout.txt'
    elif yyyy > 2013:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2014/basic/January_2014_Record_Layout.txt'
    elif yyyy > 2012:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2013/basic/January_2013_Record_Layout.txt'
    elif (yyyy == 2012) & (monthdict[mmm] > 4):
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2012/basic/may12dd.txt'
    elif yyyy > 2009:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2010/basic/jan10dd.txt'
    elif yyyy > 2008:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2009/basic/jan09dd.txt'
    elif yyyy > 2006:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2007/basic/jan07dd.txt'
    elif (((yyyy == 2005) & (monthdict[mmm] > 7))
          | yyyy > 2005):
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2005/basic/augnov05dd.txt'
    elif ((yyyy == 2004) & (monthdict[mmm] > 4)
         | (yyyy == 2005) & (monthdict[mmm] < 8)):
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2004/basic/may04dd.txt'
    elif yyyy > 2002:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2003/basic/jan03dd.txt'
    elif yyyy > 1997:
        url = 'https://www2.census.gov/programs-surveys/cps/datasets/2002/basic/jan98dd.asc'
        
    # Create file
    
    dd_file = targetdir + f'{yyyy}_{mmm}_CPS_DataDict.txt'
    urllib.request.urlretrieve(url, dd_file)
    
    ## Open file and parse out relevant lines  
    
    dd_full = open(dd_file, 'r', encoding='iso-8859-1').read()
    if yyyy > 2008:
        p = re.compile('\n(\w+)\s+(\d+)\s+(.*?)(?!\s\d)\s+(\d\d*).*?(\d\d+)')
    elif yyyy > 2002:
        p = re.compile('\n(\w+)\s+(\d+)\s+(.*?)\s+\((\d\d*).*?(\d\d+)\)')
    else:
        p = re.compile('\n[D]\s+(\w*)\s+(\d*)\s+(\d*)\n[T]\s(.*?)\n')
    
        
    data = p.findall(dd_full)
    
    ## Retrive list of relevant vars based on series arg
    series_final = []
    if (series == None) & (yyyy > 2002):
        # Import all vars as pd.df
        df_vars = pd.DataFrame(data, 
                               columns = ['name', 
                                          'size', 
                                          'description', 
                                          'loc_range_min', 
                                          'loc_range_max'])
        # Clean df and convert into list
        df_vars = df_vars[
            (df_vars.name != 'FILLER') 
            & (df_vars.name != 'PADDING')]
        df_vars['name'] = df_vars['name'].str.strip()
        
        series_final = df_vars['name'].tolist()
    
    elif series == None:
         # Import all vars as pd.df
        df_vars = pd.DataFrame(data, 
                               columns = ['name',
                                          'size', 
                                          'loc_range_min',
                                          'description'])
        # Clean df and convert into list
        df_vars = df_vars[
            (df_vars.name != 'FILLER') 
            & (df_vars.name != 'PADDING')]
        df_vars['name'] = df_vars['name'].str.strip()
        
        series_final = df_vars['name'].tolist()      
        
    else:
        # Import only series vars
        for i in series:
            series_final.append(i.upper())
    
    ## Create list of tuples with vars and locs to retrieve from .dat
    dd_sel_var = []
    adj_above_2002 = -1 if yyyy > 2002 else 0
    adj_below_2003 = -1 if yyyy < 2003 else 0
    for i in p.findall(dd_full):
        if yyyy < 2003:
            loc = [int(i[2]), int(i[2]) + int(i[1])]
        else:
            loc = [int(i[3]), int(i[4])]
            
        
        if i[0] in series_final:
            ## Account for certain data dict nits
            if loc[0] == loc[1]:
                dd_sel_var.append((i[0], 
                                   loc[0], 
                                   loc[1]+2))
            else:
                dd_sel_var.append((i[0], 
                                   loc[0]+(adj_below_2003)+(adj_above_2002), 
                                   loc[1]+(adj_below_2003)))
                    
                                  
                                  
    return dd_sel_var

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def URL_DL_ZIP(targetzip, targetdir, url):
    """Downloads and unzips zip file from url and return locations of extracted files.
    
            Parameters:
                targetzip (str): String indicating where zip file is to be saved.
                targetdir (str): String indicating where files are to be extracted.
                url (str): URL where the zip exists.
            Returns:
                file_locs (list of str): Returns locations for all the extracted files.
    """
    archive_url = archive(url=url, targetdir=targetdir).get('archive_url')
    
    # Save Zip from archived site
    r_archive = requests.get(archive_url)
    r_url = requests.get(url)
    try:
        r = r_archive
        file_locs = Unzip(targetzip, r)
        
    except:
        r = r_url
        file_locs = Unzip(targetzip, r)
        
        
    return file_locs

def Unzip(targetzip, r):
    """Unzip a file from a url.
    
            Parameters:
                r (response object): Response from url where zip file exists.
                targetzip (str): String of path to target zip file.
            Returns:
                file_locs (list of str): Returns locations for all the extracted files.
    
    """
    
    with open(targetzip,'wb') as f: 
        f.write(r.content)
    
    # Set and/or create sub-folder
    sub_folder = targetzip.rsplit('.', 1)[0] +'/'
    try:
        os.mkdir(sub_folder)
    except:
        pass
    
    # Unzipping file        
    try:
        
        with zipfile.ZipFile(targetzip, 'r') as zip_ref:
            zip_ref.extractall(sub_folder)
            # Get list of files names in zip
            files = zip_ref.namelist()
    except:
        raise

        
        
    # Return list of locations of extracted files   
    file_locs = [] 
    for file in files:
        file_locs.append(sub_folder + file)
    
    return file_locs

def archive(url, targetdir=None):
    """Archives URL and saves information to data log in targetdir based on archive age limit.
    
            Parameters:
                url (str): String indicating where data exists.
                targetdir (str): String indicating where files' data log exists.
        
            Returns:
                archive_dict (dict): Dictionary with URL and timestamp of latest archive.
    """
    archive_dict = {'archive_url': None, 'archive_time': None}
    wayback_obj = waybackpy.Url(url=url, user_agent=user_agent)
    archive_age = len(wayback_obj)
    
    # Create new archive if age is greater than limit, else use most recent
    if archive_age > archive_age_limit:
        archive_dict['archive_url'] = wayback_obj.save().archive_url
        archive_dict['archive_time'] = datetime.utcnow()
        new_archive = 1
    else:
        archive_dict['archive_url'] = wayback_obj.archive_url
        archive_dict['archive_time'] = wayback_obj.timestamp
        new_archive = 0
    
    # Dict of data about archive
    d = {'URL': [url],
         'File': [url.rsplit('/', 1)[-1]],
         'Directory': [targetdir],
         'ArchiveURL': [archive_dict['archive_url']],
         'ArchiveTime': [archive_dict['archive_time']],
         'NewArchive': [new_archive]
        }
        
    # Add to or create data log
    try:
        data_log = pd.read_csv(f'{targetdir}+_data_log.csv', index_col='LogID')
        data_log['ArchiveTime'] = [parse(x) for x in data_log['ArchiveTime']]
        d['LogID'] = data_log.index.values.max() + 1
    
        d = pd.DataFrame.from_dict(d)
        d.set_index('LogID', inplace=True)
    
        data_log = pd.concat([d, data_log]).drop_duplicates(keep='last')
        
    except:
        d['LogID'] = 1
        data_log = pd.DataFrame(data=d)
        data_log.set_index('LogID', inplace=True)
   
    data_log.to_csv(f'{targetdir}+_data_log.csv', index_label='LogID')
    
    return archive_dict