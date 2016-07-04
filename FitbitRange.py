
# coding: utf-8

# # Collecting Fitbit Data with Python

# In[1]:

#!/usr/bin/python      

import fitbit
import gather_keys_oauth2 as Oauth2
import numpy as np
import datetime
import pandas as pd
import csv
import re


# ## Access Fitbit API

# In[2]:

"""for OAuth2.0"""
USER_ID = 'your USER_ID' 
CLIENT_SECRET = 'your CLIENT_SECRET'

"""for obtaining Access-token and Refresh-token"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
print('FULL RESULTS = %s' % server.oauth.token)
print('ACCESS_TOKEN = %s' % server.oauth.token['access_token'])
 
ACCESS_TOKEN = server.oauth.token['access_token']
REFRESH_TOKEN = server.oauth.token['refresh_token']
 
"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


# ## Pick a Date Range

# In[3]:

start_date = datetime.date(2016, 5, 18)
end_date = datetime.date(2016, 5, 21)


# In[4]:

"""Iterate over Dates- resource: http://stackoverflow.com/a/1060330"""

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


# ## Define Functions for Time-Series Data Collection
# 

# In[5]:

"""Calories Series"""

def Calorieseries(start_date, end_date):
    Cals_df = pd.DataFrame([])
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d")
        fitbit_cals = auth2_client.intraday_time_series('activities/log/calories', base_date=date, detail_level='1min')
        Calstats = fitbit_cals['activities-log-calories-intraday']['dataset']
        Cals=pd.DataFrame(Calstats)
        del Cals['mets'] # delete 'mets' column 
        del Cals['level'] # delete 'level' column
        Cals=Cals.transpose()
        Cals.columns = Cals.iloc[0]
        Cals=Cals.reindex(Cals.index.drop('time'))
        Cals=Cals.rename(index={'value': str(date)})
        Cals_df = Cals_df.append(Cals, ignore_index=False)
    Cals_df.to_csv('Cals-timeseries1.csv')
    global Cals_df1
    Cals_df1 = Cals_df
    global full_index
    full_index=Cals.columns.values
    return Cals_df1, full_index

"""Steps Series"""

def Stepseries(start_date, end_date):
    Steps_df = pd.DataFrame([])
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d")
        fitbit_steps = auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level='1min')
        Stepsstats = fitbit_steps['activities-steps-intraday']['dataset']
        Steps=pd.DataFrame(Stepsstats)
        Steps=Steps.transpose()
        Steps.columns = Steps.iloc[0]
        Steps=Steps.reindex(Steps.index.drop('time'))
        Steps=Steps.rename(index={'value': str(date)})
        Steps_df = Steps_df.append(Steps, ignore_index=False)
    Steps_df.to_csv('Steps-timeseries1.csv')
    global Steps_df1
    Steps_df1 = Steps_df
    return Steps_df1

"""Heart Rate Series"""

def HRseries(start_date, end_date):
    HR_df = pd.DataFrame([])
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d")
        fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level='1min')
        stats = fitbit_stats['activities-heart-intraday']['dataset']
        HR=pd.DataFrame(stats)
        indexed_HR = HR.set_index(HR['time'])
        del indexed_HR['time']
        full_HR=indexed_HR.reindex(full_index)
        HR2=full_HR.transpose()
        HR2=HR2.rename(index={'value': str(date)})
        HR_df = HR_df.append(HR2, ignore_index=False)
    HR_df.to_csv('HR-timeseries1.csv')
    global HR_df1
    HR_df1 = HR_df
    return HR_df1

"""Sleep Series"""

