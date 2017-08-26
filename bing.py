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
# Generate PC Queries
gen = gt.queryGenerator(1)
querySet = gen.generateQueries(count, set())
account.login() # Login Account on PC
# Do Searches
for query in querySet:
    print("PC Query " + str(cur) + " / " + str(count) + " : " + query)
    account.get(c.searchURL + query, cookies=account.cookies)
    sleep(delay + uniform(0, delayRandom))
    cur += 1
account.logout() # Logout
sleep(config["accountDelay"])
cur = 1 # Reset Current Query Number
# Generate Mobile Queries
gen = gt.queryGenerator(1)
querySet = gen.generateQueries(mobileCount, set())
account.login(mobile=True) # Login Account on Mobile
# Do Searches
for query in querySet:
    print("Mobile Query " + str(cur) + " / " + str(mobileCount) + " : " + query)
    account.get(c.searchURL + query, cookies=account.cookies)
    sleep(delay + uniform(0, delayRandom))
    cur += 1
account.logout() # Logout


  
