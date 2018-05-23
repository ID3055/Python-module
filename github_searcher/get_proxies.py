#! /usr/bin/env python
# coding:utf-8
import requests
import json
import time

def get_proxies(usrl):
    response = requests.get(url)
    content = response.content
    return content

if __name__ == "__main__":
    while True:
        url = r'http://www.xiongmaodaili.com/xiongmao-web/freeip/list'
        content = get_proxies(url)
        content = json.loads(content)
        list = ''
        for item in content['obj']:
            # print item
            list += str(item['ip']) + ':' + str(item['port']) + '\n'
        list = list.strip('\n')
        with open('proxies.txt', 'w') as f:
            f.write(list)
        print u'更新代理地址完成 ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        time.sleep(15)