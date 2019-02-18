# _*_ coding:UTF-8 _*_
import requests
from lxml import etree
from re import search
#from io import TextIOWrapper
#from sys import stdout
import json
import execjs
import urllib.parse
import threading
import queue
import random
#stdout = TextIOWrapper(stdout.buffer,encoding='utf8')
list = [('review_title','title_translate','review_body','body_translate')]
page_urls = []
t_crawl_list = []
t_parse_list = []
user_agent_list = [
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
  'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]
headers = {
    'user-agent': random.choice(user_agent_list)
}
page = 1
class Py4Js():
    def __init__(self,e):
        self.e = e
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    };      
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)
    def getTk(self,text):
        return self.ctx.call("TL",text)
    def buildUrl(self,text,tk):
        text = urllib.parse.quote(text)
        # print(text)
        baseUrl = "http://translate.google.cn/translate_a/single?client=t&sl=auto&tl=%s&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s"%(self.e,tk,text)
        return baseUrl
    def translate(self,text):
        headers={
            'authority':'translate.google.cn',
            'method':'GET',
            'path':'',
            'scheme':'https',
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'cookie':'',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36','x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE=',
        }
        url=self.buildUrl(text,self.getTk(text))
        res=''
        try:
            r=requests.get(url,headers=headers)
            result=json.loads(r.text)
            # if result[7] != None:
            #     try:
            #       correctText=result[7][0].replace('<b><i>',' ').replace('</i></b>','')
            #       correctUrl=self.buildUrl(correctText,self.getTk(correctText))
            #       correctR=requests.get(correctUrl)
            #       newResult=json.loads(correctR.text)
            #       res=newResult[0][0][0]
            #     except Exception as e:
            #         res=result[0][0][0]
            # else:
            #print(result)
            if len(result[0]) > 1:
                for i in range(len(result[0])):
                    if result[0][i][0]:
                        res += result[0][i][0]
            else:
                res=result[0][0][0]
            # print(result)
        except Exception as e:
            res=''
            #print(url)
            # print("翻译"+text+"失败")
            # print("错误信息:")
            # print(e)
        finally:
            return res

class CrawlThread(threading.Thread):
    def __init__(self,page,name,headers,pages_queue,pages_url_queue, data_queue):
        super().__init__()
        self.name = name
        self.page = page
        self.headers = headers
        self.pages_queue = pages_queue
        self.pages_url_queue = pages_url_queue
        self.data_queue = data_queue
    def run(self):
        print('%s----启动' % (self.name))
        while 1:
            global page
            if not self.pages_queue.empty():
                page = self.pages_queue.get()
                print('%s正在爬取第%s页。。。'%(self.name,page))
                page_url = self.pages_url_queue.get()
                response = requests.get(page_url, headers=headers)
                self.data_queue.put((page,response))
                self.pages_queue.task_done()


class ParseThread(threading.Thread):
    def __init__(self,f,h,js,name,pages_queue,pages_url_queue, data_queue):
        super().__init__()
        self.f = f
        self.h = h
        self.js = js
        self.name = name
        self.pages_queue = pages_queue
        self.pages_url_queue = pages_url_queue
        self.data_queue = data_queue
    def run(self):
        print('%s----启动' % (self.name))
        while 1:
            page,data = self.data_queue.get()
            print('正在解析第%s页' %page)
            response = self.etree_html(data)
            page_url_2 = self.page_0(self.h, response)
            if page_url_2:
                self.pages_url_queue.put(page_url_2)
            list = self.parse(self.js, response)
            print('第%s页解析完成。。。' % page)
            self.data_queue.task_done()
            for i in range(len(list)):
                for j in range(4):
                    x = list[i][j]
                    x = x.replace(',', '，')
                    self.f.write(x)
                    if j < 3:
                        self.f.write(',')
                self.f.write('\n')
            # list = []

    def etree_html(self,response):
        response = etree.HTML(response.text)
        return response

    def page_0(self,l, response):
        page_url_3 = response.xpath('//li[@class="a-last"]/a/@href')
        if page_url_3:
            page_url = l + page_url_3[0]
        else:
            page_url = ''
        return page_url

    def parse(self,js, response):
        reviews = response.xpath('//div[@id="cm_cr-review_list"]/div[@data-hook="review"]')
        list = []
        for review in reviews:
            rate = review.xpath('.//span[@class="a-icon-alt"]/text()')[0]
            rate = search('(\d+[.,]\d)', rate).group(0)
            if rate == '5.0' or rate == '5,0':
                title = review.xpath('.//a[@data-hook="review-title"]/text()')
                if title:
                    review_title = title[0]
                    review_title = review_title.lstrip().rstrip().replace('\n', '')
                    title_traslate = js.translate(review_title)
                    title_traslate = title_traslate.lstrip().rstrip().replace('\n', '')
                    # print(title_traslate)
                else:
                    review_title = ''
                    title_traslate = ''
                body = review.xpath('.//span[@data-hook="review-body"]/text()')
                if body:
                    review_body = body[0]
                    review_body = review_body.lstrip().rstrip().replace('\n', '')
                    body_traslate = js.translate(review_body)
                    body_traslate = body_traslate.lstrip().rstrip().replace('\n', '')
                    # print(body_traslate)
                else:
                    review_body = ''
                    body_traslate = ''
                k = review_title, title_traslate, review_body, body_traslate
                if k not in list:
                    list.append(k)
        return list

