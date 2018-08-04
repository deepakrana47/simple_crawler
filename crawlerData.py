import bs4, os, pickle
from crawler import Crawler


class CrawlData():
    """
    CrawlData use crawler and beautifulSoup class to perform depth crawling on a website. It takes input as following
    :param crawllimit: the number of url to crawl in one call
    :param linkprocessor: it a user definded function that process the new links based on user filter
                          syntax::  function(links, domain)
                          return::  filter_links
    :param deep: this is boolen parameter to defind weather to go for depth or not
    :param crawl: this is the crawler object as input if given
    """
    def __init__(self, crawllimit=32, linkprocessor=None, deep=True, crawl=None):
        self.cl = crawllimit
        self.crawl = crawl if crawl else Crawler()
        self.deep = deep
        if linkprocessor:
            self.lp = linkprocessor
        else:
            # def a(links, domain): return links
            self.lp = lambda links, domain: links

    def processResponse(self, responses, domain):
        pages = {}
        pLinks, npLinks = [], []
        for i in responses:
            if responses[i] is not None:
                if responses[i].status_code == 200:
                    pages[i] = responses[i].text
                if responses[i].status_code == 304:
                    print responses[i].text
                pLinks.append(i)
            else:
                npLinks.append(i)
        return pages, pLinks, npLinks

    def getLinks(self, blocks):
        links = []
        for i in range(len(blocks)):
            block = blocks[i]
            if type(block) == bs4.element.Tag:
                if block.name == 'a':
                    if 'href' in block.attrs:
                        links.append(block.attrs['href'].strip(' |\t|\n'))
                else:
                    t1 = self.getLinks(list(block))
                    links += t1
        return links

    def getLinksData(self, page):
        soup = bs4.BeautifulSoup(page, 'html.parser')
        links = self.getLinks(list(soup))
        return links

    def HtmlExraction(self, links, clinks, domain=None):

        ## crawling of first CRWLLIMIT link is done and return response as dict {link: response}
        if(domain):
            lks = [domain + i if i[0] == '/' else i for i in links[:self.cl]]
        else:
            lks = links

        responses = self.crawl.crawler(lks)
        links = links[self.cl:]

        ## response processing is done here
        pages, pLinks, npLinks = self.processResponse(responses, domain)
        clinks += pLinks

        # extracting new links from pages
        newlinks = []
        for i in pages:
            newlinks += list(set([j for j in self.getLinksData(pages[i]) if j and (j[0] == '/' or j.startswith(domain)) and j.find('#') == -1]))

        # adding new links
        if self.deep:
            newlinks = self.lp(newlinks, domain)
            for j in newlinks:
                if j not in clinks:
                    links.append(j)

        return [pages, list(set(links+npLinks)), list(set(clinks))]

    def smallDataCrawling(self, links, clinks=None):
        """
        this is the entry function for Crawl for fixed size amount of links
        :param domain: eg: http://www.way2edu.com
        :param links: list of links to be crawl
        :param clinks: list of links that was crawled
        :return:
        """
        if not links:
            print "Provide links for crawling"
            return []

        clinks = clinks if clinks else []

        data = {}
        while links:
            domaindata, links, clinks = self.HtmlExraction(links=links, clinks=clinks)
            if not domaindata:
                break
            data.update(domaindata)
        return data

    def bigDataCrawling(self, domain, links=[], clinks=[], ecount=200):
        """
        this is an iterator function for Crawl for fixed and not known (website crawling) amount of links,
        where data is stored in 'domainname' directory in current folder
        :param domain: eg: http://www.way2edu.com
        :param links: list of links to be crawl
        :param clinks: list of links that was crawled
        :param ecount: store values of links and clinks when count == ecount
        :return:
        """
        linksFile = 'links.pkl'
        clinksFile = 'clinks.pkl'
        destdir = os.getcwd() + '/' + domain.split('.')[1] + '/'

        if not os.path.isdir(destdir):
            os.mkdir(destdir)

        # initiatition of links and clinks
        if links:
            links = links
            clinks = clinks
        else:
            links = pickle.load(open(destdir + linksFile, 'rb')) if os.path.isfile(destdir + linksFile) else [domain]
            clinks = pickle.load(open(destdir + clinksFile, 'rb')) if os.path.isfile(destdir + clinksFile) else []

        count = 0
        while links:
            domainData , links, clinks = self.HtmlExraction(domain=domain, links=links, clinks=clinks)
            if domainData:
                yield domainData
            else:
                break
            count += len(domainData)
            print "%d Links processed :: %d Links to be processed"%(len(clinks), len(links))
            if count > ecount:
                pickle.dump(clinks, open(destdir + clinksFile, 'wb'))
                pickle.dump(links, open(destdir + linksFile, 'wb'))
                print "%d Links are recorded"%(len(clinks))
                count = 0
        pickle.dump(clinks, open(destdir + clinksFile, 'wb'))
        pickle.dump(links, open(destdir + linksFile, 'wb'))
        print "%d Final Links are recorded" % (len(clinks))
        yield []
