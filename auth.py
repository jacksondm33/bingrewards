import requests
import common as c
import time
from bs4 import BeautifulSoup
from random import randint
from http.cookiejar import Cookie

class Account:

    headers = c.headers
    params = {}
    data = {"i13":"0", "type":"11", "LoginOptions":"3", "lrt":"", "ps":"2", "psRNGCDefaultType":"", "psRNGCEntropy":"", "psRNGCSLK":"", "canary":"", "ctx":"", "NewUser":"1", "FoundMSAs":"", "fspost":"0", "i21":"0", "i2":"1", "i17":"0", "i18":"__ConvergedLoginPaginatedStrings%7C1%2C__ConvergedLogin_PCore%7C1%2C", "i19":"2" + str(randint(0, 5000))}
    proxies = {"http":"127.0.0.1:8080", "https":"127.0.0.1:8080"}

    def __init__(self, email, password, mode):
        self.data["login"] = email
        self.data["loginfmt"] = email
        self.data["passwd"] = password
        self.mode = mode
        
    def login(self, mobile=False):
        if self.mode == "cookie":
            # Login with cookie
            self.CookieLogin()
        else: # Regular Login with email and password
            postURL = self.preLogin()
            res = self.post(postURL, cookies=self.cookies, data=self.data)
            # Parse HTML Form
            form = BeautifulSoup(res.text, "html.parser").findAll("form")[0] # Get Form
            params = dict()
            for field in form:
                params[field["name"]] = field["value"] # Add each field to params
            self.headers["Host"] = c.host # Set Host to Bing Server
            res = self.post(form.get("action"), cookies=self.cookies, data=params)
            self.cookies = res.cookies # Set Cookies
            
        if(mobile):
            self.headers = c.mobileHeaders

    def preLogin(self):
        res = self.get(c.hostURL)
        # Get Login URL
        index = res.text.index("WindowsLiveId") # Find URL
        cutText = res.text[index + 16:] # Cut Text at Start of URL
        loginURL = cutText[:cutText.index("\"")] # Cut at End of URL
        loginURL = bytes(loginURL, encoding="UTF-8").decode("unicode_escape") # Unescape URL
        # Get Login Cookies
        self.headers["Host"] = c.loginHost # Set Host to Login Server
        res = self.get(loginURL)
        self.cookies = res.cookies # Set Cookies
        self.cookies["CkTst"] = "G" + str(int(time.time() * 1000)) # Add Time Cookie
        # Get Post URL
        index = res.text.index(c.loginPostURL) # Find URL
        cutText = res.text[index:] # Cut Text at Start of URL
        postURL = cutText[:cutText.index("\'")] # Cut at End of URL
        # Get PPFT
        index = res.text.index("sFTTag") # Find PPFT
        cutText = res.text[index:] # Cut Text Near PPFT
        PPFT = cutText[cutText.index("value=") + 7:cutText.index("\"/>")] # Cut PPFT
        self.data["PPFT"] = PPFT
        # Get PPSX
        index = res.text.index(",r:\'") # Find PPSX
        cutText = res.text[index + 4:] # Cut Text at Start of PPSX
        PPSX = cutText[:cutText.index("\'")] # Cut at End of PPSX
        self.data["PPSX"] = PPSX
        # Finish Up
        self.cookies["wlidperf"] = "FR=L&ST=" + str(int(time.time() * 1000)) # Add Another Time Cookie
        return postURL
    
    def logout(self):
        pass
    
    def get(self, URL, params=None, cookies=None, data=None, proxy=False):
        if(proxy):
            res = requests.get(URL, headers=self.headers, params=params, cookies=cookies, data=data, proxies=self.proxies, verify=False)
        else:
            res = requests.get(URL, headers=self.headers, params=params, cookies=cookies, data=data)
        self.headers["Referer"] = URL
        return res
    
    def post(self, URL, params=None, cookies=None, data=None, proxy=False):
        if(proxy):
            res = requests.post(URL, headers=self.headers, params=params, cookies=cookies, data=data, proxies=self.proxies, verify=False)
        else:
            res = requests.post(URL, headers=self.headers, params=params, cookies=cookies, data=data)
        self.headers["Referer"] = URL
        return res
        
    def CookieLogin(self):
        # Get Login URL
        res = self.get(c.hostURL)
        index = res.text.index("WindowsLiveId")  # Find URL
        cutText = res.text[index + 16:]          # Cut Text at Start of URL
        loginURL = cutText[:cutText.index("\"")] # Cut at End of URL
        loginURL = bytes(loginURL, encoding="UTF-8").decode("unicode_escape") # Unescape URL
        
        # Get Login Cookies
        self.headers["Host"] = c.loginHost            # Set Host to Login Server
        res = self.get(loginURL, cookies=[])
        self.cookies = res.cookies                    # Set Cookies
        self.cookies.set_cookie(self.getAuthCookie()) #Set Login Cookie

        # Get Login Page
        res = self.get(loginURL, cookies=self.cookies)
        self.cookies = res.cookies

        # Get form and post it
        form = BeautifulSoup(res.text, "html.parser").findAll("form")[0]
        params = dict()
        for field in form:
            params[field["name"]] = field["value"] # Add each field to params
        self.headers["Host"] = c.host              # Set Host to Bing Server
        res = self.post(form.get("action"), cookies=self.cookies, data=params)

        # Set retrieved cookies
        self.cookies = res.cookies

    def getAuthCookie(self):
        return Cookie(
                version=0, 
                name="PPAuth", 
                value=self.data["passwd"],
                port=None, 
                port_specified=False,
                domain=".login.live.com", 
                domain_specified=True, 
                domain_initial_dot=False,
                path="/", 
                path_specified=True,
                secure=False,
                expires=None,
                discard=False,
                comment=None,
                comment_url=None,
                rest=None
            )