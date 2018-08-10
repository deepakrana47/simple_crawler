# simple_crawler

to install simple_crawler:

## pip install simple-crawler

simple_crawler is a simple crawler for crawling links or websites where it provide setting miltiple requesting, multiple proxy, multiple userAgent and other features.

Examples::

    from simple_crawler import crawler, crawlerData
    proxy = [
        {'http':'http://67.205.148.246:8080','https':'https://67.205.148.246:8080'},
        {'http':'http://54.36.162.123:10000','https':'https://54.36.162.123:10000'},
    ]

    links = [
        'http://www.way2edu.a2hosted.com/course/414876',
        'http://www.way2edu.a2hosted.com/course/415606',
        'http://www.way2edu.a2hosted.com/course/415695',
        'http://www.way2edu.a2hosted.com/course/415905',
    ]

    # sample for performing simple crawler
    c = crawlerData.CrawlData()
    data = c.smallDataCrawling(links=links)

    # sample for performing crawling with proxy
    crawl = crawler.Crawler(proxy=proxy)
    c = crawlerData.CrawlData(crawl=crawl)
    data = c.smallDataCrawling(links=links)

    # sample for performing domain crawling
    domain = 'http://www.way2edu.a2hosted.com'
    c = crawlerData.CrawlData()
    for domaindata in c.bigDataCrawling(domain=domain):
        print domaindata
