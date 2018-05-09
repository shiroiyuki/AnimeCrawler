#/usr/bin/python3

import requests, os
from bs4 import BeautifulSoup
import multiprocessing as mult
from multiprocessing.pool import ThreadPool

def download(url):
    filename = os.path.join('data', url.split('/')[-1])
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=100)
        #print(r)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        #print(filename,'sucess download')
        return
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        #print('error1')
        return
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        #print(e)
        return
if __name__ == "__main__":
    mult.freeze_support()
    #pool = mult.Pool(mult.cpu_count() + 2)
    pool = ThreadPool(mult.cpu_count() + 2)
    if os.path.exists('data') is False:
        os.makedirs('data')
    print("hello")
    start = 1
    end = 9942
    for i in range(start, end + 1):
        url = 'http://konachan.com/post?page=%d&tags=' % i
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        targetUrlList = []
        filenameList = []
        for img in soup.find_all('img', class_="preview"):
            target_url = img['src']
            targetUrlList.append(target_url)
        pool.map(download,targetUrlList)
        print('%d / %d' % (i, end))
    pool.close()
    pool.join()
