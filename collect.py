#coding=utf-8
#author:sml2h3
#created:2016.12.20
#email:sml2h3@gmail.com
import requests
import threadpool
from lxml import etree
from urlparse import *
import sys


def getu(url):
    arr = []
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    try:
        requ = requests.get(url, verify=False, timeout=3, headers = headers )
    except requests.RequestException:
        return []
    try:
        page = requ.text
    except requests.RequestException as e:
        return []
    ss = etree.HTML(page)
    urls = ss.xpath("//*[@href]/@href")
    for i in urls:
        r = urlparse(i)
        domain = r.netloc
        domain = domain.replace(" ", '')
        if domain != '':
            if r.scheme == "http" or r.scheme == "https" or r.scheme == "ftp":
                u = r.scheme + "://" + r.netloc
            else:
                u = "http://" + r.netloc
        else:
            continue

        if u in urlArr:
            continue
        else:
            urlArr.append(u)
            arr.append(u)
    return arr


def con(request, result):
    global allget
    for i in result:
        allget = allget + 1
        f.write(i+'\n')
        print "当前已爬取"+str(allget)+"个Url:"+i
    re = threadpool.makeRequests(getu, result, con)
    [pool.putRequest(req) for req in re]


reload(sys)
sys.setdefaultencoding('utf8')
f2 = file('error_file.txt', 'w')
sys.stderr = f2
urlArr = []
allget = 0
f = file("url.txt", "a+")
data = getu("http://www.tjpu.edu.cn")
pool = threadpool.ThreadPool(20)
reqrest = threadpool.makeRequests(getu, data, con)
[pool.putRequest(req) for req in reqrest]
pool.wait()
f.close()