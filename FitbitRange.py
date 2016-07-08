
# coding: utf-8

# # Collecting Fitbit Data for a Range of Dates
# To start saving your own data as a CSV, you really only need to adjust the following variables in this notebook:
# 
#   * USER_ID, CLIENT_SECRET (your own Fitbit credentials)
#   * start_date, end_date (dates in date range, note end_date is not inclusive)
#   * path (specifies where to save your output)

# ## 1. Import the necessary Python libraries and modules: 

# In[119]:

#!/usr/bin/python      

import fitbit
import gather_keys_oauth2 as Oauth2
import numpy as np
import datetime
import pandas as pd
import csv
import re
from IPython.display import display


# ## 2. Access the Fitbit API
# Replace 'your USER_ID' and 'your CLIENT_SECRET' ([follow this tutorial to obtain these](http://blog.mr-but-dr.xyz/en/programming/fitbit-python-heartrate-howto/)) to access your Fitbit data:

# In[97]:

"""provide your credentials for OAuth2.0"""
USER_ID = 'your USER_ID' # should look something like this: '123A4B'
CLIENT_SECRET = 'your CLIENT_SECRET' # should look something like this: 'c321fvdc59b4cc62156n9luv20k39072'

"""obtain access and refresh tokens"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
 
ACCESS_TOKEN = server.oauth.token['access_token']
REFRESH_TOKEN = server.oauth.token['refresh_token']
 
"""complete authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


# ## 3. Pick a Date Range
# In order to not exceed the rate limit, weekly and monthly intervals typically work best (learn more about [Fitbit's rate limiting policy]).   
# 
# [Fitbit's rate limiting policy]: https://dev.fitbit.com/docs/basics/#rate-limits

# In[99]:

start_date = datetime.date(2016, 2, 1)
end_date = datetime.date(2016, 3, 1) # end_date not inclusive


# In[100]:

"""function to iterate over dates (resource: http://stackoverflow.com/a/1060330)"""

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)): # for loop through dates in date range
        yield start_date + datetime.timedelta(n) # return date


# ## 4. Define a path to save your data files to
# If you followed the README to create folders to store your data the end of your path will look like mine, otherwise adjust as necessary:

# In[101]:

# adjust your path depending on where you want to store your data
path='/Users/amandasolis/Dropbox/Projects/python-fitbit/Data/'


# ## 5. Define functions for data collection
# Some of the following functions retrieve time-series data for each day, while others return summary data for each day. Each function creates a data frame by iterating over the days in the date range. These are then returned as global variables and saved as CSV files.
# 

# In[102]:

"""Calories Series Function"""

def Calorieseries(start_date, end_date):
    Cals_df = pd.DataFrame([]) # initialize an empty data frame 
    for single_date in daterange(start_date, end_date): # loop through dates in date range
        date = single_date.strftime("%Y-%m-%d")
        # access Fitbit calorie log and save as data frame:
        fitbit_cals = auth2_client.intraday_time_series('activities/log/calories', base_date=date, detail_level='1min')
        Calstats = fitbit_cals['activities-log-calories-intraday']['dataset']
        Cals=pd.DataFrame(Calstats)
        del Cals['mets'] # delete 'mets' column 
        del Cals['level'] # delete 'level' column
        Cals=Cals.transpose() 
        Cals.columns = Cals.iloc[0] # use 'time' stamp to rename columns with 00:00, 00:01 ... 23:58, 23:59
        Cals=Cals.reindex(Cals.index.drop('time')) # drop redundant information (time now reflected as column name)
        Cals=Cals.rename(index={'value': str(date)}) # rename the index (row name) with the corresponding date
        Cals_df = Cals_df.append(Cals, ignore_index=False) # add this row to the data frame initialized before the for loop

    # the 'name' variable reflects the folder and file name we are saving the full data frame to:
    name='Cals_Timeseries/Cals_Timeseries_', str(start_date),'.csv'
    name="".join(name)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path=path, name
    full_path="".join(full_path)
    Cals_df.to_csv(full_path)
    
    # save 'Cals_df1' as a global variable to explore directly in this notebook
    global Cals_df1
    Cals_df1 = Cals_df
    # save 'full_index' as a global variable to use elsewhere
    # (the 'full_index' variable is a 1x1440 vector of column names between 00:00, 00:01 ... 23:58, 23:59
    # it comes in handy for the time-series functions (i.e. heart rate, sleep) that do not
    # provide values for all 1440 minutes) 
    global full_index
    full_index=Cals.columns.values
    return Cals_df1, full_index

