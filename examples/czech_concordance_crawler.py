'''Example code of using ConcordanceCrawler as a library. 

ConcordanceCrawler is adapted here to crawl Czech concordances, but it can be very 
easily changed to (nearly) any other language.
'''

from ConcordanceCrawler.core.logging_crawler import *

import langdetect
import logging

# create our own LoggingCrawler object
crawler = LoggingCrawler()
     
def czech_filter(text):
    '''filter Czech text with usage of langdetect library. 
    To filter other language simply change 'cs' to other value, e.g. 'de', 'sk', 'pl' etc.
    '''
    if langdetect.detect(text) == 'cs':
        return True
    return False

def filter_non_czech_links(link):
    '''This is a filter that every link must pass before we visit it. 
    To make crawling faster we want to exclude all links on other than cz, net, org or eu domain.
    (We don't do it perfectly, but simply.)
    We concatenate our filter with default ConcordanceCrawler.filter_link who filters links 
    ending on a suffix of non-text file-formats, e.g. pdf, iso, img, doc...
    '''
    if any(s in link for s in ('cz', 'net', 'org', 'eu')) and ConcordanceCrawler.filter_link(link):
        return True
    
    # we print a debug message about filtering of this link
    logging.debug('link '+link+' was filtered')
    
    # increment counter of filtered links in our crawler object, it will log this number in statuses
    crawler.links_filtered += 1
    return False


# setup our own methods to our crawler object
crawler.setup(language_filter=czech_filter, filter_link=filter_non_czech_links,
    # logging from crawler can be enabled or disabled by this option
    # by default it's enabled
    # it's useful because than you can see whether a crawler works and is not stuck
    allow_logging=True
)

# allow logging
logging.basicConfig(level=logging.DEBUG,
                    # setup more readable format of log messages
                    format=LoggingCrawler.log_format, )


import pprint

# yield 20 concordances with any of grammatical forms of Czech word `kůň` (a horse)
for _,x in zip(range(20), crawler.yield_concordances("kůň koně koněm koni koní koním koních koňmi".split())):
    # and let them pretty printed to output
    print(pprint.pformat(x))    


