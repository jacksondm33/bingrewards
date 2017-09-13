import googleTrends as gt
import auth
import common as c
import json
from time import sleep
from random import uniform

# Get Config
with open("config.json", "r") as f:
    config = json.load(f)
count = config["count"]
mobileCount = config["mobileCount"]
delay = config["delay"]
delayRandom = config["delayRandom"]
cur = 1 # Current Query Number
account = auth.Account(config["email"], config["password"]) # Init Account
# Generate Queries
gen = gt.queryGenerator(1)
queryList = list(gen.generateQueries(count + mobileCount, set()))
pcQueryList = queryList[:count]
mobileQueryList = queryList[count:]
account.login() # Login Account on PC
# Do Searches
for query in pcQueryList:
    print("PC Query " + str(cur) + " / " + str(count) + " : " + query)
    account.get(c.searchURL + query, cookies=account.cookies)
    sleep(delay + uniform(0, delayRandom))
    cur += 1
account.logout() # Logout
sleep(config["accountDelay"])
cur = 1 # Reset Current Query Number
account.login(mobile=True) # Login Account on Mobile
# Do Searches
for query in mobileQueryList:
    print("Mobile Query " + str(cur) + " / " + str(mobileCount) + " : " + query)
    account.get(c.searchURL + query, cookies=account.cookies)
    sleep(delay + uniform(0, delayRandom))
    cur += 1
account.logout() # Logout


  
