
# coding: utf-8

# # Collecting and Visualizing Fitbit Data with Python

# In[290]:

#!/usr/bin/python      
get_ipython().magic(u'matplotlib inline')

import fitbit
import matplotlib.pyplot as plt
import gather_keys_oauth2 as Oauth2
import numpy as np
import datetime
import pandas as pd
import csv
import seaborn as sns
from scipy.stats import linregress 


# ## Access Fitbit API

# In[291]:

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


# ## Pick a Date

# In[4]:

## TO DO
#Loop through days
date='2016-06-13'


# ## Collect Time Series Data

# In[4]:

## TO DO 
#save all data to single CSV (each day's data on single row)


# In[264]:

"""Timeseries data of Heartrate"""

fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level='1min')
stats = fitbit_stats['activities-heart-intraday']['dataset']
HR=pd.DataFrame(stats)
HR.head(n=5)

print "----HEART RATE STATS----"
print 'First 5 Samples of Heart Rate Data:'
print HR.head(n=5)
print 'Total HR Samples (variable):', len(HR.index)

HRmax = HR['value'].max()
HRmin = HR['value'].min()
HRmean = HR['value'].mean()

print "Avg HR:", HRmean
print "Max HR:", HRmax
print "Min HR:", HRmin


# In[263]:

#Save HR Timeseries to CSV
HR=HR.transpose()
HR.columns = HR.iloc[0]
HR=HR.reindex(HR.index.drop('time'))
HR.to_csv('HR-timeseries.csv')


# In[258]:

"""Timeseries data of Calories and Activity Level"""

fitbit_cals = auth2_client.intraday_time_series('activities/log/calories', base_date=date, detail_level='1min')
Calstats = fitbit_cals['activities-log-calories-intraday']['dataset']
Cals=pd.DataFrame(Calstats)
Cals.head(n=5)

print "----CALORIE STATS----"
print 'First 5 Rows of Calories Data:'
print Cals.head(n=5)
print 'Total Calorie Samples (fixed):', len(Cals.index)

Calsmax = Cals['value'].max()
Calsmin = Cals['value'].min()
Calsmean = Cals['value'].mean()
CalsSumm = Cals['value'].sum()

print "Total Calories burned:", CalsSumm 
print "Min Calories burned in a minute:", Calsmin 
print "Max Calories burned in a minute:", Calsmax 


# In[257]:

#Save Calorie Timeseries to CSV
del Cals['mets'] # delets 'mets' column 
del Cals['level'] # delete 'level' column

Cals=Cals.transpose()
Cals.columns = Cals.iloc[0]
Cals=Cals.reindex(Cals.index.drop('time'))
Cals.to_csv('Cals-timeseries.csv')


# In[62]:

"""Timeseries data of Steps"""

fitbit_steps = auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level='1min')
Stepsstats = fitbit_steps['activities-steps-intraday']['dataset']

Steps=pd.DataFrame(Stepsstats)
Steps.head(n=5)

print "----STEPS STATS----"
print 'First 5 Rows of Steps Data:'
print Steps.head(n=5)
print 'Total Steps Samples (fixed):', len(Steps.index)

Stepsmax = Steps['value'].max()
Stepsmin = Steps['value'].min()
Stepsmean = Steps['value'].mean()
StepsSumm = Steps['value'].sum()

print "Total Steps walked:", StepsSumm 
print "Min Steps walked in a minute:", Stepsmin 
print "Max Steps walked in a minute:", Stepsmax 
print "Average Steps walked in a minute:", Stepsmean


# In[259]:

#Save Steps Timeseries to CSV
Steps=Steps.transpose()
Steps.columns = Steps.iloc[0]
Steps=Steps.reindex(Steps.index.drop('time'))
Steps.to_csv('Steps-timeseries.csv')


# In[260]:

"""Timeseries data of Sleep"""
fitbit_sleep = auth2_client.sleep(date)
sleepstats = fitbit_sleep['sleep'][0]['minuteData']

values=Sleep['value']
SleepValues = values.astype(float)

Sleep=pd.DataFrame(sleepstats)
Sleep.head(n=5)

print "----SLEEP STATS----"
print 'First 5 Rows of Sleep Data:'
print Sleep.head(n=5)
print 'Total Sleep Minutes Sampled (fixed):', len(Sleep.index)

