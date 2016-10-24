import os
from AutoTweet import MainProcess

apps = open('.\\config.txt','r').readlines()
address = "http://www.twitter.com/login"
user=""
passwd=""
for a in apps:
    if a.find("Username:") != -1:
        user = a.split(":")[1].strip()
        break

for b in apps:
    if b.find("Password:") != -1:
        passwd = b.split(":")[1].strip()
        break
try:
    MainProcess(address, user, passwd)
except:
    traceback.print_exc()
    raw_input(" ")
