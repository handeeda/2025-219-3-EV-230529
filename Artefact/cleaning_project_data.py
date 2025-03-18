import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("leaving-cert-project-test-firebase-adminsdk-fbsvc-9338e25e45.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://leaving-cert-project-test-default-rtdb.europe-west1.firebasedatabase.app/'})
#from graphs_python import earthquake_project
ref = db.reference("/clean_data")

# f = open("eearthquake data 1990_2023.csv",'r')
# f.readline()
df=pd.read_csv("Eartquakes-1990-2023.csv")
df=df[df["data_type"].str.contains("earthquake")]
print(df.info())
df = df.drop(df.columns[[0, 1, 2,3,4,5,8,9]], axis=1)
print(df.info())
#only keep year of date string
#example: 1990-01-01 00:22:33.990000+00:00 -> 1990
placeholder = df['date'].str
pattern2 = placeholder[:4]
df['date'] = pattern2
#remove invalid characters from country names
df['state']=df['state'].str.replace(' ','')
placeholder = df['state'].str
pattern2 = placeholder.replace('.','')
df['state'] = pattern2
placeholder = df['state'].str
pattern2 = placeholder.replace('-','')
df['state'] = pattern2
placeholder = df['state'].str
pattern2 = placeholder.replace('/','')
df['state'] = pattern2

series_dict = df.to_dict() 
print(series_dict)
#df.to_csv("clean_data_year_test.csv",index=False)
#df = pd.read_csv('clean_data_year_test.csv')
#group data frame information by country
data_by_country = df.groupby("state")
print('here1')
data_for_firebase = {}
strongest_earthquake_year_dic={}
for country_name, country_data_frame in data_by_country:
        if country_name not in data_for_firebase:
            data_for_firebase[country_name] = {}
        total_magnitude=0
        total_depth=0
        count=0
        
        for rowIndex, row in country_data_frame.iterrows():
            #print(row['date'])
            if row['date'] not in data_for_firebase[country_name]:
                data_for_firebase[country_name][row['date']] = {}
                data_for_firebase[country_name][row['date']]['Magnitude'] =0
                data_for_firebase[country_name][row['date']]['depth'] = 0
                data_for_firebase[country_name][row['date']]['count']=0
            data_for_firebase[country_name][row['date']]['Magnitude']=round(data_for_firebase[country_name][row['date']]['Magnitude'],2)+round(row['magnitudo'],2)
            data_for_firebase[country_name][row['date']]['depth']=data_for_firebase[country_name][row['date']]['depth']+row['depth']
            data_for_firebase[country_name][row['date']]['count']=data_for_firebase[country_name][row['date']]['count']+1
            
            #"""""""""""""""""""""""""""""""""""""""""""""""""""
            
            
            
          
            if row['date'] not in strongest_earthquake_year_dic:
                strongest_earthquake_year_dic[row['date']] = {'Magnitude':round(row['magnitudo'],2),'Country':country_name}
                

            else:
               # print(type(row['date']))
               # if row['date'] == 2020:
                    if strongest_earthquake_year_dic[row['date']]['Magnitude'] < round(row['magnitudo'],2):
                        #print('Changing value:',row['date'], strongest_earthquake_year_dic[row['date']]['Magnitude'],'--------',round(row['magnitudo'],2),country_name)
                        strongest_earthquake_year_dic[row['date']] = {'Magnitude':round(row['magnitudo'],2),'Country':country_name}
                    

#          
# print(strongest_earthquake_year_dic)
            
            
            
            
ref = db.reference('/'+"clean_data")
print(data_for_firebase)
ref.set(data_for_firebase)            
            
            
            
            
            
            #""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#             print(data_for_firebase)
# print('here')
ref = db.reference('/')
ref = db.reference('/strongest_earthquake_by_year')
ref.set(strongest_earthquake_year_dic)