def Sleepseries(start_date, end_date):
    Sleep_df = pd.DataFrame([])
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d")
        fitbit_sleep = auth2_client.sleep(date)
        try:
            sleepstats = fitbit_sleep['sleep'][0]['minuteData']
        except IndexError:
            filler=pd.DataFrame(np.empty(1400, dtype=object))
            full_filler=filler.reindex(full_index)
            filler=full_filler.transpose()
            filler=filler.rename(index={0: str(date)})
            Sleep_df = Sleep_df.append(filler, ignore_index=False)
        else:
            Sleep=pd.DataFrame(sleepstats)
            Sleep['dateTime']=Sleep['dateTime'].astype(str)
            i=0
            for val in Sleep['dateTime']:
                val2=re.sub('30$', '00', val)
                Sleep.set_value(i,'dateTime',val2)
                i=i+1
            Sleep=Sleep.transpose()
            Sleep.columns = Sleep.iloc[0]
            Sleep=Sleep.reindex(Sleep.index.drop('dateTime'))
            Sleep2=Sleep.transpose()
            full_Sleep=Sleep2.reindex(full_index)
            Sleep=full_Sleep.transpose()
            Sleep=Sleep.rename(index={'value': str(date)})
            Sleep_df = Sleep_df.append(Sleep, ignore_index=False)
    Sleep_df.to_csv('Sleep-timeseries1.csv')
    global Sleep_df1
    Sleep_df1 = Sleep_df
    return Sleep_df1


# ## Define Functions for Collecting Summary Data
# 

# In[6]:

"""Sleep Summary"""

def SleepSummary(start_date, end_date):
    SleepSummary_df = pd.DataFrame([])
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d")
        fitbit_sleep = auth2_client.sleep(date)
        try:
            SleepSumm = fitbit_sleep['sleep']
            del SleepSumm[0]['minuteData']
        except IndexError:
            filler=pd.DataFrame(np.empty(14, dtype=object))
            filler=filler.transpose()
            filler=filler.rename(index={0: str(date)})
            col_names=[u'awakeCount', u'awakeDuration', u'awakeningsCount', u'duration',u'efficiency', u'isMainSleep', u'minutesAfterWakeup', u'minutesAsleep', u'minutesAwake', u'minutesToFallAsleep', u'restlessCount',u'restlessDuration', u'startTime', u'timeInBed']
            filler.columns = col_names
            SleepSummary_df = SleepSummary_df.append(filler, ignore_index=False)
        else:
            del SleepSumm[0]['logId']
            del SleepSumm[0]['dateOfSleep']
            SleepSumm=pd.DataFrame(SleepSumm)
            SleepSumm=SleepSumm.rename(index={0: str(date)})
            SleepSummary_df = SleepSummary_df.append(SleepSumm, ignore_index=False)
    SleepSummary_df.to_csv('Sleep-Summary.csv')
    global SleepSummary_df1
    SleepSummary_df1 = SleepSummary_df
    return SleepSummary_df1

""" Activities Summary (Distances, Heart Rate Zones, Remaining Activity)"""

