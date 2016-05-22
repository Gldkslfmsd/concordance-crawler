# Customizing ConcordanceCrawler 

## Simple usage

How can you customize ConcordanceCrawler? The easiest way is to use `LoggingCrawler` class:

```py
from ConcordanceCrawler.core.logging_crawler import LoggingCrawler

crawler = LoggingCrawler()
```

It gives you an infinite generator of concordances. This class logs process of crawling, catches exceptions and errors occurring during visit of links, logs them and continues with other links.

You can also use `ConcordanceCrawler.core.concordance_crawler.ConcordanceCrawler` class, which only allows crawling without logging and error handling. 

Once you create your ConcordanceCrawler or LoggingCrawler object, you can configure it by your own desires and then crawl concordances as in following snippet. It will crawl 20 concordances with a word `Praha`.

```py
for _,x in zip(range(20), crawler.yield_concordances(['Praha']):
    print(x) 
```

## Example code

Click [here](https://github.com/Gldkslfmsd/concordance-crawler/blob/dev/examples/czech_concordance_crawler.py) to see an example of using customized ConcordanceCrawler.

## Documentation

**class LoggingCrawler**

You may to use its "public" methods:

- `yield_concordances(words)` -- returns a generator object yielding concordances

 *  `words`: a nonempty list of strings. They are words whose concordances should be
		crawled. It should be a single word, or a single word and its other forms.
		The first one is considered as a dictionary form, links will be found only
		with this form.

- `setup(**kwargs)` -- setup configurable parts of setup (Logging|Concordance)Crawler

 * `**kwargs`: a key=value pairs, keys are configurable attribute names of (Logging|Concordance)Crawler, values are their new values.

## How to setup your crawler

Trivial example:

```py
crawler = ConcordanceCrawler()
crawler.setup(filter_link=lambda _: True)
```
This will replace a filter every link must pass through before it's visited by a trivial filter that everything passes through.

Here is a complete description of configurable attributes. Include them as keyword arguments for `setup` method. All of them (except the first two) are functions. They're expected behavior in ConcordanceCrawler is as follows:

- `allow_logging` -- boolean value, if set to True, your LoggingCrawler will log progress of crawling. It's useful to see whether your crawler works or is stuck. Default value is True.

- `bazgen` -- bazword generator object. It's used for generating links by default get_links function. It's an object inheriting `AbstractBazwordGenerator` class in `ConcordanceCrawler.core.bazwords` module.

- `get_links(keyword)` -- gets keyword, returns a list of links. A link is a string.

 By default it finds them on Bing.com with usage of bazword generator.

- `filter_link(url)` -- filter links that will be visited. 

 By default it excludes links ending by '.docx', '.doc', '.pdf', '.ppt', '.pptx', '.odt', or '.img', because they probably contain non-text document. ConcordanceCrawler is not adapted for extraction from these formats. 

- `get_raw_html(url)` -- Extracts document on given url.
 * `url`
 * returns: a pair, document residing on a given url (as string) and http response headers (as returned from `requests` library).

 By default it uses `requests` library and `stopit` to stop execution if it lasts more than 60 seconds. (Because some documents can be really long.) To every request http header it adds User-Agent value of some real existing browser. It doesn't catch any errors from `requests`.

- `norm_encoding(document, headers)` -- normalize encoding of raw document or return None, if it's impossible.

 What is implemented: In fact it only returns the same document or `None`. If the document is html and there is metatag specifying `allowed` encoding (which is another parameter), or the encoding is given in http response header and these two values are not unequal, then the `document` is returned, `None` otherwise.

- `predict_format(normed_document)` -- returns a probable format of document as string

- `accept_format(format)` -- returns True, if format returned by `predict_format` is acceptable, False otherwise. Then extraction of document will be skipped.

 These two method are not implemented in ConcordanceCrawler and do nothing.

- `get_visible_text(raw_html)` -- assumes that `raw_html` on the input is html. It tries to exclude all html tags and texts invisible by humans displaying the document via web browser.
 * `raw_html` -- raw document extracted from Internet. We assume it's a text in html, but sometimes it can be invalid assumption.
 * returns: string containing only visible parts of the document

- `language_filter(text)` -- gets a text. Returns True if language of the text should be accepted, False otherwise.

 Implemented: it filters English texts. It uses comparison of 1,2,3-grams of given text and really long English Wikipedia text.

- `sentence_segmentation(text)` -- gets a text, returns a list of sentences contained in text.

 Implemented: it uses `segtok` library improved by one additional rule.

- `sentence_filter(sentence)` -- returns True/False meaning whether the sentence can be included to corpus or not.

 By default it does nothing, all sentences pass. Optional excluding of concordances containing any non-ASCII character is done by this way.

- `concordance_filtering(sentence, target_words)`

 * sentence
 * target_words -- a list of target words

 * returns: `None`, if any of target words is not presented in a sentence, or a triple (word, start, end).

   * word is a target word which was found in a sentence

    * start is its starting index in sentence

     * end is the first index behind word occurrence in a sentence

   Example: `concordance_filtering('a b c', ['d', 'e, 'b'])` returns `('b', 2, 3)`.
   
   Implemented: In ConcordanceCrawler it's implemented by two ways, the first uses simple regular expression and the other uses automatic lemmatizing via `textblob`. 




		
