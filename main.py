# -*- coding: UTF-8 -*-
import json
import sqlite3
from urllib.parse import quote
import base64
import datetime
import requests

def b64(data):
    return str(base64.b64encode(data.encode("utf-8")), "utf-8")

def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))


# 下载并解析getVpsInfo
getVpsInfo = "/data/data/com.termux/files/home/ss/getVpsInfo.json"
getVpsInfoUrl = "http://104.168.190.184:9555/api/getVpsInfo"
# 来源于 https://raw.githubusercontent.com/Kerr1Gan/Kerr1Gan.github.io/master/galaxy/scripts/config.json 的第一个 url + "/api/getVpsInfo"

print("下载信息文件")

r1 = requests.get(getVpsInfoUrl) 
with open(getVpsInfo,'wb') as f:
    f.write(r1.content)


with open(getVpsInfo) as f:
    info = json.load(f)

print("读取数据库")
# sqlite转换为字典
db_path = '/data/data/com.termux/files/home/ss/profile.db'
con = sqlite3.connect(db_path, check_same_thread=False)
con.row_factory = dict_factory
cur = con.cursor()
cur.execute("select name,host,remotePort,password,plugin from Profile")
dict_data = cur.fetchall()

# print(dict_data)



print("匹配节点")

isOk=[]
for i in range(len(info)):
    for j in range(len(dict_data)):
        if (info[i]['ip']==dict_data[j]['host']):
            info[i]['password']=dict_data[j]['password']
            info[i]['plugin']=dict_data[j]['plugin']
            info[i]['port']=dict_data[j]['remotePort']


    if (info[i]['isAlive'] and info[i]['password']!=''):
        isOk.append(info[i])


for i in range(len(isOk)):
    del isOk[i]['ssIpMsg']
    del isOk[i]['updateTs']
    del isOk[i]['ssCount']
    del isOk[i]['isAlive']
    isOk[i]['sslink']="ss://" + b64("aes-256-gcm:" + isOk[i]['password']) + "@" + isOk[i]['ip'] + ":"+ str(isOk[i]['port']) +"?plugin=" + quote(isOk[i]['plugin']) + "#" + quote(isOk[i]['title'])


#print(json.dumps(isOk))
print("获取节点个数：",len(isOk))

infoJSON="/data/data/com.termux/files/home/ss/info.json"
with open(infoJSON, "w") as f:
    f.write(json.dumps(isOk))

print("写入配置文件")

dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

timeDict={}
timeDict['time']=dt

timeJSON="/data/data/com.termux/files/home/ss/time.json" 
with open(timeJSON, "w") as f: 
    f.write(json.dumps(timeDict))
print("更新时间：",dt)
#print(json.dumps(timeDict))
