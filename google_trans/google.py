import json
import sys
import traceback
from urllib import quote

import execjs
import psycopg2
import requests

reload(sys)
sys.setdefaultencoding( "utf-8" )
requests.packages.urllib3.disable_warnings()  

class Py4Js():  
    def __init__(self):  
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

py = Py4Js()


def get_tran(word):
    # wordtmp = word
    try:
        code = py.getTk(word)
    except:
        traceback.print_exc()
        # print wordtmp
        exit()
    word = quote(word,safe='')
    # code = py.getTk(word)
    url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=4&tk={}&q={}"
    _url = url.format(code, word)
    resp = requests.get(_url, verify=False)
    if resp.text:
        try:
            js_data = json.loads(resp.text)
            first = js_data[0]
            res = ""
            for item in first:
                if len(item) < 1:
                    continue
                if not item[0]:
                    continue
                res += item[0]
            # print _url
            # print '--------------'
            return res
        except Exception:
            traceback.print_exc()
            # print wordtmp
            # print '-------------------'
    return ""

if __name__ == '__main__':
    print(get_tran('chinese'))
