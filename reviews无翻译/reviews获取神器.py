# _*_ coding:UTF-8 _*_
import requests
from lxml import etree
from re import search
from io import TextIOWrapper
from sys import stdout
import urllib.parse
stdout = TextIOWrapper(stdout.buffer,encoding='utf8')
list = [('review_title','title_translate','review_body','body_translate')]
page_urls = []


def etree_html(response):
    response = etree.HTML(response.text)
    return response

def parse(response):
    reviews = response.xpath('//div[@id="cm_cr-review_list"]/div[@data-hook="review"]')
    for review in reviews:
        rate = review.xpath('.//span[@class="a-icon-alt"]/text()')[0]
        rate = search('(\d+[.,]\d)',rate).group(0)
        if rate == '5.0' or rate == '5,0':
            title = review.xpath('.//a[@data-hook="review-title"]/text()')
            if title:
                review_title = title[0]
                review_title = review_title.lstrip().rstrip().replace('\n', '')
                # print(title_traslate)
            else:
                review_title = ''
            body = review.xpath('.//span[@data-hook="review-body"]')[0].xpath('string(.)')
            if body:
                review_body = body
                review_body = review_body.lstrip().rstrip().replace('\n', '')
                # print(body_traslate)
            else:
                review_body = ''
            k = review_title,review_body
            if k not in list:
                list.append(k)
    return list

def page(l,response):
    page = response.xpath('//li[@class="a-last"]/a/@href')
    if page:   
        page_url = l + page[0]
    else:
        page_url = ''
    return page_url

def main():
    while 1:
        url = input('请输入reviews地址：')
        headers={
            'authority':'translate.google.cn',
            'method':'GET',
            'path':'',
            'scheme':'https',
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie':'',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36','x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE=',
        }
        l = search('(.*?//.*?/)',url).group(0)
        try:
            asin = search('(B0.*?)/',url).group(0)
            print('此商品asin：%s'%asin)
            url_1 = l + 'gp/customer-reviews/widgets/average-customer-review/popover/ref=dpx_acr_pop_?contextId=dpx&asin=' + asin
            
        except Exception as e:
            print('检索不到该产品asin，请重新输入')
            continue
        response = requests.get(url_1,headers=headers)
        response = etree_html(response)
        url_2 = response.xpath("//a[@class='a-size-small a-link-emphasis']/@href")
        p = response.xpath("//a[@class='a-size-small a-link-emphasis']/text()")[0]
        num = search('(\d+)',p).group(0)
        if url_2:
            url_3 = url_2[0]
            break
        else:
            print('该产品没有reviews或地址有误，请重新输入')
            continue
    page_urls.append(url_3)
    n = 1
    j = int(int(num)/10) + 1
    print('此商品最多有%s页评论'%j)
    m = int(input('请输入要获取的页码数：'))
    for page_url in page_urls:
        if page_url:
            if n <= m:
                print('正在解析第%s页，请稍等。。。'%n)
                response = requests.get(page_url,headers=headers)
                response = etree_html(response)
                page_url_2 = page(l,response)
                if page_url_2:
                    page_urls.append(page_url_2)
                list = parse(response)
                print('第%s页解析完成。。。'%n)
                n += 1
            else:
                break
        else:
            print('已超出此产品评论最大页数。。。')
    filename = input('请输入要保存的文件名：')
    filename = filename + '.csv'
    f = open(filename,'a',encoding='utf8')
    for i in range(len(list)):
        for j in range(2):
            x = list[i][j]

            x = x.replace(',','，')
            f.write(x)
            if j < 1:
                f.write(',')
        f.write('\n')
    f.close()
    print('写入完成。。。')

if __name__ == '__main__':
    main()
