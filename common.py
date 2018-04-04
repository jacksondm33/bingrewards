
host = "www.bing.com"
hostURL = "https://www.bing.com/"
searchURL = "https://www.bing.com/search?q="
loginHost = "login.live.com"
loginPostURL = "https://login.live.com/ppsecure/post.srf"
ua = "Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"
mobile_ua = "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; NOKIA; Lumia 822) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
acceptLang = "en-US,en;q=0.5"
connection = "close"
headers = {"Host": host, "User-Agent": ua, "Accept": accept,
           "Accept-Language": acceptLang, "Connection": connection}
mobileHeaders = {"Host": host, "User-Agent": mobile_ua, "Accept": accept,
                 "Accept-Language": acceptLang, "Connection": connection}
proxies = {"http": "127.0.0.1:8080", "https": "127.0.0.1:8080"}