def ActivitiesSummary(start_date, end_date):
    DistancesSummary_df = pd.DataFrame([])
    HRSummary_df = pd.DataFrame([])
    ActivitySummary_df = pd.DataFrame([])
    
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y-%m-%d")
        active_list = auth2_client.activities(date)
        activities_summary=active_list['summary']
        distances=activities_summary['distances']        
        try:
            HRzones=activities_summary['heartRateZones'] 

        except KeyError:
            HRfiller=pd.DataFrame(np.empty(16, dtype=object))
            HRfiller=HRfiller.transpose()
            HRfiller=HRfiller.rename(index={0: str(date)})
            HRcol_names= [u'OutRange.caloriesOut', u'OR.max', u'OR.min', u'OR.minutes', u'FatBurn.caloriesOut', u'FB.max', u'FB.min', u'FB.minutes', u'Cardio.caloriesOut', u'C.max', u'C.min', u'C.minutes',u'Peak.caloriesOut', u'P.max', u'P.min', u'P.minutes']
            HRfiller.columns = HRcol_names
            HRSummary_df = HRSummary_df.append(HRfiller, ignore_index=False)
            
            DistSumm=pd.DataFrame(distances)
            DistSumm=DistSumm.transpose()
            DistSumm.columns = DistSumm.iloc[0]
            DistSumm=DistSumm.reindex(DistSumm.index.drop('activity'))
            DistSumm=DistSumm.rename(index={'distance': str(date)})            
            DistancesSummary_df = DistancesSummary_df.append(DistSumm, ignore_index=False)

            del activities_summary['distances']
            
            ActivitiesSumm=pd.DataFrame(activities_summary.items())
            ActivitiesSumm=ActivitiesSumm.transpose()
            ActivitiesSumm.columns = ActivitiesSumm.iloc[0]
            ActivitiesSumm=ActivitiesSumm.reindex(ActivitiesSumm.index.drop(0))
            ActivitiesSumm=ActivitiesSumm.rename(index={1: str(date)})
            ActivitySummary_df = ActivitySummary_df.append(ActivitiesSumm, ignore_index=False)
            
        else:
            DistSumm=pd.DataFrame(distances)
            DistSumm=DistSumm.transpose()
            DistSumm.columns = DistSumm.iloc[0]
            DistSumm=DistSumm.reindex(DistSumm.index.drop('activity'))
            DistSumm=DistSumm.rename(index={'distance': str(date)})            
            DistancesSummary_df = DistancesSummary_df.append(DistSumm, ignore_index=False)

            HRSumm=pd.DataFrame(HRzones) 
            HRSumm.rows = HRSumm.iloc[0]
            HRSumm=HRSumm.rename(index={0:"Out of Range", 1:"Fat Burn", 2:"Cardio", 3:"Peak"})            
            del HRSumm['name'] #delete duplicated info now that indexes are named
            HRflat=HRSumm.values.flatten() #Flatten dataframe into single row
            HRSumm2=pd.DataFrame(HRflat)
            HRSumm2=HRSumm2.transpose()
            HRSumm2=HRSumm2.rename(columns={0:"OutRange.caloriesOut", 1:"OR.max", 2:"OR.min", 3:"OR.minutes", 4:"FatBurn.caloriesOut", 5:"FB.max", 6:"FB.min", 7:"FB.minutes", 8:"Cardio.caloriesOut", 9:"C.max", 10:"C.min", 11:"C.minutes", 12:"Peak.caloriesOut", 13:"P.max", 14:"P.min", 15:"P.minutes"})
            HRSumm2=HRSumm2.rename(index={0: str(date)})
            HRSummary_df = HRSummary_df.append(HRSumm2, ignore_index=False)

            del activities_summary['distances']
            del activities_summary['heartRateZones']

            ActivitiesSumm=pd.DataFrame(activities_summary.items())
            ActivitiesSumm=ActivitiesSumm.transpose()
            ActivitiesSumm.columns = ActivitiesSumm.iloc[0]
            ActivitiesSumm=ActivitiesSumm.reindex(ActivitiesSumm.index.drop(0))
            ActivitiesSumm=ActivitiesSumm.rename(index={1: str(date)})
            ActivitySummary_df = ActivitySummary_df.append(ActivitiesSumm, ignore_index=False)

    DistancesSummary_df.to_csv('Distances-Summary.csv')
    HRSummary_df.to_csv('HR-Summary.csv')
    ActivitySummary_df.to_csv('Activities-Summary.csv')
    
    global DistancesSummary_df1
    DistancesSummary_df1 = DistancesSummary_df
    global HRSummary_df1
    HRSummary_df1 = HRSummary_df
    global ActivitySummary_df1
    ActivitySummary_df1 = ActivitySummary_df
    
    return DistancesSummary_df1, HRSummary_df1, ActivitySummary_df1


# ## Combine into Main Function

# In[9]:

def main():
    Calorieseries(start_date, end_date)
    HRseries(start_date,end_date)
    Sleepseries(start_date, end_date)
    Stepseries(start_date, end_date)
    SleepSummary(start_date, end_date)
    ActivitiesSummary(start_date, end_date)


# ## Run Main and Explore Files! 
# ("Cals-timeseries1.csv", "Steps-timeseries1.csv", "HR-timeseries1.csv", "Sleep-timeseries1.csv", "Sleep-Summary.csv","Distances-Summary.csv", "HR-Summary.csv", "Activities-Summary.csv")

# In[11]:

main()

