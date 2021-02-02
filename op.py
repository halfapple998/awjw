import threading
from queue import Queue
from lxml import etree
import requests
import parsel
import time
import random
import re
import csv
from urllib import request
import threading


def check_ip(proxy, url):
    """检测ip的方法"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5)  # 超时报错
        if response.status_code == 200:
            can_use.append(proxy)
    except Exception as error:
        print(error)


# 1、确定爬取的url路径，headers参数

def page(i):
    base_url = 'https://www.kuaidaili.com/ops/proxylist/%d/' % i
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    # 2、发送请求 -- requests 模拟浏览器发送请求，获取响应数据
    response = requests.get(base_url, headers=headers)
    data = response.text
    # print(data)

    # 3、解析数据 -- parsel  转化为Selector对象，Selector对象具有xpath的方法，能够对转化的数据进行处理
    # 3、1 转换python可交互的数据类型
    html_data = parsel.Selector(data)
    # 3、2 解析数据
    parse_list = html_data.xpath('//*[@id="freelist"]/table/tbody/tr')  # 返回Selector对象
    # print(parse_list)

    # 免费 IP  {"协议":"IP:port"}
    # 循环遍历，二次提取

    for tr in parse_list:
        proxies_dict = {}
        #  http_type = tr.xpath('./td[4]/text()').extract_first()
        http_type = 'http'
        ip_num = tr.xpath('./td[1]/text()').extract_first()
        port_num = tr.xpath('./td[2]/text()').extract_first()
        # print(http_type, ip_num, port_num)

        # 构建代{过}{滤}理ip字典
        proxies_dict[http_type] = "http://" + ip_num + ':' + port_num
        proxies_dict['https'] = "https://" + ip_num + ':' + port_num
        # print(proxies_dict)
        proxies_list.append(proxies_dict)


if __name__ == '__main__':
    start = time.time()
    proxies_list = []
    threads = []
    can_use = []
    c = input("please input your want to find how much pages")
    for i in range(1, int(c) + 1):
        t = threading.Thread(target=page, args=(i,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

    print(proxies_list)
    print("获取到的代{过}{滤}理ip数量：", len(proxies_list), '个')
    url = "https://music.163.com/"
    # url ='http://httpbin.org/get'
    # 检测代{过}{滤}理ip可用性
    threads = []
    for i in proxies_list:
        t = threading.Thread(target=check_ip, args=(i, url))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

    print("能用的代{过}{滤}理：", can_use)
    print("能用的代{过}{滤}理数量：", len(can_use))
    proxy = random.choice(can_use)
    print(proxy)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    end = time.time()
    print('cost time', end - start)
    # response = requests.get(url, headers=headers, proxies=random.choice(can_use))

    # print(response.text)

    '''with open ('ip.txt','w',encoding='utf-8')as f:
        for i,a in can_use:

            f.write(i)
            f.write(a)
            f.write('\n')'''

'''proxy_support=urllib.request.ProxyHandler(proxy)

opener=urllib.request.build_opener(proxy_support)
opener.addheaders=[{"User-Agent"," Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}]
urllib.request.install_opener(opener)
response=urllib.request.urlopen(url)
html=response.read().decode("utf-8")
print(html)

'''