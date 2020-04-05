#coding=utf-8
#code by wzh
import os

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


#目标网站

nameList = ['fangqiyan', 'guxinyi', 'mengqiqi', 'gezheng']
urlList = ['https://www.yeitu.com/meinv/xinggan/20180603_14236.html','https://www.yeitu.com/meinv/xinggan/20150708_10017.html',
           'https://www.yeitu.com/meinv/xinggan/20170301_11675.html', 'https://www.xgmn.org/HuaYang/HuaYang12935.html']

webFlag =[0, 0, 0, 1]

def download(url, dirName, webTag):
    if (webTag == 0):
        return
    nextUrl = url
    cur = 0
    while (True):
        # 获取网站源码
        htmlContent = requests.get(nextUrl)
        # 防止中文乱码
        htmlContent.encoding = 'utf-8'
        # print(htmlContent.text)

        # 网站内容解析器
        soup = BeautifulSoup(htmlContent.text, "lxml")
        soup.prettify()
        # 递归查找标签
        print(soup.find_all('img', recursive=True))

        # 提取img标签中src地址
        targetUrl = soup.find_all("img", recursive=True)
        for item in targetUrl:
            cur = cur + 1
            dir = "./downloadImg/" + dirName
            if (not os.path.exists(dir)):
                os.makedirs(dir)

            path = dir + "/" + str(cur) + ".jpg"
            if (os.path.exists(path)):
                break

            # 下载文件
            curUrl = item["src"]
            if (webTag == 1):
                curUrl = "https://www.xgmn.org" + curUrl

            print(curUrl)
            ua = UserAgent()
            headers = {'User-Agent': ua.random, 'Referer': 'https://www.xgmn.org/'}
            r = requests.get(curUrl, headers=headers)
            if (len(r.content) < 540 * 960):
                continue

            with open(path, "wb") as f:
                f.write(r.content)



        if (webTag == 1):
            index = nextUrl.find("_")
            if (index == -1):
                index = nextUrl.replace(".html", "_1.html")
            else:
                num = nextUrl[index + 1 : len(nextUrl) - 5]
                num = num + 1
                nextUrl = nextUrl[0 : index + 1] + str(num) + ".html"


        flag = False
        for item in soup.find_all("div", class_="img_box"):
            print(item.a)
            if (item.a is None):
                flag = True
                break
            nextUrl = item.a["href"]
            break

        if (nextUrl is None or flag):
            break

for i in range(len(urlList)):
    download(urlList[i], nameList[i], webFlag[i])