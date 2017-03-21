# -*- coding:utf-8 -*-

import os
import random
import urllib
import re
import threading

girl_urls = []
img_urls = []
threads = []

def getHtml(url, page=None):
    if not page:
        htmlurl = url
    else:
        htmlurl = url + page
    html = urllib.urlopen(htmlurl).read().decode('gb2312').encode('utf-8')
    reg = r'<LI class=picimg><A href="(.*?)" title="(.*?)" target=_blank><img'
    urlreg = re.compile(reg)
    urls = re.findall(urlreg, html)
    for a in urls:
        girl_urls.append(a)
    netpage = re.findall(re.compile(r'<li><a href=\'(.*?)\'>下一页</a></li>'), html)
    if netpage:
        getHtml(url, netpage[0])
    else:
        getGirlInfo()

def getGirlInfo():
    for url in girl_urls:
        th = threading.Thread(target=getGirlInfoUrls, args=('http://www.hmrenti.net' + url[0], url[1]))
        threads.append(th)

    for t in threads:
        t.start()
        while True:
            if len(threading.enumerate()) < 10:
                break

def getGirlInfoUrls(url, title):
    title = re.findall(re.compile(r'\s(.*?)无圣光'), title)
    html = urllib.urlopen(url).read().decode('gb2312').encode('utf-8')
    allpage = re.findall(re.compile(r'<span class="page-ch">共(.*?)页</span>'), html)
    allnums = int(allpage[0]) + 1
    getGirlImg(url, title[0])
    for i in range(2, allnums):
        getGirlImg(url[:-5] + '_' + str(i) + '.html', title[0])

def getGirlImg(url, title):
    html = urllib.urlopen(url).read().decode('gb2312').encode('utf-8')
    reg = r'<img src=\'(.*?)\' alt=\'(.*?)\' title="(.*?)" id=\'bigimg\' />'
    imgreg = re.compile(reg)
    imgurl = re.findall(imgreg, html)
    path = 'tuigirl_pic/' + title.decode('utf-8').encode('gbk').replace('/', '+')
    if not os.path.exists(path):
        os.makedirs(path)

    print '正在下载【' + title + '】的图片' + imgurl[0][0] + ',请耐心等待。。。'
    urllib.urlretrieve(imgurl[0][0], path + '/' + str(random.randint(1000000000, 9999999999)) + '.jpg')


if __name__ == '__main__':
    getHtml('http://www.hmrenti.net/tuigirl/')
