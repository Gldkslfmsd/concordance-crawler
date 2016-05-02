
from ConcordanceCrawler.core.logging_crawler import *
import langdetect
import logging

class CzechConcordanceCrawler(LoggingCrawler):
    
    def __init__(self):
        super().__init__()
        
        self.setup(language_filter=self.czech_filter, filter_link=self.filter_non_czech_links)
   
       
    def czech_filter(self, text):
        if langdetect.detect(text) == 'cs':
            return True
        return False
    
    def filter_non_czech_links(self, link):
        if 'cz' in link and ConcordanceCrawler.filter_link(self, link):
            return True
        logging.debug('link '+link+' was filtered')
        self.links_filtered += 1
        return False


crawler = LoggingCrawler()
crawler.setup(language_filter=CzechConcordanceCrawler.czech_filter)


c = CzechConcordanceCrawler()
c.Logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)-15s %(levelname)s: %(message)s", )


print(c.czech_filter("ahoj, je tenhle text v češtině? Nebo v čem jiném? by mohl být?"))

import pprint
for _,x in zip(range(20), c.yield_concordances(["pusa"])):
    print(pprint.pformat(x))    


