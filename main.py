import json
import base64
import datetime
from urllib.parse import quote

def b64(data):
    return str(base64.b64encode(data.encode("utf-8")), "utf-8")

# tsudo cp /data/data/com.galaxylab.ss/no_backup/shadowsocks.conf /data/data/com.termux/files/home/ss/shadowsocks.conf
filename = "/data/data/com.termux/files/home/ss/shadowsocks.conf"
with open(filename) as f:
    conf = json.load(f)

# print(conf)
if ('v2ray' in conf['plugin']):
    conf['plugin']="v2ray"
else:
    conf['plugin']=""

sslink="ss://" + b64(conf['method'] + ":" + conf['password']) + "@" + conf['server'] + ":"+ str(conf['server_port']) +"?plugin="+ quote(conf['plugin'])
#  + "#" + quote(conf['title'])
print(sslink)


info={}
info['ip']=conf['server']
info['password']=conf['password']
info['plugin']=conf['plugin']
info['port']=conf['server_port']
info['sslink']=sslink


infoJSON="/data/data/com.termux/files/home/ss/info.json"
with open(infoJSON, "w") as f:
    f.write(json.dumps(info))

print("-Write info.json")


timeDict = {}
dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
timeDict['time'] = dt

timeJSON="/data/data/com.termux/files/home/ss/time.json"
with open(timeJSON, "w") as f: 
    f.write(json.dumps(timeDict))
print("-Update time:",dt)