def test_url():
    while 1:
        url = input('请输入reviews地址：')
        # url= 'https://www.amazon.de/OMOTON-Panzerglas-Schutzfolie-Bedeckung-Bl%C3%A4schenfrei-schwarz/dp/B07C6CB8YC/ref=cm_cr_arp_d_product_top?ie=UTF8'
        l = search('(.*?//.*?/)',url).group(0)
        try:
            asin = search('(B0.*?)/',url).group(0)
            print('此商品asin：%s'%asin)
            print('请选择要翻译成的语言: 1.英文  2.中文')
            while True:
                o = input('请输入对应序号（1或2）：')
                if o == '1':
                    print('你选择翻译为英文。。。')
                    o = 'en'
                    break
                if o == '2':
                    print('你选择翻译为中文。。。')
                    o = 'zh-CN'
                    break
                else:
                    print('输入有误，请重新输入。。。')
                    continue
            print('请稍等。。。')
            url_1 = l + 'gp/customer-reviews/widgets/average-customer-review/popover/ref=dpx_acr_pop_?contextId=dpx&asin=' + asin
        except Exception as e:
            print('检索不到该产品asin，请重新输入')
            continue
        response = requests.get(url_1,headers=headers).text
        response = etree.HTML(response)
        url_2 = response.xpath("//a[@class='a-size-small a-link-emphasis']/@href")
        p = response.xpath("//a[@class='a-size-small a-link-emphasis']/text()")[0]
        num = search('(\d+[,.]*\d+)', p).group(0)
        if ',' in num or '.' in num:
            num = num.replace(',','').replace('.','')
        # if search('(\d+)', p).group(1):
        #     num2 = search('(\d+)', p).group(1)
        #     print(num2)
        #     num = num + num2
        if not isinstance(num,int):
            j = int(int(num) / 10) + 1
        if url_2:
            url_3 = url_2[0]
            break
        else:
            print('该产品没有reviews或地址有误，请重新输入')
            continue
    return o,url_3,headers,l,j

def create_crawl_thread(page,headers,pages_queue,pages_url_queue,data_queue):
    crawl_name = ['采集线程一号']
    for name in crawl_name:
        tcrawl = CrawlThread(page,name,headers,pages_queue,pages_url_queue, data_queue)
        tcrawl.setDaemon(True)
        t_crawl_list.append(tcrawl)

def create_parse_thread(f,l,js,pages_queue,pages_url_queue,data_queue):
    parse_name = ['解析线程一号']
    for name in parse_name:
        tparse = ParseThread(f,l,js,name,pages_queue,pages_url_queue,data_queue)
        t_parse_list.append(tparse)


def main():
    pages_queue = queue.Queue()
    pages_url_queue = queue.Queue()
    data_queue = queue.Queue()
    o, url_3, headers,l,num = test_url()
    js = Py4Js(o)
    pages_url_queue.put(url_3)
    page_urls.append(url_3)
    response = requests.get(page_urls[0],headers=headers)
    response = etree.HTML(response.text)
    # num = response.xpath('//li[@class="page-button"][last()]/a/text()')[0]
    print('此商品最多有%s页评论'%num)
    m = int(input('请输入要获取的页码数：'))
    filename = input('请输入要保存的文件名：')
    print('请稍候。。。')
    filename = filename + '.csv'
    f = open(filename,'a',encoding='utf8')
    for i in range(len(list)):
        for j in range(4):
            x = list[i][j]
            x = x.replace(',', '，')
            f.write(x)
            if j < 3:
                f.write(',')
        f.write('\n')
    if m >= int(num):
        m = int(num)
    else:
        m = m
    for i in range(1,m+1):
        pages_queue.put(i)
    create_crawl_thread(page,headers,pages_queue,pages_url_queue,data_queue)
    create_parse_thread(f,l,js,pages_queue,pages_url_queue,data_queue)
    for tcrawl in t_crawl_list:
        tcrawl.start()

    for tparse in t_parse_list:
        tparse.start()
    # for tparse in t_parse_list:
    #     tparse.join()
    pages_queue.join()
    # print('tyryrtyrt')
    data_queue.join()
    print('主线程和子线程全部完成。。。')
    # for page_url in page_urls:
    #     if page_url:
    #         if n <= m:
    #             print('正在解析第%s页，请稍等。。。'%n)
    #             response = requests.get(page_url,headers=headers)
    #             response = etree_html(response)
    #             page_url_2 = page(l,response)
    #             if page_url_2:
    #                 page_urls.append(page_url_2)
    #             list = parse(js,response)
    #             print('第%s页解析完成。。。'%n)
    #             n += 1
    #         else:
    #             break
    #     else:
    #         print('已超出此产品评论最大页数。。。')
    # filename = input('请输入要保存的文件名：')
    # filename = filename + '.csv'
    # f = open(filename,'a',encoding='utf8')
    # for i in range(len(list)):
    #     for j in range(4):
    #         x = list[i][j]
    #
    #         x = x.replace(',','，')
    #         f.write(x)
    #         if j < 3:
    #             f.write(',')
    #     f.write('\n')
    f.close()
    print('写入完成。。。')

if __name__ == '__main__':
    main()
