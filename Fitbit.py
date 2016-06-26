
# coding: utf-8

# # Collecting and Visualizing Fitbit Data with Python

# In[14]:

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


# ## Pick a Date

# In[3]:

## TO DO
#Loop through days
date='2016-06-13'


# ## Collect Time Series Data

# In[4]:

## TO DO for all
#Save as CSV's + save all data to single CSV (each day's data on single row)


# In[5]:

"""Timeseries data of Heartrate"""

## TO DO
#Deal with missing values

fitbit_stats = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level='1min')
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


# In[6]:

"""Timeseries data of Calories and Activity Level"""

fitbit_cals = auth2_client.intraday_time_series('activities/log/calories', base_date=date, detail_level='1min')
Calstats = fitbit_cals['activities-log-calories-intraday']['dataset']
f2 = open('dataCals-timeseries.txt', 'w')
Cals = []
CalsTime = []
ActivityLevel= []
for var in range(0, len(Calstats)):
    f2.write(Calstats[var]['time'])
    f2.write("\t")
    f2.write(str(Calstats[var]['level']))
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


# In[7]:

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


# In[8]:

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

# In[9]:

##TO DO
#change sleep data values(10=asleep, 0=not recording, etc), add something to sleep data or sleep graph during awake period 


# In[11]:

"""Histograms"""
#HR Histogram
plt.figure(1)
#plt.subplot(211)
plt.hist(HR, bins=len(stats), range=(HRmin,HRmax))
#sns.distplot(HR);
plt.title('Distribution of HR Values')
plt.ylabel('Samples')
plt.xlabel('HR Value')

#Calories Histogram
plt.figure(2)
#plt.subplot(212)
plt.hist(Cals, bins=len(Calstats), range=(Calsmin,Calsmax))
#sns.distplot(Cals);
plt.title('Distribution of Calories Burned Per Minute')
plt.ylabel('Minutes')
plt.xlabel('Calories Burned')

#Steps Histogram
plt.figure(3)
plt.hist(Steps, bins=len(Stepsstats), range=(Stepsmin,Stepsmax))
#sns.distplot(Steps);
axes = plt.gca()
axes.set_ylim([0,40])
plt.title('Distribution of Steps Walked Per Minute')
plt.ylabel('Minutes')
plt.xlabel('Steps Walked')

#Sleep Histogram
fig = plt.figure(4)
plt.hist(newSleep, range=(0.5,3.5))
#sns.distplot(Sleep);
plt.title('Distribution of Sleep Quality')
plt.ylabel('Minutes')
plt.xlabel('Sleep Quality')
quality = '1.0=Asleep', '2.0=Awake', '3.0=Very Awake'
fig.text(1,.5,quality)

"""Line Plots"""
#HR Over Time
plt.figure(5)
datetimesHR = [datetime.datetime.strptime(t, "%H:%M:%S") for t in HRTime]
datetimesHR1 = [t.replace(year=2016, month=6, day=13) for t in datetimesHR]
#plt.subplot(211)
plt.plot(datetimesHR, HR)
plt.gcf().autofmt_xdate()
plt.title('Heart Rate Over Time')
plt.ylabel('Heart Rate')
plt.xlabel('Time of Day')

#Calories Over Time
plt.figure(6)
datetimesCals = [datetime.datetime.strptime(t, "%H:%M:%S") for t in CalsTime]
datetimesCals1 = [t.replace(year=2016, month=6, day=13) for t in datetimesCals]
#plt.subplot(212)
plt.plot(datetimesCals1, Cals)
plt.gcf().autofmt_xdate()
plt.title('Calories Over Time')
plt.ylabel('Calories Burned ')
plt.xlabel('Time of Day')

#Steps Over Time
plt.figure(7)
datetimesSteps = [datetime.datetime.strptime(t, "%H:%M:%S") for t in StepsTime]
datetimesSteps1 = [t.replace(year=2016, month=6, day=13) for t in datetimesSteps]
plt.plot(datetimesSteps1, Steps)
plt.gcf().autofmt_xdate()
plt.title('Steps Over Time')
plt.ylabel('Steps Per Minute ')
plt.xlabel('Time of Day')

