#/usr/bin/python3

import requests, os
from bs4 import BeautifulSoup
import multiprocessing as mult
from multiprocessing.pool import ThreadPool

def animeSpider(request_url):
    filename = os.path.join(dir, request_url.split('/')[-1])
    request_url = os.path.join(Root_url,request_url)
    #print(request_url)
    if os.path.exists(filename):
        print(filename,'already exists!')
        return
    try:
        r = requests.get(request_url, stream=True, timeout=100)
        #print(filename)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: 
                    f.write(chunk)
                    f.flush()
        #print(filename,'sucess download')
        return
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        print(e)
        return 
        
        
def makedir(soup):
    dir =''
    try:
        dir = soup.find("a",{"id":"tooltip-day"}).text.split('/')[0]
        dir = os.path.join(home_dir,dir)
    except:
        pass
    else:
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        try:
            title = soup.find('meta',{"name":"keywords"})['content'].replace('～','')
            title = soup.find('meta',{"name":"keywords"})['content'].replace('～','')
            title = soup.find('meta',{"name":"keywords"})['content'].replace('?','')
            title = soup.find('meta',{"name":"keywords"})['content'].replace('+','')
            title = soup.find('meta',{"name":"keywords"})['content'].replace('-','')
            title = soup.find('meta',{"name":"keywords"})['content'].replace(' ','')
            title, company = title.split(',')
            dir = os.path.join(dir,company)
            if os.path.exists(dir) is False:
                os.mkdir(dir)
            dir = os.path.join(dir,title)
            if os.path.exists(dir) is False:
               os.mkdir(dir)
        except:
            pass
    return dir
    
if __name__ == "__main__":
    mult.freeze_support()
    pool = ThreadPool(mult.cpu_count()-1)
    home_dir = 'getchu'
    if os.path.exists(home_dir) is False:
        os.mkdir(home_dir)
    Root_url = 'http://www.getchu.com/'
    start = 0
    end = 1000000
    for i in range(start, end + 1):
        url = 'http://www.getchu.com/soft.phtml?id=%d&gc=gc' % i
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        targetUrlList = []
        for img in soup.find_all("img", alt=lambda value: value and value.startswith("キャラ")):
            target_url = img['src']
            targetUrlList.append(target_url)
        if len(targetUrlList) ==0:
            #print('no image')
            pass
        else:
            dir = makedir(soup)
            pool.map(animeSpider,targetUrlList)
        if i %1000 ==0:
            print('%d / %d' % (i, end))
    pool.close()
    pool.join()