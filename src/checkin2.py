#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Author  : Loot at the stars
# @Time    : 2022/4/5 11:05
# @File    : checkin2.py
# @Software: PyCharm


import base64
import hashlib
import time

import requests
import json


class checkin2:
    def __init__(self, username, userid, province, city, country):
        self.timestamp = None
        self.userName = username
        self.userID = userid
        self.province = province
        self.city = city
        self.country = country
        self.mysession = requests.session()
        self.mysession.cookies.clear()
        self.headers_options={
            "X-Requested-With": "com.tencent.mm",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
            "Connection": "keep-alive",
            "Host": "api.hduhelp.com",
            "Origin": "https://healthcheckin.hduhelp.com",
            "Referer": "https://healthcheckin.hduhelp.com/",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 3 Build/SP1A.210812.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3195 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/2340 MicroMessenger/8.0.20.2100(0x28001437) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"

        }
        self.headers_post = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": "token 4a795319-97da-4725-a876-df5514ecafa3",
            "Connection": "keep-alive",
            "Content-Length": "734",
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "api.hduhelp.com",
            "Origin": "https://healthcheckin.hduhelp.com",
            "Referer": "https://healthcheckin.hduhelp.com/",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; IN2020 Build/RP1A.201005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/1209 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
        }
        self.url = "https://api.hduhelp.com/base/healthcheckin?sign="

    def getSign(self):
        btoa_a = str(base64.b64encode(self.userID.encode('utf-8')), "utf-8")
        btoa_b = str(base64.b64encode(self.province.encode('utf-8')), "utf-8")
        self.timestamp = int(time.time())
        print(self.timestamp)
        temp_timestamp = str(int(self.timestamp)/1e3)
        # temp_timestamp = "1649234083"
        print(temp_timestamp)
        value = self.userName + btoa_a + temp_timestamp + btoa_b + self.city + self.country
        sha = hashlib.sha1(value.encode('utf-8'))
        encrypts = sha.hexdigest()
        # print(encrypts)
        return encrypts

    def go(self):
        sign = self.getSign()
        # print(sign)
        answerJsonStr = {
            "ques1": "健康良好",
            "ques2": "正常在校（未经学校审批，不得提前返校）",
            "ques3": "null",
            "ques4": "否",
            "ques5": "否",
            "ques6": "",
            "ques7": "null",
            "ques77": "null",
            "ques8": "null",
            "ques88": "null",
            "ques9": "null",
            "ques10": "null",
            "ques11": "null",
            "ques12": "null",
            "ques13": "null",
            "ques14": "null",
            "ques15": "否",
            "ques16": "否",
            "ques17": "无新冠肺炎确诊或疑似",
            "ques18": "37度以下",
            "ques19": "null",
            "ques20": "绿码",
            "ques21": "否",
            "ques22": "否",
            "ques23": "否",
            "ques24": "共三针 - 已完成第三针",
            "carTo": ["330000", "330100", "330101"]
        }
        data = {
            "name": "xxx",
            "timestamp": self.timestamp,
            "province": "330000",
            "city": "330100",
            "country": "330101",
            "answerJsonStr": json.dumps(answerJsonStr)
        }
        print(data)
        cookie = {
            "_ga": "GA1.2.2057824246.1649127648",
            "_gid": "GA1.2.2074480724.1649127648"
        }
        # req_validate=self.mysession.get(url="https://api.hduhelp.com/token/validate",headers=self.headers_post)
        # print(req_validate.text)
        req_option=self.mysession.options(url=self.url,headers=self.headers_options)
        if req_option.status_code==204:
            print("option跨域请求成功！")
            res = self.mysession.post(url=self.url + sign, headers=self.headers_post, data=json.dumps(data))
            print(res.status_code)
            print(res.text)


if __name__ == "__main__":
    mycheck = checkin2('xxx', 'xxx', '330000', '330100', '330101')
    mycheck.go()
