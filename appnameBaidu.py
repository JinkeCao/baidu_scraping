#coding=utf-8
#!/usr/bin/python
import urllib
import json
from bs4 import BeautifulSoup as BS
import time
import timeout_decorator

i = 0
outputfile = ""

@timeout_decorator.timeout(2)
def genjson(word, outputfile):
    baseUrl = 'http://www.baidu.com/s'
    page = 1
    data = {'wd':word,
            'pn':str(page-1)+'0',
            'tn':'baidurt',
            'ie':'utf-8',
            'bsst':'1'}
    data = urllib.parse.urlencode(data)
    url = baseUrl+'?'+data
    request = urllib.request.Request(url)  
    response = urllib.request.urlopen(request)
    html = response.read()
    soup = BS(html)
    td = soup.find_all(class_='f')
    for t in td:
        font_str = t.find_all('font',attrs={'size':'-1'})[0].get_text()
        start = 0
        realtime = t.find_all('div',attrs={'class':'realtime'})
        if realtime:
            realtime_str = realtime[0].get_text()
            start = len(realtime_str)
        end = font_str.find('...')
        appinfo = json.dumps({"appname":str(word),
                              "brief":str(t.h3.a.get_text()),
                              "content":str(font_str[start:end+3])},
                             ensure_ascii = False,
                             sort_keys = True)
        with open(outputfile, 'a') as info:
            print (appinfo, file=info)
            
if __name__ == '__main__':
    try:
        with open('appname') as data:
            for each_line in data:
                try:
                    if i % 10000 == 0:
                        outputfile = str((i // 10000) + 1) + "_appinfo.json"
                    appname = each_line.strip()
                    word = appname 
                    genjson(word, outputfile)
                    i = i + 1
                    print(str(i) + " " + word)
                except Exception as e:
                    print (e)
                    continue
    except Exception as e:
        print (e)
