
# coding: utf-8

# # Collecting and Visualizing Fitbit Data with Python

# In[491]:

#!/usr/bin/python      
get_ipython().magic(u'matplotlib inline')

import fitbit
import matplotlib.pyplot as plt
import gather_keys_oauth2 as Oauth2
import numpy as np
import datetime
import pandas as pd


# ## Access Fitbit API

# In[492]:

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

# In[493]:

date='2016-06-13'


# ## Collect Time Series Data

# In[494]:

"""Timeseries data of Heartrate"""

fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level='1sec')
stats = fitbit_stats['activities-heart-intraday']['dataset']
f1 = open('dataHR-timeseries.txt', 'w')
HR = []
HRTime = []
for var in range(0, len(stats)):
    f1.write(stats[var]['time'])
    f1.write("\t")
    f1.write(str(stats[var]['value']))
    f1.write("\n")
    HR = HR + [stats[var]['value']]
    HRTime = HRTime + [stats[var]['time']]
f1.close()

newHRTime=[str(x.encode('utf-8')) for x in HRTime] 

print "----HEART RATE STATS----"
print 'First 10 Samples of HR Values:',HR[:10]
print 'Corresponding Time Stamps:', newHRTime[:10]
print 'Total HR Samples (variable):', len(HR)

HRmax = np.max(HR)
HRmin = np.min(HR)
HRmean = np.mean(HR)
print "Avg HR:", HRmean, "Max HR:", HRmax, "Min HR:", HRmin


# In[495]:

"""Timeseries data of Calories and Activity Level"""
# Add activity level to text file
fitbit_cals = auth2_client.intraday_time_series('activities/log/calories', base_date=date, detail_level='1min')
Calstats = fitbit_cals['activities-log-calories-intraday']['dataset']
f2 = open('dataCals-timeseries.txt', 'w')
Cals = []
CalsTime = []
ActivityLevel= []
for var in range(0, len(Calstats)):
    f2.write(Calstats[var]['time'])
    f2.write("\t")
    f2.write(str(Calstats[var]['value']))
    f2.write("\n")
    Cals = Cals + [Calstats[var]['value']]
    CalsTime = CalsTime + [Calstats[var]['time']]
    ActivityLevel = ActivityLevel + [Calstats[var]['level']]
f2.close()

newCalsTime=[str(x.encode('utf-8')) for x in CalsTime] 

print "----CALORIE STATS----"
print 'First 10 Samples of Calorie Values:',Cals[:10]
print 'Corresponding Time Stamps:', newCalsTime[:10]
print 'Total Calorie Samples (fixed):', len(Cals)

Calsmax = np.max(Cals)
Calsmin = np.min(Cals)
Calsmean = np.mean(Cals)
CalsSumm = np.sum(Cals)

print "Total Calories burned:", CalsSumm, "Min Calories burned in a minute:", Calsmin, "Max Calories burned in a minute:", Calsmax 


# In[496]:

"""Timeseries data of Steps"""

fitbit_steps = auth2_client.intraday_time_series('activities/steps', base_date=date, detail_level='1min')
Stepsstats = fitbit_steps['activities-steps-intraday']['dataset']
f3 = open('dataSteps-timeseries.txt', 'w')
Steps = []
StepsTime = []
for var in range(0, len(Stepsstats)):
    f3.write(Stepsstats[var]['time'])
    f3.write("\t")
    f3.write(str(Stepsstats[var]['value']))
    f3.write("\n")
    Steps = Steps + [Stepsstats[var]['value']]
    StepsTime = StepsTime + [Stepsstats[var]['time']]
f3.close()

newStepsTime=[str(x.encode('utf-8')) for x in StepsTime] 

print "----STEPS STATS----"
print 'First 10 Samples of Steps Per Minute:',Steps[:10]
print 'Corresponding Time Stamps:', newStepsTime[:10]
print 'Total Samples (fixed):', len(Steps)


Stepsmax = np.max(Steps)
Stepsmin = np.min(Steps)
Stepsmean = np.mean(Steps)
print 'Avg Steps:', Stepsmean, 'Max Steps:', Stepsmax


# In[497]:

"""Timeseries data of Sleep"""
fitbit_sleep = auth2_client.sleep(date)
sleepstats = fitbit_sleep['sleep'][0]['minuteData']

f4 = open('dataSleep-timeseries.txt', 'w')
Sleep = []
SleepTime = []
for var in range(0, len(sleepstats)):
    f4.write(sleepstats[var]['dateTime'])
    f4.write("\t")
    f4.write(str(sleepstats[var]['value']))
    f4.write("\n")
    Sleep = Sleep + [sleepstats[var]['value']]
    SleepTime = SleepTime + [sleepstats[var]['dateTime']]
