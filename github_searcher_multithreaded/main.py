#! /usr/bin/env python
# coding:utf-8

import github_searcher
import github_login
import json
import time
import sqlite3
import random
def search(cookie, keywords, proxies=None):
    g = github_searcher.Searcher(keywords, cookie, 3, proxies)
    return g.response()

def run(cookie, keyword, proxies=None):
    conn = sqlite3.connect('CVE.db')
    cursor = conn.cursor()
    try:
        cursor.execute('create table cve (id varchar(20) primary key, statu varchar(10), file_url text)')
    except:
        pass
    
    poc_id = keyword
    result_str = ''
    result_statu = ''
    print('-----------------------------------------------')
    keywords = poc_id + " poc"
    print keywords
    
    print u'开始时间: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    cursor.execute(r'select statu from cve where id="%s"' % poc_id)
    conn.commit()
    values = cursor.fetchall()
    if not values:
        print poc_id + u' 未抓取，开始抓取' 
    elif values[0][0] == 'success':
        print poc_id + u'已经存在，抓取完成'
        return
    elif values[0][0] == 'error':
        print poc_id + u' 抓取错误，开始重新抓取' 
    
    result = search(cookie, keywords, proxies)
    result = json.loads(result)
    
    result_statu = result['statu']
    for item in result['result']:
        result_str += item['code_url'] + '@@@'

    
    print result_statu
    print result_str
    
    cursor.execute(r'insert or replace into cve (id, statu, file_url) values ("%s", "%s", "%s")' % (poc_id, result_statu, result_str))
    conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    while True:
        username = ''
        password = ''
        github = github_login.GithubLogin(username, password)
        cookie = github.cookie

        with open('CVE.txt','r') as f:
            lines = f.read()
            for line in lines.split('\n'):
                with open('proxies.txt', 'r') as f:
                    list = f.read()
                proxy = {"https": random.choice(list.split('\n'))}
                run(cookie, line, proxy)
