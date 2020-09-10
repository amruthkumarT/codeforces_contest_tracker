import requests 
import json
import datetime
from collections import defaultdict

def find_totalseconds():
    a=str(datetime.datetime.now())
    days=int(a[8:10])
    hours=int(a[11:13])
    minutes=int(a[14:16])
    seconds=int(a[17:19])
    totalseconds=days*24*3600+hours*3600+minutes*60+seconds
    return(totalseconds)

def getContestData():
    global div2
    global div3
    url = "https://codeforces.com/api/contest.list"
    url_dump = requests.get(url)
    data = url_dump.json()
    data=data["result"]
    contests=[]
    completetime=find_totalseconds()
    for i in data:
        starttime=(i["relativeTimeSeconds"])
        name=i['name']
        if('Div. 1' in name):
            continue
        if(starttime<0):
            continue
        if(starttime<=completetime):
            contests.append([i["id"],i["name"],i["durationSeconds"]])
        else:
            break 
        if('Div. 2' in name):
            div2+=1
        if('Div. 3' in name):
            div3+=1
    return(contests)

def userContests(user):
    url="https://codeforces.com/api/user.rating?handle="+user
    url_dump=requests.get(url)
    data = url_dump.json()
    data=data["result"]
    contests=[]
    for i in data:
        contests.append(i["contestName"])
    return(contests)

def getHistory(user,participated_contests):
    url="https://codeforces.com/api/user.status?handle="+user
    url_dump=requests.get(url)
    data=url_dump.json()
    data=data["result"]
    d=defaultdict(list)
    for i in data:
        if('contestId' not in i):
            continue
        id=i["contestId"]
        if(id not in participated_contests):
            continue 
        if(i["verdict"]!="OK"):
            continue
        duration=participated_contests[id][1]
        time=i["relativeTimeSeconds"]
        if(time<=duration):
            k=i["problem"]
            d[id].append(k["index"])
    return(d)

def find_rated(users):
    unrated=0
    greenrated=0
    for i in users:
        user=users[i]
        url="https://codeforces.com/api/user.info?handles="+user
        url_dump=requests.get(url)
        data=url_dump.json()
        data=data['result'][0]
        if('rating' not in data):
            unrated+=1
            #print(user,"unrated")
        elif(data['rating']>=1200):
            greenrated+=1
            #print(user,"green rated")
    print("Green rated percentage: ",(greenrated/len(users))*100)
    print("Unrated perentage: ",(unrated/len(users))*100)
        
div2=0
div3=0
contest_ids = getContestData()
print("Total CF contest in this month: ")
print("Div 2",div2)
print("Div 3",div3)
d=defaultdict(list)
for i in contest_ids:
    d[i[0]]=i[1]
users={'K.N.Anantha nandanan':'ananthanAN2k',
    'Shashank Priyadarshi':'robustTechie',
    'Ashwin R':'ashwinkey04',
    'Akshay V':'akymaster007',
    'Sashmita Raghav':'sassycode',
    'Akshay Praveen Nair':'Xacker11',
    'Mayukh Deb':'mayukhmainak2000',
    'Nehal Nevle':'nehalnevle',
    'Govind Goel':'ggoel19017',
    'Giwansh Aryan':'aryan_001',
    'Navneet Kumar':'code_bull',
    'Siddharth':'siddharthc30',
    'Mainak Deb':'The_Gypsy',
    'Rishab Mudliar':'WalkingSticks6677',
    'Ajay Prabhakar':'chromicle',
    'Harshith Pabbati':'Harshithpabbati',
    'Abhijit Ramesh':'abhijitramesh2k',
    'Swathi Kasikala':'swathi_kasikala',
    'Athira Nair K':'stormborn',
    'Puneeth Chanda':'puneeth_chanda',
    'Akhil K G':'akhilam512',
    'Yash Khare':'yashk2000',
    'Shivangi':'SAforce',
    'Veerasamy S':'sevagen123',
    'T. Vishwaak Chandran':'Xerous'}
status=defaultdict(int)
print()
print("First years")
for name in users:
    user=users[name]
    if(user=='chromicle'):
        print()
        print()
        print("Third years")
    user_contests=userContests(user)
    participated_contests=defaultdict(list)
    for i in contest_ids:
        if(i[1] in user_contests):
            participated_contests[i[0]].append(i[1])
            participated_contests[i[0]].append(i[2])
    history=getHistory(user,participated_contests)
    print(name+' ['+str(len(participated_contests))+'/'+str(len(contest_ids))+']')
print()
find_rated(users)
