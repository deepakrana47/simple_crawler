import Queue, requests, urllib2
import threading, time
import random

def get_links(links, num):
    """
    function to get num number of links out of links list
    :param links: contain the list of links
    :param num: contain the number of links to be extracts out of list
    :return links
    """
    il = links[:num]
    for i in range(num):
        if links:
            links.pop(0)
        else:
            break
    return il


class Crawler:
    """
    Crawler is a class consist of crawling with following features
    Feature Provided:
        - multi requesting
        - multi proxy user
        - multi User Agent
        - random timeout in between 0 to given timeout
    """
    def __init__(self, nReqs=4, proxy=None, tSleepBetThreads=.5, timeout=5, retry=2, userAgent = None):
        self.q = Queue.Queue()
        self.nReqs = nReqs
        self.tsbt = tSleepBetThreads
        self.proxy = proxy if proxy else [None]
        self.uA = userAgent if userAgent else ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0']
        self.to = timeout
        self.retry = retry

    def get_pindex(self):
        return random.randrange(0, len(self.proxy)) if len(self.proxy) else 0

    def get_hindex(self):
        return random.randrange(0, len(self.uA)) if len(self.proxy) else 0

    def crawler(self, links):
        responses = {}
        count = 0
        while links:
            resp = self.crawl(links)
            responses.update(resp)
            count+=self.nReqs
        return responses

    def crawl(self, links):
        lks = get_links(links, self.nReqs)
        thread = []
        for url in lks:
            pindex = self.get_pindex()
            hindex = self.get_hindex()
            thread.append((threading.Thread(target=self.getReq, args=(url, pindex, hindex))))
            thread[-1].start()
            time.sleep(self.tsbt)
        for t in thread:
            t.join()
        resp = {}
        while not self.q.empty():
            resp.update(self.q.get())
        return resp

    def curl(self, url, pindex, hindex):
        """
        return content at url.
        return empty string if response raise an HTTPError
        """
        try:
            response = None
            print "retrieving url... %s" % (url)
            for i in range(self.retry):
                try:
                    response = requests.get(url, headers={'User-Agent': self.uA[hindex]}, timeout=random.randrange(1,self.to+1), proxies=self.proxy[pindex] if self.proxy else None)
                    break
                except requests.Timeout as e:
                    print i, "timeout :: proxy:", self.proxy[pindex]
                except requests.exceptions.ProxyError:
                    print "proxy error:", self.proxy[pindex]
                    response = None
                except requests.exceptions.SSLError:
                    print "SSL error:", self.proxy[pindex]
                    response = None
            return response
        except urllib2.HTTPError, e:
            print "error %s: %s" % (url, e)
            return None

    def get(self, url, pindex, hindex):
        resp = self.curl(url, pindex, hindex)
        return resp

    def getReq(self, url, pindex, hindex):
        resp = self.get(url, pindex, hindex)
        self.q.put({url: resp})