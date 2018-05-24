# -*- coding: utf-8 -*-
import json
import re
import sys
import time
import traceback

import requests
from bs4 import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf8')


class Searcher():
    def __init__(self, keywords, cookies, max_page = 1, proxy=None):
        self.keywords = keywords.replace(' ','%20')
        self.cookies =  cookies

        self.max_page = max_page
        self.proxy = proxy
        self.page = 1

        self.headers = {            
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "github.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
                        }

        self.result = [] 
        self.statu = 'success'
        self.process()

    def set_error(self):
        self.statu = 'error'            
        
    def get_page(self, url):
        '''
        获取搜索结果页面，返回html代码
        '''
        page_content = ''
        try:
            session = requests.Session()
            headers = self.headers
            cookies = self.cookies
            response = session.get(url, headers=headers, cookies=cookies, timeout=10, proxies = self.proxy)
            
            page_content = response.content
        except Exception as e:
            # traceback.print_exc()
            print e
        finally:
            return page_content

    def get_code(self,content,first = False):
        '''
        获取相关结果的repo名，repo地址，文件地址，代码片段
        '''
        if not content:
            self.set_error()
            return
        if 'Whoa there' in content:
            print 'rate limit'
            self.set_error()
            return

        soup = BeautifulSoup(content,'html.parser')
        #查找到所有单个的结果块
        blocks = soup.find_all("div", attrs={"class": "code-list-item col-12 py-4 code-list-item-public "})
        if not blocks:
            print 'empty list'
            return

        #开始处理结果
        for i in blocks:
            if not i:
                continue
            tmp_url = []  #文件url
            tmp_repo = [] #repo名
            tmp_code = [] #代码片段
            one_search_result = {}#单个结果的字典

            #repo和code文件url
            for tag_a in i.find("div", attrs={"class": "d-inline-block col-10"}).find_all('a'):
                tmp_repo.append(tag_a.get_text())
                tmp_url.append('https://github.com' + str(tag_a.get('href')))
                
            #代码片段
            for tag_td in i.find('table').find_all('td', attrs={"class": "blob-code blob-code-inner"}):
                # print tag_div
                tmp_code.append(tag_td.get_text())

            #处理存入字典
            one_search_result["repo"] = tmp_repo[0]
            one_search_result["code_url"] = tmp_url[1]
            one_search_result["repo_url"] = tmp_url[0]
            one_search_result["code"] = ''.join(tmp_code)
            self.result.append(one_search_result)

        #处理分页
        if first:
            try:
                result_num_text = soup.find("div", attrs={"class": "d-flex flex-justify-between border-bottom pb-3"}).find('h3').text
                result_num_text = result_num_text.replace(' ','').replace(',', '').replace('\n', '').replace('\r', '')
                
                m = re.match(r'(?P<num>\d+)[\s\S]*', result_num_text)
                self.page = int(m.group('num'))
                if not self.page % 10 == 0:
                    self.page = self.page/10 + 1
                print 'total page: %s'% self.page
            except:
                traceback.print_exc()
                self.page = 1

    def process(self):
        '''
        开始
        '''
        start_url = "https://github.com/search?o=desc&p=1&q=%s&ref=cmdform&type=Code" % (self.keywords)
        print start_url
        content = self.get_page(start_url)  
        # time.sleep(5)     
        self.get_code(content,True)
        if self.statu != 'success':
            return
        if self.page >= 1:
            if self.page > self.max_page:
                end_page = self.max_page
            else:
                end_page = self.page
            for page_num in range (2,end_page + 1):
                # time.sleep(5)
                print 'page %s' % (page_num,)
                url = "https://github.com/search?o=desc&p=%s&q=%s&ref=cmdform&type=Code" % (str(page_num),self.keywords)
                content = self.get_page(url)
                self.get_code(content)

    def response(self):
        res_dict = {
            "keyword": self.keywords.replace('%20',' '),
            "statu": self.statu,
            "result": self.result
            }
        return json.dumps(res_dict)

if __name__ == "__main__":
    pass
    