"""Steps Series Function"""

def Stepseries(start_date, end_date):
    Steps_df = pd.DataFrame([]) # initialize an empty data frame
    for single_date in daterange(start_date, end_date): # loop through dates in date range
        date = single_date.strftime("%Y-%m-%d")
        # access Fitbit step log and save as data frame:
        fitbit_steps = auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level='1min')
        Stepsstats = fitbit_steps['activities-steps-intraday']['dataset']
        Steps=pd.DataFrame(Stepsstats)
        Steps=Steps.transpose()
        Steps.columns = Steps.iloc[0] # use 'time' stamp to rename columns with 00:00, 00:01 ... 23:58, 23:59
        Steps=Steps.reindex(Steps.index.drop('time')) # drop redundant information (time now reflected as column name)
        Steps=Steps.rename(index={'value': str(date)}) # rename the index (row name) with the corresponding date
        Steps_df = Steps_df.append(Steps, ignore_index=False) # add this row to the data frame initialized before the for loop

    # the 'name' variable reflects the folder and file name we are saving the full data frame to:
    name='Steps_Timeseries/Steps_Timeseries_', str(start_date),'.csv'
    name="".join(name)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path=path, name
    full_path="".join(full_path)
    Steps_df.to_csv(full_path)
    
    # save 'Steps_df1' as a global variable to explore directly in this notebook
    global Steps_df1
    Steps_df1 = Steps_df
    return Steps_df1

"""Heart Rate Series Function"""

def HRseries(start_date, end_date):
    HR_df = pd.DataFrame([]) # initialize an empty data frame
    for single_date in daterange(start_date, end_date): # loop through dates in date range
        date = single_date.strftime("%Y-%m-%d")
        # access Fitbit heart rate log and save as data frame:
        fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level='1min')
        stats = fitbit_stats['activities-heart-intraday']['dataset']
        HR=pd.DataFrame(stats)
        try: # try the following:
            indexed_HR = HR.set_index(HR['time'])
        except KeyError: # if there is no HR['time'] data for this date, create an empty row:
            filler=pd.DataFrame(np.empty(1400, dtype=object))
            full_filler=filler.reindex(full_index) # reindex with the full_index of times from the Calorieseries function 
            filler=full_filler.transpose()
            filler=filler.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
            HR_df = HR_df.append(filler, ignore_index=False) # add this row to the data frame initialized before the for loop
        else:
            del indexed_HR['time']
            full_HR=indexed_HR.reindex(full_index) # reindex with the full_index of times from the Calorieseries function 
            HR2=full_HR.transpose()
            HR2=HR2.rename(index={'value': str(date)}) # rename the index (row name) with the corresponding date
            HR_df = HR_df.append(HR2, ignore_index=False) # add this row to the data frame initialized before the for loop
    
    # the 'name' variable reflects the folder and file name we are saving the full data frame to:
    name='HR_Timeseries/HR_Timeseries_', str(start_date),'.csv'
    name="".join(name)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path=path, name
    full_path="".join(full_path)
    HR_df.to_csv(full_path)
    
    # save 'HR_df1' as a global variable to explore directly in this notebook
    global HR_df1
    HR_df1 = HR_df
    return HR_df1


# In[103]:

"""Sleep Series & Summary Function"""

