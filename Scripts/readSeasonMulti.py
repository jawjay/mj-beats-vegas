# from urlparse import urlparse
import urllib.parse as urlparse
from threading import Thread
import  sys
import http.client as httplib
from multiprocessing import Queue
import requests
import multiprocessing
import pickle



def readBoxScore2(game):
    address = 'http://www.basketball-reference.com/boxscores/'+game+'.html'
    try:
        with urllib.request.urlopen(address) as url:
            s = url.read()
            bs = BeautifulSoup(s,"html.parser")
            #return bs
    except HTTPError:
        return None
    data = []
    for t in bs.findAll('table'):
    # should go away basic, away advanced,home basic, home advanced
        data.append([a.text for a in t.findAll('tr')[-1].find_all('td')])

    return data


def bbGetter(stuff):
    session = requests.Session()
    stuff_got = []

    for game in stuff:
        response = session.get( 'http://www.basketball-reference.com/boxscores/'+game+'.html')
        stuff_got.append(response)
    return stuff_got


concurrent = 200

def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print(status, url)
    
seasons = pickle.load(open('SeasonGames_1985-2017.pkl','rb'))
t_urls = ['http://www.basketball-reference.com/boxscores/'+game+'.html' for game in seasons['2015']]
q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in t_urls:
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)