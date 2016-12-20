#coding=utf-8
#author:sml2h3
#created:2016.12.20
#email:sml2h3@gmail.com
import requests
import threadpool
from lxml import etree
from urlparse import *
import sys
from logger import Logger

logger = Logger('collect.py')


def get_url(url):
    """获取URL"""
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    try:
         page = requests.get(url, verify=False, timeout=3, headers=headers).text

    except requests.RequestException as e:
        logger.error(e)
        return []
    
    try:
        ss = etree.HTML(page)
        urls = ss.xpath("//*[@href]/@href")

    except Exception as e:
        logger.error("dom化失败:{}".format(e))
        return []

    domain_url_list = deal_url(urls)

    return domain_url_list


def deal_url(urls):
    """处理url, 获取domain"""
    res_list = []

    if len(urls) == 0:
        return []

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
            res_list.append(u)

    return res_list


def con(request, result):
    global allget
    for i in result:
        allget = allget + 1
        f.write(i+'\n')
        logger.info("当前已爬取"+str(allget)+"个Url:"+i)
    re = threadpool.makeRequests(get_url, result, con)
    [pool.putRequest(req) for req in re]


if __name__ == '__main__':

    # 测试
    reload(sys)
    sys.setdefaultencoding('utf8')
    f2 = file('error_file.txt', 'w')
    sys.stderr = f2
    urlArr = []
    allget = 0
    f = file("url.txt", "a+")
    data = get_url("http://www.baidu.com")
    pool = threadpool.ThreadPool(20)
    reqrest = threadpool.makeRequests(get_url, data, con)
    [pool.putRequest(req) for req in reqrest]
    pool.wait()
    f.close()
