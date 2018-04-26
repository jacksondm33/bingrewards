import requests
import common as c
import time
from bs4 import BeautifulSoup
from random import randint
from http.cookies import SimpleCookie
from requests.cookies import RequestsCookieJar


USE_SELF = object()


class Account:

    headers = c.headers
    data = None
    proxies = c.proxies

    def __init__(self, email, password=None, cookie=None):
        self.email = email
        self.cookies = RequestsCookieJar()
        if password is None:
            temp_cookie = SimpleCookie()
            temp_cookie.load(cookie)
            for key, morsel in temp_cookie.items():
                self.cookies[key] = morsel.value
            self.cookie = True
        else:
            self.password = password
            self.cookie = False

    def login(self, mobile=False, useProxy=False):
        self.headers = c.headers
        if not self.cookie:
            postURL = self.preLogin(useProxy=useProxy)
            res = self.post(postURL, data=self.data, useProxy=useProxy)
            # Parse HTML Form
            form = BeautifulSoup(res.text, "html.parser").findAll("form")[
                0]  # Get Form
            params = dict()
            for field in form:
                # Add each field to params
                params[field["name"]] = field["value"]
            self.headers["Host"] = c.host  # Set Host to Bing Server
            self.cookies.clear()
            res = self.post(form.get("action"), data=params, useProxy=useProxy)
        if mobile:
            self.headers = c.mobileHeaders

    def preLogin(self, useProxy=False):
        res = self.get(c.hostURL, useProxy=useProxy)
        # Get Login URL
        index = res.text.index("WindowsLiveId")  # Find URL
        cutText = res.text[index + 16:]  # Cut Text at Start of URL
        loginURL = cutText[:cutText.index("\"")]  # Cut at End of URL
        # Unescape URL
        loginURL = bytes(loginURL, encoding="UTF-8").decode("unicode_escape")
        # Get Login Cookies
        self.headers["Host"] = c.loginHost  # Set Host to Login Server
        res = self.get(loginURL, useProxy=useProxy)
        self.data = self.getAuthData()
        self.cookies["CkTst"] = "G" + \
            str(int(time.time() * 1000))  # Add Time Cookie
        # Get Post URL
        index = res.text.index(c.loginPostURL)  # Find URL
        cutText = res.text[index:]  # Cut Text at Start of URL
        postURL = cutText[:cutText.index("\'")]  # Cut at End of URL
        # Get PPFT
        index = res.text.index("sFTTag")  # Find PPFT
        cutText = res.text[index:]  # Cut Text Near PPFT
        PPFT = cutText[cutText.index(
            "value=") + 7:cutText.index("\"/>")]  # Cut PPFT
        self.data["PPFT"] = PPFT
        # Get PPSX
        index = res.text.index(",bH:\'")  # Find PPSX
        cutText = res.text[index + 4:]  # Cut Text at Start of PPSX
        PPSX = cutText[:cutText.index("\'")]  # Cut at End of PPSX
        self.data["PPSX"] = PPSX
        # Finish Up
        self.cookies["wlidperf"] = "FR=L&ST=" + \
            str(int(time.time() * 1000))  # Add Another Time Cookie
        return postURL

    def logout(self):
        if not self.cookie:
            self.cookies.clear()

    def getAuthData(self):
        return {
            "login": self.email,
            "loginfmt": self.email,
            "passwd": self.password,
            "i13": "0",
            "type": "11",
            "LoginOptions": "3",
            "lrt": "",
            "ps": "2",
            "psRNGCDefaultType": "",
            "psRNGCEntropy": "",
            "psRNGCSLK": "",
            "canary": "",
            "ctx": "",
            "NewUser": "1",
            "FoundMSAs": "",
            "fspost": "0",
            "i21": "0",
            "i2": "1",
            "i17": "0",
            "i18": "__ConvergedLoginPaginatedStrings%7C1%2C__ConvergedLogin_PCore%7C1%2C",
            "i19": "2" + str(randint(0, 5000))
        }

    def request(self, method, URL, headers=USE_SELF, cookies=USE_SELF, params=None, data=None, proxies=USE_SELF, useProxy=False, setReferer=True, setCookies=True):
        headers = self.headers if headers is USE_SELF else headers
        cookies = self.cookies if cookies is USE_SELF else cookies
        proxies = self.proxies if proxies is USE_SELF else proxies
        res = requests.request(method, URL, headers=headers, cookies=cookies,
                               params=params, data=data, proxies=proxies if useProxy else None)
        if setReferer:
            self.headers["Referer"] = URL
        if setCookies:
            self.cookies.update(res.cookies)
        return res

    def get(self, URL, headers=USE_SELF, cookies=USE_SELF, params=None, data=None, proxies=USE_SELF, useProxy=False, setReferer=True, setCookies=True):
        return self.request('GET', URL, headers, cookies, params, data, proxies, useProxy, setReferer, setCookies)

    def post(self, URL, headers=USE_SELF, cookies=USE_SELF, params=None, data=None, proxies=USE_SELF, useProxy=False, setReferer=True, setCookies=True):
        return self.request('POST', URL, headers, cookies, params, data, proxies, useProxy, setReferer, setCookies)