f4.close()

newSleep=[int(x.encode('utf-8')) for x in Sleep]
newSleepTime=[str(x.encode('utf-8')) for x in SleepTime]


print "----SLEEP STATS----"
print 'First 10 Samples of Sleep Time:',newSleep[:10]
print 'Corresponding Time Stamps:', newSleepTime[:10]
print 'Total Minutes in Bed (variable):', len(Sleep)
print "Minutes Asleep:", newSleep.count(1)
print "Minutes Awake:", newSleep.count(2)
print "Minutes Very Awake:", newSleep.count(3)


# ## Plots

# In[541]:

## TO DO
# Fix "Sleep Quality Over Time", only include timestamps when sleeping 
# Subplots


# In[490]:

"""Histograms"""
#HR Histogram
plt.figure(1)
#plt.subplot(211)
plt.hist(HR, bins=len(stats), range=(HRmin,HRmax))
plt.title('Distribution of HR Values')
plt.ylabel('Samples')
plt.xlabel('HR Value')

#Calories Histogram
plt.figure(2)
#plt.subplot(212)
plt.hist(Cals, bins=len(Calstats), range=(Calsmin,Calsmax))
plt.title('Distribution of Calories Burned Per Minute')
plt.ylabel('Minutes')
plt.xlabel('Calories Burned')

#Steps Histogram
plt.figure(3)
plt.hist(Steps, bins=len(Stepsstats), range=(Stepsmin,Stepsmax))
axes = plt.gca()
axes.set_ylim([0,40])
plt.title('Distribution of Steps Walked Per Minute')
plt.ylabel('Minutes')
plt.xlabel('Steps Walked')

#Sleep Histogram
fig = plt.figure(4)
plt.hist(newSleep, range=(0.5,3.5))
plt.title('Distribution of Sleep Quality')
plt.ylabel('Minutes')
plt.xlabel('Sleep Quality')
quality = '1.0=Asleep', '2.0=Awake', '3.0=Very Awake'
fig.text(1,.5,quality)

"""Line Plots"""
#HR Over Time
plt.figure(5)
datetimesHR = [datetime.datetime.strptime(t, "%H:%M:%S") for t in HRTime]
#plt.subplot(211)
plt.plot(datetimesHR, HR)
plt.gcf().autofmt_xdate()
plt.title('Heart Rate Over Time')
plt.ylabel('Heart Rate')
plt.xlabel('Time of Day')

#Calories Over Time
plt.figure(6)
datetimesCals = [datetime.datetime.strptime(t, "%H:%M:%S") for t in CalsTime]
#plt.subplot(212)
plt.plot(datetimesCals, Cals)
plt.gcf().autofmt_xdate()
plt.title('Calories Over Time')
plt.ylabel('Calories Burned ')
plt.xlabel('Time of Day')

#Steps Over Time
plt.figure(7)
datetimesSteps = [datetime.datetime.strptime(t, "%H:%M:%S") for t in StepsTime]
plt.plot(datetimesSteps, Steps)
plt.gcf().autofmt_xdate()
plt.title('Steps Over Time')
plt.ylabel('Steps Per Minute ')
plt.xlabel('Time of Day')

#Sleep Quality Over Time
fig=plt.figure(8)
datetimesSleep = [datetime.datetime.strptime(t, "%H:%M:%S") for t in newSleepTime]
plt.plot(datetimesSleep, newSleep)
plt.gcf().autofmt_xdate()
plt.gca().set_ylim([0,4])
plt.title('Sleep Quality Over Time')
plt.ylabel('Sleep Quality ')
plt.xlabel('Time of Day')
quality = '1.0=Asleep', '2.0=Awake', '3.0=Very Awake'
fig.text(1,.5,quality)


plt.show()


# ## Collect Daily Summaries

# In[ ]:

## TO DO
#remove unicode u
#save as text/csv files


# In[535]:

"""Sleep Daily Summary"""
#1 API call

fitbit_sleep = auth2_client.sleep(date)
SleepStats = fitbit_sleep['sleep']
print SleepStats


# In[538]:

"""Calories burned while Active"""
active_cals = auth2_client.time_series('activities/activityCalories', base_date= date ,end_date=date)
print active_cals


# In[539]:

"""Activity Log"""
active_list = auth2_client.activities(date)
print active_list


# In[540]:

"""Heart Rate Daily Summary"""
fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date=date)
stats = fitbit_stats['activities-heart']
print stats