def Sleep(start_date, end_date):
    Sleep_df = pd.DataFrame([]) # initialize an empty data frame
    SleepSummary_df = pd.DataFrame([]) # initialize an empty data frame

    for single_date in daterange(start_date, end_date): # loop through dates in date range
        date = single_date.strftime("%Y-%m-%d")
        # access Fitbit sleep log and save as data frame:
        fitbit_sleep = auth2_client.sleep(date)
        try: # try the following:
            sleepstats = fitbit_sleep['sleep'][0]['minuteData']
        except IndexError: # create empty/filler data if no timeseries data collected:
            filler=pd.DataFrame(np.empty(1400, dtype=object))
            full_filler=filler.reindex(full_index) # reindex with the full_index of times from the Calorieseries function 
            filler=full_filler.transpose()
            filler=filler.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
            Sleep_df = Sleep_df.append(filler, ignore_index=False) # add this row to the data frame initialized before the for loop
        else: # check for multiple sleep records
            if len(fitbit_sleep['sleep']) >= 2: # if multiple sleep records exist for one day, combine all records:
                for record in range(1,len(fitbit_sleep['sleep'])-1): # loop through sleep records
                    temp=fitbit_sleep['sleep'][record]['minuteData'] # create temporary sleep record
                    sleepstats = sleepstats + [x for x in temp if x not in sleepstats] # append temporary record to full sleepstats
            else: # if there are not multiple records, continue with initial sleepstats variable:
                pass   
            Sleep=pd.DataFrame(sleepstats)
            Sleep['dateTime']=Sleep['dateTime'].astype(str)
            i=0
            for val in Sleep['dateTime']: # loop through time stamps, for values that end with --:30 replace with --:00:
                val2=re.sub('30$', '00', val)
                Sleep.set_value(i,'dateTime',val2)
                i=i+1
            Sleep=Sleep.transpose()
            Sleep.columns = Sleep.iloc[0] # use 'time' stamp to rename columns with 00:00, 00:01 ... 23:58, 23:59
            Sleep=Sleep.reindex(Sleep.index.drop('dateTime')) # drop redundant information (time now reflected as column name)
            Sleep2=Sleep.transpose()
            full_Sleep=Sleep2.reindex(full_index) # reindex with the full_index of times from the Calorieseries function 
            Sleep=full_Sleep.transpose()
            Sleep=Sleep.rename(index={'value': str(date)}) # rename the index (row name) with the corresponding date
            Sleep_df = Sleep_df.append(Sleep, ignore_index=False) # add this row to the data frame initialized before the for loop
        try: # try the following:
            SleepSumm = fitbit_sleep['sleep']
        except IndexError: # if no entry exists for this date, create a filler row:
            filler=pd.DataFrame(np.empty(14, dtype=object))
            filler=filler.transpose()
            filler=filler.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
            col_names=[u'awakeCount', u'awakeDuration', u'awakeningsCount', u'duration',u'efficiency', u'isMainSleep', u'minutesAfterWakeup', u'minutesAsleep', u'minutesAwake', u'minutesToFallAsleep', u'restlessCount',u'restlessDuration', u'startTime', u'timeInBed']
            filler.columns = col_names # rename the column names with the ones defined in 'col_names'
            SleepSummary_df = SleepSummary_df.append(filler, ignore_index=False) # add this row to the data frame initialized before the for loop
        else: # check for multiple sleep records
            if len(fitbit_sleep['sleep']) >= 2: # if multiple sleep records exist for one day, combine all records:
                for record in range(0,len(fitbit_sleep['sleep'])-1): # loop through sleep records
                    SleepSumm=fitbit_sleep['sleep'][record] 
                    # delete redundant data:
                    del SleepSumm['minuteData'] 
                    del SleepSumm['logId']
                    del SleepSumm['dateOfSleep']
                    SleepSumm=pd.DataFrame([SleepSumm])
                    SleepSumm=SleepSumm.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
                    SleepSummary_df = SleepSummary_df.append(SleepSumm, ignore_index=False) # add this row to the data frame initialized before the for loop
            else: # if there are not multiple records:
                try: 
                    # delete redundant data:
                    del SleepSumm[0]['minuteData']
                    del SleepSumm[0]['logId']
                    del SleepSumm[0]['dateOfSleep']
                except IndexError: # if no entry exists for this date, create a filler row:
                    filler=pd.DataFrame(np.empty(14, dtype=object))
                    filler=filler.transpose()
                    filler=filler.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
                    col_names=[u'awakeCount', u'awakeDuration', u'awakeningsCount', u'duration',u'efficiency', u'isMainSleep', u'minutesAfterWakeup', u'minutesAsleep', u'minutesAwake', u'minutesToFallAsleep', u'restlessCount',u'restlessDuration', u'startTime', u'timeInBed']
                    filler.columns = col_names # rename the column names with the ones defined in 'col_names'
                    SleepSummary_df = SleepSummary_df.append(filler, ignore_index=False) # add this row to the data frame initialized before the for loop
                else:
                    SleepSumm=pd.DataFrame(SleepSumm)
                    SleepSumm=SleepSumm.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
                    SleepSummary_df = SleepSummary_df.append(SleepSumm, ignore_index=False) # add this row to the data frame initialized before the for loop
    
    # the 'name1' variable reflects the folder and file name we are saving the full summary data frame to:
    name1='Sleep_Summary/Sleep_Summary_', str(start_date),'.csv'
    name1="".join(name1)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path1=path, name1
    full_path1="".join(full_path1)
    SleepSummary_df.to_csv(full_path1)

    # the 'name2' variable reflects the folder and file name we are saving the full time-series data frame to:
    name2='Sleep_Timeseries/Sleep_Timeseries_', str(start_date),'.csv'
    name2="".join(name2)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path2=path, name2
    full_path2="".join(full_path2)
    Sleep_df.to_csv(full_path2)
    
    # save 'SleepSummary_df1' as a global variable to explore directly in this notebook
    global SleepSummary_df1
    SleepSummary_df1 = SleepSummary_df
    # save 'Sleep_df1' as a global variable to explore directly in this notebook
    global Sleep_df1
    Sleep_df1 = Sleep_df
    return SleepSummary_df1, Sleep_df1


