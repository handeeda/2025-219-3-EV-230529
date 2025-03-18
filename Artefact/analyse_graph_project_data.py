import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numbers
import matplotlib.pyplot as plt

cred = credentials.Certificate("leaving-cert-project-test-firebase-adminsdk-fbsvc-9338e25e45.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://leaving-cert-project-test-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference('/clean_data')
data=ref.get()
print(data)

#average magnitude

average_magnitude_dic={}
average_magnitude_over_time_for_each_country = {}
def average_magnitude(c,i):
    totalMagnitudes = 0
    count = 0
    average_magnitude_dic[c]={}
    for year,magnitudes in i.items():
        average_magnitude_dic[c][year]=round(magnitudes["Magnitude"]/magnitudes["count"],2)
        totalMagnitudes = totalMagnitudes + average_magnitude_dic[c][year]
        count = count + 1
    average_magnitude_over_time_for_each_country[c] = round(totalMagnitudes/count,2)

for country,info in data.items():
    
    average_magnitude(country,info)
print(average_magnitude_dic)
        
#average depth
average_depth_dic={}
def average_depth(c,i):
    average_depth_dic[c]={}
    for year,depths in i.items():
        average_depth_dic[c][year]=round(depths["depth"]/depths["count"],2)

for country,info in data.items():
    print(country)
    average_depth(country,info)
print(average_depth_dic["AR"])

##questions
##experienced_earthquakes
experienced_earthquakes_dic={}
def experienced_earthquakes(c,i):
    
    if c not in experienced_earthquakes_dic:
        experienced_earthquakes_dic[c] = {}

        total_earthquakes = 0
        for year, count in i.items():
            total_earthquakes += count["count"] 

        experienced_earthquakes_dic[c] = total_earthquakes

for country, info in data.items():
    experienced_earthquakes(country, info)

print(experienced_earthquakes_dic["Alaska"])

##strongest_earthquake
strongest_earthquake_year_dic={}
def strongest_earthquake(c,i):
#     if c not in strongest_earthquake_dic:
#         strongest_earthquake_dic[c] = {}
        for year, magnitude in i.items():
            #print('this is',year,magnitude)
            if year not in strongest_earthquake_year_dic:
                strongest_earthquake_year_dic[year] = round(magnitude['Magnitude'],2)
            else:
                if strongest_earthquake_year_dic[year] < magnitude['Magnitude']:
                    strongest_earthquake_year_dic[year] = round(magnitude['Magnitude'],2)      
           # print(strongest_earthquake_year_dic)
        print(country, magnitude['Magnitude'])
for country, info in data.items():
    strongest_earthquake(country, info)
print("========================================\n\n\n")
print(strongest_earthquake_year_dic)

##################
# 
#   
# country ="California"
# print(list(average_magnitude_dic[country].keys()))
# #average magnitude graph
# fig, ax = plt.subplots()
# 
# #fruits = ['apple', 'blueberry', 'cherry', 'orange']
# counts = list(average_magnitude_dic[country].values())
# bar_labels = list(average_magnitude_dic[country].keys())
# #bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']
# 
# ax.bar(bar_labels, counts)
# 
# ax.set_ylabel('magnitude')
# ax.set_xlabel('years')
# ax.set_title('average earthquake magnitude per year '+country)
# #ax.legend(title='Fruit color')
# 
# plt.show()
#

####
# country =input("write a country: ")
# 
#     if country not in info.items:
#         print("please write a country in database...")
#         country =input("write a country: ")
#     
# print(list(average_depth_dic[country].keys()))
#####

##average depth graph
#fig, ax = plt.subplots()

counts = list(average_depth_dic[country].values())
bar_labels = list(average_depth_dic[country].keys())

#ax.bar(bar_labels, counts)
plt.bar(bar_labels, counts)
plt.title("average earthquake depth per year")
plt.xlabel("years")
plt.ylabel("depth")
plt.show()
# ax.set_ylabel('depth')
# ax.set_xlabel('years')
# ax.set_title('average earthquake depth per year '+country)
#ax.legend(title='Fruit color')

##average magnitude graph
counts = list(average_magnitude_dic[country].values())
bar_labels = list(average_magnitude_dic[country].keys())
plt.bar(bar_labels, counts)
plt.xlabel("years")
plt.ylabel("magnitude")
plt.title("average earthquake magnitude per year")

# ax.bar(bar_labels, counts)
# 
# ax.set_ylabel('magnitude')
# ax.set_xlabel('years')
# ax.set_title('average earthquake magnitude per year '+country)
plt.show()
#counts = list(average_magnitude_dic[country].values())



ref = db.reference('/')
ref = db.reference('/average magnitude')
ref.set(average_magnitude_dic)
ref = db.reference('/')
ref = db.reference('/average depth')
ref.set(average_depth_dic)
ref = db.reference('/')
ref = db.reference('/number_of_experienced_earthquakes')
ref.set(experienced_earthquakes_dic)
ref = db.reference('/')
ref = db.reference('/average_magnitude_over_time_by_country')
ref.set(average_magnitude_over_time_for_each_country)





