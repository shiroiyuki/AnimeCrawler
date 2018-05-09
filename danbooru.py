#/usr/bin/python3

import requests, os
from bs4 import BeautifulSoup
import multiprocessing as mult
from multiprocessing.pool import ThreadPool

def animeSpider(request_url):
    filename = os.path.join('danbooru', request_url.split('/')[-1])
    if os.path.exists(filename):
        print('file already exists!')
        return
    try:
        r = requests.get(request_url, stream=True, timeout=100)
        print(filename)
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
    
if __name__ == "__main__":
    mult.freeze_support()
    pool = ThreadPool(mult.cpu_count() + 2)
    if os.path.exists('danbooru') is False:
        os.mkdir('danbooru')
    Root_url = 'https://danbooru.donmai.us'
    url = Root_url
    while True:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        targetUrlList = []
        for img in soup.find_all('img', {'itemprop':'thumbnailUrl'}):
            temp = img['src']
            targetUrlList.append(temp)
        pool.map(animeSpider,targetUrlList)
        try:
            arrow = soup.find('a', {'rel':'next'})
        except:
            print('finish')
            break
        url = Root_url + arrow['href']
        #print(arrow['href'])
    pool.close()
    pool.join()