#Sleep Quality Over Time
fig=plt.figure(8)
datetimesSleep = [datetime.datetime.strptime(t, "%H:%M:%S") for t in newSleepTime]
datetimesSleep1 = [t.replace(year=2016, month=6, day=13) for t in datetimesSleep]
plt.plot(datetimesSleep1, newSleep)
plt.gcf().autofmt_xdate()
plt.gca().set_ylim([0,4])
plt.title('Sleep Quality Over Time')
plt.ylabel('Sleep Quality ')
plt.xlabel('Time of Day')
quality = '1.0=Asleep', '2.0=Awake', '3.0=Very Awake'
fig.text(1,.5,quality)

plt.show()


# In[12]:

fig=plt.figure(9)
datetimesHR1 = [t.replace(year=2016, month=6, day=13) for t in datetimesHR]
plt.plot(datetimesHR1, HR, 'r', label="Heart Rate")
plt.plot(datetimesSteps1, Steps, 'g', label="Steps")
plt.plot(datetimesCals1, Cals, 'b', label="Calories")
plt.plot(datetimesSleep1, newSleep, 'k',label="Sleep")
plt.gcf().autofmt_xdate()
#plt.yscale('log') #Log Scale
plt.legend( loc='center left', numpoints = 1, fancybox=True, shadow=True, bbox_to_anchor=(1, 0.5),ncol=2)
plt.title('Overlay of Time Series Data')
plt.ylabel('Value')
plt.xlabel('Time of Day')
plt.show()

#Compute and plot linear regression stats (Calories vs Steps)
fig=plt.figure(10)
slope, intercept, r_value, p_value, std_err=linregress(Cals,Steps) #x and y are arrays or lists.
plt.plot(Cals,Steps,'.')
plt.title('Scatterplot: Steps vs Calories')
plt.ylabel('Steps per Minute')
plt.xlabel('Calories Burned per Minute')
plt.plot(Cals, np.poly1d(np.polyfit(Cals, Steps, 1))(Cals),label="Regression Line")
plt.legend( loc='center left', numpoints = 1, fancybox=True, shadow=True, bbox_to_anchor=(1, 0.5))
plt.show()
print "r-squared=", (r_value**2) #(measure of how well linear model fits a set of observations)


# In[16]:

## Plotting with seaborn
#sns.set(color_codes=True)
sns.set_palette("GnBu_d")

sns.distplot(HR);

x=np.array(Cals)
y=np.array(Steps)
sns.jointplot(x,y,kind="reg", joint_kws={'color':'green'})


# ## Collect Daily Summaries

# In[ ]:

## TO DO
#Merge summaries into single file


# In[ ]:

"""SLEEP SUMMARY"""

SleepStats = fitbit_sleep['sleep']
del SleepStats[0]['minuteData']
keys = SleepStats[0].keys()
keysclean=[x.encode('UTF8') for x in keys]
print keysclean
with open('SleepSummary.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keysclean)
    dict_writer.writeheader()
    dict_writer.writerows(SleepStats)


# In[ ]:

""" ACTIVITIES SUMMARY """
## TO DO
#turn Distances/HR Zone Summaries into csv's

active_list = auth2_client.activities(date)
activity_summary=active_list['summary']

'''Distances Summary'''

f5 = open('distances-summary.txt', 'w')
distances=activities_summary['distances']
for var in range(0, len(distances)):
    value=str(distances[var]['distance'])
    f5.write(value)
    f5.write("\t")
    activity=str(distances[var]['activity'])
    f5.write(activity)
    f5.write("\n")
f5.close()

'''HR Zones Summary'''

f6 = open('HRzones-summary.txt', 'w')
HRzones=activities_summary['heartRateZones']
for var in range(0, len(HRzones)):
    maxHR=str(HRzones[var]['max'])
    f6.write(maxHR)
    f6.write("\t")
    caloriesOut=str(HRzones[var]['caloriesOut'])
    f6.write(caloriesOut)
    f6.write("\t")
    minutes=str(HRzones[var]['minutes'])
    f6.write(minutes)
    f6.write("\t")   
    name=str(HRzones[var]['name'])
    f6.write(name)
    f6.write("\t")
    minHR=str(HRzones[var]['min'])
    f6.write(minHR)
    f6.write("\n")
f6.close()

"""Remaining Activity Data"""

del activity_summary['distances']
del activity_summary['heartRateZones']

keys = activity_summary.keys()
keysclean=[x.encode('UTF8') for x in keys]
with open('ActivitiesSummary.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keysclean)
    dict_writer.writeheader()
    dict_writer.writerow(activity_summary)

