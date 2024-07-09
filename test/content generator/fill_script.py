import requests
import urllib.parse
csrf_cookie = urllib.parse.quote("526c56672f112a358db952372d5bc970ea443eb229518e530e096ed0cb502746a:2:{i:0;s:5:\"_csrf\";i:1;s:32:\"39YPS6IgZZnAlj_Ku0ZENgwlHuajcNvG\";}")
csrf_token  = "YFscGwsDyF3y0YdJWjWv7rIyBAdj8apJMfJRI69DdnxTYkVLWDWBOqiL6Qg2X_ClxwJeQi2W3SV5hzBJzA0AOw"
cookies = {"_csrf" : csrf_cookie}
login_data = {
    "_csrf": csrf_token,
    "Login[username]": "yara.sadeghi.81@gmail.com",
    "Login[password]": "12345",
    "Login[rememberMe]": "1"
}
proxy_url = "127.0.0.1:8080"
proxy_dict = {"http": proxy_url, "https": proxy_url}
response = requests.post("http://collabra.yaramsn.lol/user/auth/login",cookies=cookies,data=login_data,proxies=proxy_dict)
cookies["_identity"] = response.cookies["_identity"]

post_data = {
    "_csrf": csrf_token,
    "Post[message]":"A text from my script",
    "containerGuid":"3e7693d6-e5c2-4c13-8133-942cd871a9db",
    "containerClass":"humhub%5Cmodules%5Cspace%5Cmodels%5CSpace",
    "state":"1"
}
response = requests.post("http://collabra.yaramsn.lol/s/movies/post/post/post",cookies=cookies,data=post_data,proxies=proxy_dict)