counts = Sleep['value'].value_counts().to_dict()
counts['Asleep'] = counts.pop('1')
counts['Awake'] = counts.pop('2')
counts['Very Awake'] = counts.pop('3')

print counts


# In[261]:

#Save Sleep Timeseries to CSV
Sleep=Sleep.transpose()
Sleep.columns = Sleep.iloc[0]
Sleep=Sleep.reindex(Sleep.index.drop('dateTime'))
Sleep.to_csv('Sleep-timeseries.csv')


# ## Plots

# In[9]:

##TO DO
#change sleep data values(10=asleep, 0=not recording, etc), add something to sleep data or sleep graph during awake period 


# In[95]:

"""Histograms"""
#HR Histogram
plt.figure(1)
#plt.subplot(211)
plt.hist(HR['value'], bins=len(stats), range=(HRmin,HRmax))
#sns.distplot(HR);
plt.title('Distribution of HR Values')
plt.ylabel('Samples')
plt.xlabel('HR Value')

#Calories Histogram
plt.figure(2)
#plt.subplot(212)
plt.hist(Cals['value'], bins=len(Calstats), range=(Calsmin,Calsmax))
#sns.distplot(Cals);
plt.title('Distribution of Calories Burned Per Minute')
plt.ylabel('Minutes')
plt.xlabel('Calories Burned')

#Steps Histogram
plt.figure(3)
plt.hist(Steps['value'], bins=len(Stepsstats), range=(Stepsmin,Stepsmax))
#sns.distplot(Steps);
axes = plt.gca()
axes.set_ylim([0,40])
plt.title('Distribution of Steps Walked Per Minute')
plt.ylabel('Minutes')
plt.xlabel('Steps Walked')

#Sleep Histogram
fig = plt.figure(4)
plt.hist(SleepValues, range=(0.5,3.5))
#sns.distplot(Sleep);
plt.title('Distribution of Sleep Quality')
plt.ylabel('Minutes')
plt.xlabel('Sleep Quality')
quality = '1.0=Asleep', '2.0=Awake', '3.0=Very Awake'
fig.text(1,.5,quality)

"""Line Plots"""
#HR Over Time
plt.figure(5)
HRtimes=pd.to_datetime(HR['time'])
HRtimes1 = [t.replace(year=2016, month=6, day=13) for t in HRtimes]
plt.plot(HRtimes1, HR['value'])
plt.gcf().autofmt_xdate()
plt.title('Heart Rate Over Time')
plt.ylabel('Heart Rate')
plt.xlabel('Time of Day')

#Calories Over Time
plt.figure(6)
Calstimes=pd.to_datetime(Cals['time'])
Calstimes1 = [t.replace(year=2016, month=6, day=13) for t in Calstimes]
plt.plot(Calstimes1, Cals['value'])
plt.gcf().autofmt_xdate()
plt.title('Calories Over Time')
plt.ylabel('Calories Burned ')
plt.xlabel('Time of Day')

#Steps Over Time
plt.figure(7)
Steptimes=pd.to_datetime(Steps['time'])
Steptimes1 = [t.replace(year=2016, month=6, day=13) for t in Steptimes]
plt.plot(Steptimes1, Steps['value'])
plt.gcf().autofmt_xdate()
plt.title('Steps Over Time')
plt.ylabel('Steps Per Minute ')
plt.xlabel('Time of Day')

#Sleep Quality Over Time
fig=plt.figure(8)
Sleeptimes=pd.to_datetime(Sleep['dateTime'])
Sleeptimes1 = [t.replace(year=2016, month=6, day=13) for t in Sleeptimes]
plt.plot(Sleeptimes1, SleepValues)
plt.gcf().autofmt_xdate()
plt.gca().set_ylim([0,4])
plt.title('Sleep Quality Over Time')
plt.ylabel('Sleep Quality ')
plt.xlabel('Time of Day')
quality = '1.0=Asleep', '2.0=Awake', '3.0=Very Awake'
fig.text(1,.5,quality)

plt.show()


# In[98]:

fig=plt.figure(9)
#datetimesHR1 = [t.replace(year=2016, month=6, day=13) for t in datetimesHR]
plt.plot(HRtimes1, HR['value'], 'r', label="Heart Rate")
plt.plot(Steptimes1, Steps['value'], 'g', label="Steps")
plt.plot(Calstimes1, Cals['value'], 'b', label="Calories")
plt.plot(Sleeptimes1, SleepValues, 'k',label="Sleep")
plt.gcf().autofmt_xdate()
#plt.yscale('log') #Log Scale
plt.legend( loc='center left', numpoints = 1, fancybox=True, shadow=True, bbox_to_anchor=(1, 0.5),ncol=2)
plt.title('Overlay of Time Series Data')
plt.ylabel('Value')
plt.xlabel('Time of Day')
plt.show()

#Compute and plot linear regression stats (Calories vs Steps)
fig=plt.figure(10)
slope, intercept, r_value, p_value, std_err=linregress(Cals['value'],Steps['value']) #x and y are arrays or lists.
plt.plot(Cals['value'],Steps['value'],'.')
plt.title('Scatterplot: Steps vs Calories')
plt.ylabel('Steps per Minute')
plt.xlabel('Calories Burned per Minute')
plt.plot(Cals['value'], np.poly1d(np.polyfit(Cals['value'], Steps['value'], 1))(Cals['value']),label="Regression Line")
plt.legend( loc='center left', numpoints = 1, fancybox=True, shadow=True, bbox_to_anchor=(1, 0.5))
plt.show()
print "r-squared=", (r_value**2) #(measure of how well linear model fits a set of observations)


# In[99]:

## Plotting with seaborn
#sns.set(color_codes=True)
sns.set_palette("GnBu_d")

sns.distplot(HR['value']);

x=np.array(Cals['value'])
y=np.array(Steps['value'])
sns.jointplot(x,y,kind="reg", joint_kws={'color':'green'})


# ## Collect Daily Summaries

# In[ ]:

## TO DO
#Merge summaries into single file


# In[265]:

"""SLEEP SUMMARY"""

SleepStats = fitbit_sleep['sleep']
del SleepStats[0]['minuteData']

SleepSumm=pd.DataFrame(SleepStats)
SleepSumm.to_csv('Sleep-Summary.csv')


# In[289]:

""" ACTIVITIES SUMMARY """

active_list = auth2_client.activities(date)
activities_summary=active_list['summary']

'''Distances Summary'''

distances=activities_summary['distances']
DistSumm=pd.DataFrame(distances)
DistSumm=DistSumm.transpose()
DistSumm.columns = DistSumm.iloc[0]
DistSumm=DistSumm.reindex(DistSumm.index.drop('activity'))
DistSumm.to_csv('Distances-Summary.csv')

'''HR Zones Summary'''

HRzones=activities_summary['heartRateZones'] 
HRSumm=pd.DataFrame(HRzones) 
HRSumm.rows = HRSumm.iloc[0]
HRSumm=HRSumm.rename(index={0:"Out of Range", 1:"Fat Burn", 2:"Cardio", 3:"Peak"})
del HRSumm['name'] #delete duplicated info now that indexes are named
HRflat=HRSumm.values.flatten() #Flatten dataframe into single row
HRSumm2=pd.DataFrame(HRflat)
HRSumm2=HRSumm2.transpose()
HRSumm2=HRSumm2.rename(columns={0:"OutRange.caloriesOut", 1:"OR.max", 2:"OR.min", 3:"OR.minutes", 4:"FatBurn.caloriesOut", 5:"FB.max", 6:"FB.min", 7:"FB.minutes", 8:"Cardio.caloriesOut", 9:"C.max", 10:"C.min", 11:"C.minutes", 12:"Peak.caloriesOut", 13:"P.max", 14:"P.min", 15:"P.minutes"})
HRSumm2.to_csv('HR-Summary.csv')

"""Remaining Activity Data Summary"""

del activities_summary['distances']
del activities_summary['heartRateZones']

ActivitiesSumm=pd.DataFrame(activities_summary.items())
ActivitiesSumm=ActivitiesSumm.transpose()
ActivitiesSumm.columns = ActivitiesSumm.iloc[0]
ActivitiesSumm=ActivitiesSumm.reindex(ActivitiesSumm.index.drop(0))
ActivitiesSumm.to_csv('Activities-Summary.csv')

