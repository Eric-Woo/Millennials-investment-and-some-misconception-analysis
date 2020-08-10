import pandas as pd
import re
import numpy as np


data = pd.read_csv('C:\\Users\\fuzel\\PycharmProjects\\4550\\Fidelity.csv')
print(data.info())
data.drop([0,1],inplace=True)
data.drop(columns=['EndDate','IPAddress','Progress','Duration (in seconds)','Status','RecordedDate',
                   'ResponseId','RecipientLastName','RecipientFirstName','RecipientEmail','LocationLatitude',
                   'LocationLongitude','DistributionChannel','UserLanguage','ExternalReference','Q36'],axis=1,inplace=True)
print(data.info())
data=data[data['Finished']=='TRUE']
print(data.info())
# Before process the data
# Extracting Missing Count and Unique Count by Column
unique_count = []
for x in data.columns:
    unique_count.append([x,len(data[x].unique()),data[x].isnull().sum()])
con=pd.DataFrame(unique_count, columns=["Column","Unique","Missing"]).set_index("Column").T
print(con)
data['Average_income'] = data['Q10'].apply(lambda x: re.sub("[\s+\.\!\/_,$%^*(+\"\')+\]]+|[+——([)?【】“”！，\-。？、"
                                                            "~@#￥%……&*（）]+", '', str(x)))
data['Average_spend'] = data['Q20'].apply(lambda x: re.sub("[\s+\.\!\/_,$%^*(+\"\')+\]]+|[+——([)?【】“”！，\-。"
                                                           "？、~@#￥%……&*（）]+", '', str(x)))
data['Average_income'] = pd.to_numeric(data['Average_income'], errors='coerce')
data['Average_spend'] = pd.to_numeric(data['Average_spend'], errors='coerce')
data.loc[data['Average_spend'] ==0,'Average_speed']=np.nan
data.loc[data['Average_income'] ==0,'Average_income']=np.nan

miss_income_col = data.loc[data['Average_income'].isnull()]['Average_spend'].unique()
print(miss_income_col)
def fill_na_with_mean1(ds, value):
  fill_value = ds.loc[ds['Average_spend'] ==value]['Average_income'].mean()
  condit = ((ds['Average_spend'] == value) & (ds['Average_income'].isnull()))
  ds.loc[condit, 'Average_income'] = ds.loc[condit, 'Average_income'].fillna(fill_value)
for a in miss_income_col:
  fill_na_with_mean1(data, a)

miss_spend_col = data.loc[data['Average_spend'].isnull()]['Average_income'].unique()
print(miss_spend_col)
def fill_na_with_mean2(ds, value):
  fill_value = ds.loc[ds['Average_income'] ==value]['Average_spend'].mean()
  condit = ((ds['Average_income'] == value) & (ds['Average_spend'].isnull()))
  ds.loc[condit, 'Average_spend'] = ds.loc[condit, 'Average_spend'].fillna(fill_value)
for a in miss_spend_col:
  fill_na_with_mean2(data, a)

data.sort_values(by="Average_spend", ascending=True)
data['Average_income']= data['Average_income'].interpolate()
print(data['Average_spend'])