# In[104]:

""" Activities Summary (Distances, Heart Rate Zones, Remaining Activity) Function"""

def ActivitiesSummary(start_date, end_date):
    DistancesSummary_df = pd.DataFrame([]) # initialize an empty data frame
    HRSummary_df = pd.DataFrame([]) # initialize an empty data frame
    ActivitySummary_df = pd.DataFrame([]) # initialize an empty data frame
    
    for single_date in daterange(start_date, end_date): # loop through dates in date range
        date = single_date.strftime("%Y-%m-%d")
        # access Fitbit activity summary and save subfields as individual data frames:
        active_list = auth2_client.activities(date)
        activities_summary=active_list['summary']
        distances=activities_summary['distances']        
        try: # try the following:
            HRzones=activities_summary['heartRateZones'] 
        except KeyError: # if no summary exists, create fillder data:
            HRfiller=pd.DataFrame(np.empty(16, dtype=object))
            HRfiller=HRfiller.transpose()
            HRfiller=HRfiller.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
            HRcol_names= [u'OutRange.caloriesOut', u'OR.max', u'OR.min', u'OR.minutes', u'FatBurn.caloriesOut', u'FB.max', u'FB.min', u'FB.minutes', u'Cardio.caloriesOut', u'C.max', u'C.min', u'C.minutes',u'Peak.caloriesOut', u'P.max', u'P.min', u'P.minutes']
            HRfiller.columns = HRcol_names # rename the column names with the ones defined in 'HRcol_names'
            HRSummary_df = HRSummary_df.append(HRfiller, ignore_index=False) # add this row to the data frame initialized before the for loop
            
            DistSumm=pd.DataFrame(distances)
            DistSumm=DistSumm.transpose()
            DistSumm.columns = DistSumm.iloc[0] # rename the columns w/ names from row 0
            DistSumm=DistSumm.reindex(DistSumm.index.drop('activity')) # drop redundant information (now reflected as column names)
            DistSumm=DistSumm.rename(index={'distance': str(date)}) # rename the index (row name) with the corresponding date            
            DistancesSummary_df = DistancesSummary_df.append(DistSumm, ignore_index=False) # add this row to the data frame initialized before the for loop

            del activities_summary['distances']
            
            ActivitiesSumm=pd.DataFrame(activities_summary.items())
            ActivitiesSumm=ActivitiesSumm.transpose()
            ActivitiesSumm.columns = ActivitiesSumm.iloc[0] # rename the columns w/ names from row 0
            ActivitiesSumm=ActivitiesSumm.reindex(ActivitiesSumm.index.drop(0)) # drop redundant information (now reflected as column names)
            ActivitiesSumm=ActivitiesSumm.rename(index={1: str(date)}) # rename the index (row name) with the corresponding date
            ActivitySummary_df = ActivitySummary_df.append(ActivitiesSumm, ignore_index=False) # add this row to the data frame initialized before the for loop
    
            
        else:
            DistSumm=pd.DataFrame(distances)
            DistSumm=DistSumm.transpose()
            DistSumm.columns = DistSumm.iloc[0] # rename the columns w/ names from row 0
            DistSumm=DistSumm.reindex(DistSumm.index.drop('activity')) # drop redundant information (now reflected as column names)
            DistSumm=DistSumm.rename(index={'distance': str(date)}) # rename the index (row name) with the corresponding date            
            DistancesSummary_df = DistancesSummary_df.append(DistSumm, ignore_index=False) # add this row to the data frame initialized before the for loop
    

            HRSumm=pd.DataFrame(HRzones) 
            HRSumm.rows = HRSumm.iloc[0] # rename the rows w/ names from row 0
            HRSumm=HRSumm.rename(index={0:"Out of Range", 1:"Fat Burn", 2:"Cardio", 3:"Peak"}) # rename the index           
            del HRSumm['name'] # delete duplicated info now that indexes are named
            HRflat=HRSumm.values.flatten() # flatten dataframe into single row
            HRSumm2=pd.DataFrame(HRflat)
            HRSumm2=HRSumm2.transpose()
            # rename column names:
            HRSumm2=HRSumm2.rename(columns={0:"OutRange.caloriesOut", 1:"OR.max", 2:"OR.min", 3:"OR.minutes", 4:"FatBurn.caloriesOut", 5:"FB.max", 6:"FB.min", 7:"FB.minutes", 8:"Cardio.caloriesOut", 9:"C.max", 10:"C.min", 11:"C.minutes", 12:"Peak.caloriesOut", 13:"P.max", 14:"P.min", 15:"P.minutes"})
            HRSumm2=HRSumm2.rename(index={0: str(date)}) # rename the index (row name) with the corresponding date
            HRSummary_df = HRSummary_df.append(HRSumm2, ignore_index=False) # add this row to the data frame initialized before the for loop
    
            # delete data that we have already used:
            del activities_summary['distances']
            del activities_summary['heartRateZones']

            ActivitiesSumm=pd.DataFrame(activities_summary.items())
            ActivitiesSumm=ActivitiesSumm.transpose()
            ActivitiesSumm.columns = ActivitiesSumm.iloc[0] # rename the columns w/ names from row 0
            ActivitiesSumm=ActivitiesSumm.reindex(ActivitiesSumm.index.drop(0)) # drop redundant information (now reflected as column names)
            ActivitiesSumm=ActivitiesSumm.rename(index={1: str(date)}) # rename the index (row name) with the corresponding date
            ActivitySummary_df = ActivitySummary_df.append(ActivitiesSumm, ignore_index=False) # add this row to the data frame initialized before the for loop
    
    # the 'name1' variable reflects the folder and file name we are saving the full Distances summary data frame to:
    name1='Distances_Summary/Distances_Summary_', str(start_date),'.csv'
    name1="".join(name1)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path1=path, name1
    full_path1="".join(full_path1)
    DistancesSummary_df.to_csv(full_path1)
    
    # the 'name2' variable reflects the folder and file name we are saving the full HR summary data frame to:
    name2='HR_Summary/HR_Summary_', str(start_date),'.csv'
    name2="".join(name2)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path2=path, name2
    full_path2="".join(full_path2)
    HRSummary_df.to_csv(full_path2)
    
    # the 'name3' variable reflects the folder and file name we are saving the full Activities summary data frame to:
    name3='Activities_Summary/Activities_Summary_', str(start_date),'.csv'
    name3="".join(name3)
    # adding in the full path saves the file to the exact location specified earlier:
    full_path3=path, name3
    full_path3="".join(full_path3)
    ActivitySummary_df.to_csv(full_path3)
    
    # save 'DistancesSummary_df1' as a global variable to explore directly in this notebook
    global DistancesSummary_df1
    DistancesSummary_df1 = DistancesSummary_df
    # save 'HRSummary_df1' as a global variable to explore directly in this notebook
    global HRSummary_df1
    HRSummary_df1 = HRSummary_df
    # save 'ActivitySummary_df1' as a global variable to explore directly in this notebook
    global ActivitySummary_df1
    ActivitySummary_df1 = ActivitySummary_df
    return DistancesSummary_df1, HRSummary_df1, ActivitySummary_df1


# ## 6. Combine above functions into main function
# If you don't want to collect all of these measures, feel free to comment any of them out:

# In[107]:

def main():
    Calorieseries(start_date, end_date) # obtain calories time-series data
    HRseries(start_date,end_date) # obtain heart rate time-series data
    Stepseries(start_date, end_date) # obtain steps time-series data
    ActivitiesSummary(start_date, end_date) # obtain activity, HR, and distances summary data
    Sleep(start_date, end_date) # obtain sleep time-series and summary data


# ## 7. Run Main and Explore Files/Global Variables! 

# In[ ]:

main()


# In[118]:

"""preview the first 5 rows of each data frame"""

print "Activity Summary"
display(ActivitySummary_df1.head())

print "Distances Summary"
display(DistancesSummary_df1.head())

print "Heart Rate Zones Summary"
display(HRSummary_df1.head())

print "Sleep Summary"
display(SleepSummary_df1.head())

print "Sleep Time-Series"
display(Sleep_df1.head())

print "Calories Time-Series"
display(Cals_df1.head())

print "Steps Time-Series"
display(Steps_df1.head())

print "Heart Rate Time-Series"
display(HR_df1.head())

