import googleTrends as gt
import auth
import common as c
import json
from time import sleep
from random import uniform
import getpass

# Get Config
with open("config.json", "r") as f:
    config = json.load(f)
count = config["count"]
mobileCount = config["mobileCount"]
delay = config["delay"]
delayRandom = config["delayRandom"]
for login in config["accounts"]:
    cur = 1  # Current Query Number
    if(login["email"] == ""):
        login["email"] = input("Email: ")
    if(login["mode"] == "password"):
        if(login["password"] == ""):
            login["password"] = getpass.getpass(login["email"] + " Password: ")
        account = auth.Account(
            login["email"], password=login["password"])
    elif(login["mode"] == "cookie"):
        account = auth.Account(login["email"], cookie=login["cookie"])
    # Generate Queries
    gen = gt.queryGenerator(1)
    queryList = list(gen.generateQueries(count + mobileCount, set()))
    pcQueryList = queryList[:count]
    mobileQueryList = queryList[count:]
    account.login()  # Login Account on PC
    # Do Searches
    for query in pcQueryList:
        print(login["email"] + " : PC Query " +
              str(cur) + " / " + str(count) + " : " + query)
        account.get(c.searchURL + query)
        sleep(delay + uniform(0, delayRandom))
        cur += 1
    account.logout()  # Logout
    sleep(config["accountDelay"])
    cur = 1  # Reset Current Query Number
    account.login(mobile=True)  # Login Account on Mobile
    # Do Searches
    for query in mobileQueryList:
        print(login["email"] + " : Mobile Query " + str(cur) +
              " / " + str(mobileCount) + " : " + query)
        account.get(c.searchURL + query)
        sleep(delay + uniform(0, delayRandom))
        cur += 1
    account.logout()  # Logout
    sleep(config["accountDelay"])
