# importing our libraries
import pandas as pd
import numpy as np

# loading our url

# then storing the url location of our dataset to the variable url
url = 'http://bit.ly/autolib_dataset'

# We will read the dataset from above url and store the dataframe in the variable df
df = pd.read_csv(url)
df.head(3)

df.info()

# checking for the shape of the data frame
df.shape

# checking for null values for every column
df.isnull().sum()

df.columns

df.describe()

# Let us start cleaning the data
# duplicates
# the columns cars and blue car counter both contain values that are a duplicate of each other
# therefore one of the columns will be dropped

df1 = df.drop(columns=['Cars'])

# previewing the new table
df1.head(3)

# checking for duplicate rows and dropping them
df1 = df1.drop_duplicates()
df1.head(3)

df1.duplicated().sum()

"""There are no other duplicates"""

# checking for shape

df1.shape

# select only the rows where status is ok

df_2 = df1[df1.Status == 'ok']

# check shape to ensure we only have relevant rows
df_2.shape

# dropping irrelevant columns

df2 = df_2.drop(columns=['Scheduled at', 'Displayed comment', 'Geo point'])
df2.head(2)

# combining the columns year, day and time then renaming them
# then dropping the irrelevant columns

df2['DateTime'] = pd.to_datetime(df2[['year', 'month', 'day', 'hour', 'minute']])

df2 = df2.drop(columns=['year', 'month', 'day', 'hour', 'minute'])

df2.head(2)

# checking current dataset info
df2.info()
df2.shape

# dropping all rows where the value of "bluecar counter" is less than 0 or greater than 7

nr = df2[(df2['Bluecar counter'] < 0) & (df2['Bluecar counter'] > 7)].index
df2.drop(nr, inplace=True)
df2

# checking if any of the rows dropped
df2.shape

# creating a new dataframe where city is paris

df_paris = df2[df2.City == 'Paris']
df_paris.head(2)

df_paris.info()

# splitting date and timein paris
#
new_dates, new_times = zip(*[(d.date(), d.time()) for d in df_paris['DateTime']])

paris1 = df_paris.assign(Date=new_dates, Time=new_times)
paris1.head(2)

paris1.sample(5)

# arranging the data frame from day 1 to day 9

paris1 = df_paris.sort_values(['ID', 'DateTime'], ascending=[True, True])
paris1

# previewing the new dataframe and checking if it has been sorted
paris1.head()

paris1['Hour'] = paris1['DateTime'].dt.hour
paris1.head()

# reseting indexes afer sorting

paris1 = paris1.reset_index(drop=True)
paris1.head(5)

paris1.drop(columns={'Hour'})
paris1.head(5)

# to get successive Bluecar Counters

paris1["Diff_Bluecar"] = paris1["Bluecar counter"].diff(-1)
paris1.head()

# to get the most popular day
paris1.loc[0, 'DateTime'].day_name()

# highest value for bluecar counter
column = paris1["Bluecar counter"]

max_value = column.max()
max_value

# most popular time when all cars are not returned yet
empty = paris1.loc[paris1['Bluecar counter'] == 0].groupby('Hour')['Hour'].count().sort_values(
    ascending=False).nlargest(1)
empty

# worst hours for business in the 24hr system

full = paris1.loc[paris1['Bluecar counter'] >= 3].groupby('Hour')['Hour'].count().sort_values(
    ascending=False).nlargest()
full

# worst dates for business
days = paris1.loc[paris1['Bluecar counter'] >= 3].groupby('DateTime')['Hour'].count().sort_values(
    ascending=False).nlargest()
days

# most popular hour for picking cars in 24hr system

paris1[(paris1['Station type'] == 'station') & (paris1['Status'] == 'ok')].groupby('Hour')['Hour'].count().sort_values(
    ascending=False).nlargest(1)

# most popular station

paris1[(paris1['Station type'] == 'station') & (paris1['Status'] == 'ok')].groupby('Public name')[
    'Public name'].count().sort_values(ascending=False).nlargest()

# most popular postal code
paris1[(paris1['Station type'] == 'station') & (paris1['Status'] == 'ok')].groupby('Postal code')[
    'Postal code'].count().sort_values(ascending=False).nlargest()

# to get popular day and time

paris1.loc[0, 'DateTime']

# selecting specific columns.

selected_cols = ['Diff_Bluecar', 'Hour', 'DateTime']
data = paris1[selected_cols]
data

# checking data for utilib counter
for_utilib = ['Utilib counter', 'Utilib 1.4 counter', 'Station type', 'Postal code', 'DateTime', 'Hour', 'Status']

data1 = paris1[for_utilib]
data1

# checking popular postal code for utilib counter
data1[(data1['Station type'] == 'station') & (data1['Status'] == 'ok')].groupby('Postal code')
['Postal code'].count().sort_values(ascending=False).nlargest()
