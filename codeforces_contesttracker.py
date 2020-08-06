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
    url = "https://codeforces.com/api/contest.list"
    url_dump = requests.get(url)
    data = url_dump.json()
    data=data["result"]
    contests=[]
    for i in data:
        starttime=(i["relativeTimeSeconds"])
        if(starttime<0):
            continue
        completetime=find_totalseconds()
        if(starttime<=completetime):
            contests.append([i["id"],i["name"],i["durationSeconds"]])
        else:
            break 
        break 
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
        
if __name__ == "__main__":
    contest_ids = getContestData()
    user="amruthkumar"
    user_contests=userContests(user)
    participated_contests=defaultdict(list)
    d=defaultdict(list)
    for i in contest_ids:
        d[i[0]]=i[1]
    for i in contest_ids:
        if(i[1] in user_contests):
            participated_contests[i[0]].append(i[1])
            participated_contests[i[0]].append(i[2])
    history=getHistory(user,participated_contests)    
    for i in history:
        history[i].sort()
        print(d[i],*history[i])

    
  