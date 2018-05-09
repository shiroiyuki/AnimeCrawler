#/usr/bin/python3

import requests, os
from bs4 import BeautifulSoup
import multiprocessing as mult
from multiprocessing.pool import ThreadPool

def animeSpider(i):
    url = "https://kukuo.nctu.me/anime/photo/R18/%d.png" % i
    filename = os.path.join('kukuo_18', url.split('/')[-1])
    if os.path.exists(filename):
        print('file already exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=100)
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
    if os.path.exists('kukuo_18') is False:
        os.mkdir('kukuo_18')
    index = range(1,300)
    pool.map(animeSpider, index)
    pool.close()
    pool.join()
