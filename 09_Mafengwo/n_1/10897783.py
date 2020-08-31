__author__ = '15275'
from bloom_filter import BloomFilter
import re
import urllib.request
import lxml.etree as etree
import queue
import os
import threading
import time

note_url_queue = queue.Queue()
download_bf = BloomFilter(1024 * 1024 * 16, 0.01)
# 因为需要对URL队列进行操作  所以对队列的操作，需要先获取这把锁
con_note_url_queue=threading.Condition();
# 写文件也需要锁
con_write_hdfs=threading.Condition();
TIME_OUT = 2

request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
}

#抓取城市名字城市id元组形式存储，存到一个list里
city = []
def get_city():
    url='http://www.mafengwo.cn/mdd/'
    request=urllib.request.Request(url,headers=request_headers);
    try:
      reponse=urllib.request.urlopen(request)
    except Exception:
        print("error,response失败")
    content=reponse.read().decode('utf-8');
    cityurl=re.findall('href="/travel-scenic-spot/mafengwo/\d{5}.html"',content)
    cityid=[x[-11:-6] for x in cityurl];
    citynameall=re.findall('href="/travel-scenic-spot/mafengwo/\d{5}.html" target="_blank">\S*<',content)
    citynameiter=iter(citynameall);
    cityname=[];
    while True:
        try:
            cityname.append(next(citynameiter)[63:-1]);
        except Exception:
            break;
    city=zip(cityid,cityname)
    return city;


# 根据城市id爬取   每个城市爬十页最热游记 的url放入队列   记住  队列全是二元组（完整的URL路径 ，游记title）
def put_citynoteurl_inqueue():
    # city = get_city()
    # for tu in city:
    #     for pagenumber in range(1):
    #         url = 'http://www.mafengwo.cn/yj/%s/1-0-%d.html' % (tu[0],pagenumber)
    #         request = urllib.request.Request(url, headers=request_headers);
    #         try:
    #             response = urllib.request.urlopen(request)
    #         except Exception:
    #            print("error,response失败")
    #            return
    #         content = response.read().decode('utf8');
    #         tr=etree.HTML(content)
    #         #竟然特么不支持正则  d{9}  cao  cao
    #         notes_url=tr.xpath('//li[@class="post-item clearfix"]/h2//a[contains(@href,"/i/")]/@href');
    #         #文章标题
    #         title_text=tr.xpath('//li[@class="post-item clearfix"]/h2//a[contains(@href,"/i/")]/text()')
    #         notes_url_title=zip(notes_url,title_text);
    #         base_url='http://www.mafengwo.cn/i/'
    base_url = 'http://www.mafengwo.cn'
    link_list = open("youji.txt", 'r')
    for url_and_title in link_list:
        tail_url = url_and_title[0][-12:]
        com_note_url = base_url+tail_url
        url_and_title = (com_note_url, url_and_title[1])
        if com_note_url in download_bf:
            continue
        else:
            download_bf.add(com_note_url)
            con_note_url_queue.acquire()
            # con_note_url_queue.notify_all()
            # con_note_url_queue.wait()
            note_url_queue.put(url_and_title)
            # con_note_url_queue.notify_all()
            con_note_url_queue.release()


# 写文件  titl 跟内容    a是追加写入
def write_title_and_notes(title, note):
    if(os.path.exists('file/citynote.txt')):
        with open('file/citynote.txt', 'a', encoding='utf-8') as citynote:
            print(threading.current_thread().name)
            # con_write_hdfs.notify_all()
            # con_write_hdfs.wait()
            citynote.writelines('<<'+title+'>>')
            for str in note:
                citynote.writelines(str.strip())
            # con_write_hdfs.notify_all()


#得到所有游记  并写入
def get_note_for_queue(note_url_queue):
    while not note_url_queue.empty():
        con_note_url_queue.acquire()
        url_title = note_url_queue.get()
        con_note_url_queue.release()
        url = url_title[0]
        title = url_title[1]
        request = urllib.request.Request(url, headers=request_headers)
        try:
            response = urllib.request.urlopen(request)
        except Exception:
               print("error,response失败")
               return
        content = response.read().decode('utf-8')
        tr = etree.HTML(content)
        notes_content = tr.xpath('//div[contains(@class,"_j_content_box")]//p/text()')
        con_write_hdfs.acquire()
        write_title_and_notes(title, notes_content)
        con_write_hdfs.release()
#get_note_for_queue()


# 创建一个线程池  其中第一个线程 爬取note_url   其余线程根据URL爬取游记
threads = []
threadmain = threading.Thread(target=put_citynoteurl_inqueue)
threads.append(threadmain)
threadmain.setDaemon(True)
threadmain.start()
while True:
    while len(threads) < 10:
        thread = (threading.Thread(target=get_note_for_queue, args=(note_url_queue,)))
        threads.append(thread)
        thread.setDaemon(True)
        thread.start()
    for value in threads:
        if not value.is_alive():
            threads.remove(value)








