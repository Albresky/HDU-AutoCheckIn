#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Author  : Loot at the stars
# @Time    : 2022/3/10 16:44
# @File    : demo.py
# @Software: PyCharm

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import js2py
import hashlib
import time
import base64
import logging


class CheckIn:
    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.userName = ''
        self.userID = ''
        self.userPWD = ''
        self.provice = '330000'
        self.city = '330100'
        self.country = '330101'
        self.MySha1 = ''
        self.btoa_1 = ''
        self.cookies = None
        self.timestamp = ''
        self.lt = None
        self.rsa = ''
        self.sign = ''
        self.cas2sso = ''
        self.ssoUrl = ''
        self.casUrl = ''
        self.etag=''
        self.lastMod=''
        self.AuthToken = ''
        self.MySession = requests.session()

        self.check_url = "https://healthcheckin.hduhelp.com/"
        self.login_url = "https://api.hduhelp.com/login/direct/cas?clientID=healthcheckin&redirect=https%3A%2F%2Fhealthcheckin.hduhelp.com%2F%23%2Fauth"
        self.checkin_url = ''

        self.wechatHeaders = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://cas.hdu.edu.cn/",
            "Authorization": "",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; IN2020 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1209 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
        }

        self.headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://healthcheckin.hduhelp.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }
        self.headers2 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "cas.hdu.edu.cn",
            "Referer": "https://healthcheckin.hduhelp.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }

        self.headers3 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "350",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "cas.hdu.edu.cn",
            "Origin": "https://cas.hdu.edu.cn",
            "Referer": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Cookie": ""
        }

        self.headers4 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Referer": "https://cas.hdu.edu.cn/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; IN2020 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1209 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        }

        self.headersOptions = {

        }

    def getLT(self, casResponse):
        soup = BeautifulSoup(casResponse.text, features='lxml')
        try:
            scriptPart = soup.find("script", id="password_template").get_text()
            if scriptPart is not None:
                print("Find Script OK!")
                realSoup = BeautifulSoup(scriptPart, "lxml")
                try:
                    self.lt = realSoup.find("input", attrs={"type": "hidden", "id": "lt"})['value']
                    if self.lt is not None:
                        print("Find LT OK!")
                        print("LT:  {}".format(self.lt))
                except AttributeError as e:
                    logging.error("Find LT Fail! => {}".format(e))
                    raise e
        except AttributeError as e:
            logging.error("bs4 Find Script Fail! => {}".format(e))
            raise e

    def cacuRsa(self):
        try:
            with open('des.js', 'r', encoding='UTF-8') as f:
                js_code = f.read()
        except FileNotFoundError as e:
            logging.error("des.js not found")
            raise e
        jsFunction = js2py.EvalJs()
        jsFunction.execute(js_code)
        value = self.userID + self.userPWD + self.lt
        self.rsa = jsFunction.strEnc(value, '1', '2', '3')
        print("Compute rsa OK!")
        print("rsa:  {}".format(self.rsa))

    def getSign(self):
        btoa_1 = str(base64.b64encode(self.userID.encode('utf-8')), "utf-8")
        btoa_2 = str(base64.b64encode(self.provice.encode('utf-8')), "utf-8")
        self.timestamp = str(int(time.time() / 1e3))
        value = self.userName + btoa_1 + self.timestamp + btoa_2 + self.city + self.country
        sha = hashlib.sha1(value.encode('utf-8'))
        encrypts = sha.hexdigest()
        return encrypts

    def login(self, userid, userpwd):
        self.userID = userid
        self.userPWD = userpwd
        self.MySession.cookies.clear()
        self.MySession.verify = False

        # 打开打卡网页
        self.MySession.headers = self.headers1

        response0=self.MySession.get(url=self.check_url,headers=self.headers1,allow_redirects=False)
        try:
            print("response0.status_code: {}".format(response0.status_code))
            if response0.status_code == 200:
                self.etag=response0.headers["etag"]
                self.lastMod=response0.headers["last-modified"]
                print("etag=> {}".format(self.etag))
                print("lastMod=> {}".format(self.lastMod))
            else:
                print("First ERROR!")
        except:
            raise

        response1 = self.MySession.get(url=self.login_url, headers=self.headers1, allow_redirects=False)
        try:
            print("response1.status_code: {}".format(response1.status_code))
            if response1.status_code == 302:
                self.casUrl = response1.headers['location']
                print("获取CAS认证界面URL成功！=>{}".format(self.casUrl))
            else:
                print("获取CAS认证界面URL失败！")
        except:
            raise

        # 跳转CAS认证界面
        response2 = self.MySession.get(url=self.casUrl, headers=self.headers2, allow_redirects=False)
        try:
            print("response2.status_code: {}".format(response2.status_code))
            if response2.status_code == 200:
                print(response2.cookies)
                self.cookies = "JSESSIONID={}; Language={}".format(
                    response2.cookies["JSESSIONID"], response2.cookies["Language"])
                print("self.cookie:{}".format(self.cookies))
                print("self.MySession's Cookie:{}".format(self.MySession.cookies))
                print("跳转CAS认证界面成功!")
            else:
                logging.warning("跳转CAS认证界面失败!")
        except:
            raise

        # 获取页面零时凭证LT
        self.getLT(response2)
        # 计算登录表单中的Rsa
        self.cacuRsa()

        ul = len(self.userID)
        pl = len(self.userPWD)

        # Cas界面Post表单数据
        formData = {
            'rsa': self.rsa,
            'ul': ul,
            'pl': pl,
            'lt': self.lt,
            'execution': 'e1s1',
            '_eventId': 'submit'
        }
        print(formData)

        self.headers3["Referer"] = self.casUrl
        self.headers3["Cookie"] = self.cookies
        print("headers3.Referer: {}".format(self.headers3["Referer"]))
        print("headers3.Cookie: {}".format(self.headers3["Cookie"]))
        response3 = self.MySession.post(url=self.casUrl, headers=self.headers3, data=formData, allow_redirects=False)
        try:
            print("response3.status_code: {}".format(response3.status_code))
            if response3.status_code == 302:
                print("CAS Cartify OK!")
                self.cookies = response3.headers['Set-Cookie']
                self.ssoUrl = response3.headers['Location']
                print("self.ssoUrl: {}".format(self.ssoUrl))
                print("self.cookies: {}".format(self.cookies))
                print("MySession's cookies: {}".format(self.MySession.cookies))
        except requests.exceptions.ConnectionError as e:
            logging.error("跳转sso失败！")
            raise e

        # 跳转sso
        response4 = self.MySession.get(url=self.ssoUrl, headers=self.headers4, allow_redirects=False)
        try:
            print("response4.status_code: {}".format(response4.status_code))
            print("MySession's cookies: {}".format(self.MySession.cookies))
            if response4.status_code == 302:
                print("跳转sso成功！")
                self.checkin_url = response4.headers['location']
                self.AuthToken = "token "+ self.checkin_url.split('?')[1].split('=')[1]
                self.wechatHeaders["Authorization"] = self.AuthToken
                print("response4.HeaderLocation: {}".format(self.checkin_url))
                print("validate token: {}".format(self.AuthToken))
        except requests.exceptions.ConnectionError as e:
            logging.error("跳转sso失败！")
            raise e


        # 跳转至打卡网页
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; IN2020 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1209 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://cas.hdu.edu.cn/",
            "if-modified-since": self.lastMod,
            "if-none-match": self.etag
        }

        response5 = self.MySession.get(url=self.check_url, headers=headers)
        try:
            print("response5.status_code: {}".format(response5.status_code))
            if response5.status_code == 304 and \
                response5.headers["etag"]==self.etag:
                print("CheckIn Pre OK!!!")
        except:
            raise ConnectionError("CheckIn Pre Fail!!!")


    def submit(self):
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; IN2020 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1209 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Referer": "https://healthcheckin.hduhelp.com",
            "Origin": "https://healthcheckin.hduhelp.com/",
            "Authorization": self.AuthToken,
            "Content-Length": "734",
            "Content-Type": "application/json;charset=UTF-8"
        }
        check_data = {
            "name": "石开",
            "timestamp": self.timestamp,
            "province": "330000",
            "city": "330100",
            "country": "330101",
            "answerJsonStr": "{\"ques1\":\"健康良好\",\"ques2\":\"正常在校（未经学校审批，不得提前返校）\",\"ques3\":null,\"ques4\":\"否\",\"ques5\":\"否\",\"ques6\":\"\",\"ques7\":null,\"ques77\":null,\"ques8\":null,\"ques88\":null,\"ques9\":null,\"ques10\":null,\"ques11\":null,\"ques12\":null,\"ques13\":null,\"ques14\":null,\"ques15\":\"否\",\"ques16\":\"否\",\"ques17\":\"无新冠肺炎确诊或疑似\",\"ques18\":\"37度以下\",\"ques19\":null,\"ques20\":\"绿码\",\"ques21\":\"否\",\"ques22\":\"否\",\"ques23\":\"否\",\"ques24\":\"共三针 - 已完成第三针\",\"carTo\":[\"330000\",\"330100\",\"330101\"]}"
        }
        data = json.dumps(check_data)
        result = self.MySession.post(url=self.check_url + 'base/healthcheckin?sign=' + self.getSign(),
                                     headers=headers,
                                     data=data)
        try:
            print("result.status_code: {}".format(result.status_code))
            print(result.text)
            if result.status_code == 200:
                print("打卡成功")
        except:
            raise

    def getDaily(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; IN2020 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1209 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Referer": "https://healthcheckin.hduhelp.com",
            "Origin": "https://healthcheckin.hduhelp.com/",
            "Authorization": self.AuthToken
        }
        respond = self.MySession.get(url="https://api.hduhelp.com/base/healthcheckin/info/daily", headers=headers)
        if respond.status_code==200:
            return respond.text


if __name__ == '__main__':
    _login = CheckIn()
    _login.login('20041423', 'shikaiHDU7')
    print(_login.getDaily())
