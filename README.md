# ConcordanceCrawler

[![Build Status](https://travis-ci.org/Gldkslfmsd/concordance-crawler.svg?branch=master)](https://travis-ci.org/Gldkslfmsd/concordance-crawler)

ConcordanceCrawler is a tool for automatic concordance extraction from the
Internet. A concordance is a sentence containing some given word. Take an
English word, and ConcordanceCrawler will be able to download you hundreds
thousands of sentences with your word. 

ConcordanceCrawler is a console application whose main purpose is
crawling of English verbs or other words, but you can also use its API. It allows you to
adapt ConcordanceCrawler to any other language. 

## Installation

I recommend ConcordanceCrawler installation in Python virtual environment (see
https://virtualenv.pypa.io/ ). 

```
virtualenv -p python3 p3
source p3/bin/activate
pip install git+https://github.com/Gldkslfmsd/concordance-crawler.git
```

If you want to use also automatic conjugating of English verbs (or
inflecting of nouns or comparing of adjectives), then install also
`textblob` library, but it's not necessary, you can use ConcordanceCrawler
pretty well without it. It's quite huge, because it uses `nltk`. For
installing it just type `pip install textblob`.

Now you can use simply ```ConcordanceCrawler -h``` to run it and see its options.

## Version

This is version 0.3.0. It's intended for Python >= 2.7 and >= 3.2.

Required libraries will be installed automaticaly.

## Usage

You can use ConcordanceCrawler like a command-line application just as
a Python library. This is a part of ConcordanceCrawler's help message:

```
usage: ConcordanceCrawler [-h] [-n NUMBER_OF_CONCORDANCES] [-m MAX_PER_PAGE]
                          [--disable-english-filter] [-o OUTPUT]
                          [-b {RANDOM,WIKI_ARTICLES,WIKI_TITLES,NUMBERS}]
                          [-f {json}] [-v {0,1,2,3}] [-p {v,a,n,x}]
                          word [word ...]
```
`-n N`, `--number-of-concordances N` is a number of concordances that you
wish a program would crawl. By default it's 10.

`-m M`, `--max-per-page M` is a maximum number of concordances that will be
crawled from one site. They are gotten from top to down. Default is to skip
this option and then this number won't be limited. 

`-o OUTPUT`, `--output OUTPUT` is a name of an output "file". It can be e.g.
`concordances.xml`, `concordances.json` or any other "file" as `/dev/null`.
If a file exists, then it's overwritten, otherwise a new one is created.
Default `OUTPUT` is standard output. 

`-b {RANDOM,WIKI_ARTICLES,WIKI_TITLES,NUMBERS}, --bazword-generator` is a way how
ConcordanceCrawler generates or takes bazwords. It uses them for increasing
a number of links that can be found at Bing.com.

- `RANDOM` -- bazword will be a random four-letter word. This option is
	default.

- `WIKI_ARTICLES` -- from https://en.wikipedia.org/wiki/Special:Random will
	be downloaded random Wikipedia article. Its words will be used as
	bazwords, one word per one searching request.

- `WIKI_TITLES` -- same as previous, but as bazwords will be chosen just
	words from titles.

- `NUMBERS` -- bazwords will be 0, 1, 2, 3, ...

`-f {json}, --format` is an output format, default is json. Format xml will be
operational in later versions.

`-v {0,1,2,3}, --verbosity` is verbosity level, see rest of help message
(`ConcordanceCrawler -h`) for more info.

`-p {v,a,n,x}`, `--part-of-speech {v,a,n,x}` is target word's part of
speech. It can be

- `v` verb

- `a` adjective

- `n` noun

- `x` any part of speech

If you choose `-p` and `v`, `a` or `n`, then ConcordanceCrawler will use
textblob's automatic lemmatizing, you must install it first, otherwise
ConcordanceCrawler terminates.

`word` is the target word in the centre of your interest. You can specify
more of its forms, then all sentences containing at least one of this words
will be crawled. The first word is considered as canonical form and
ConcordanceCrawler will seek this 

### Example

```ConcordanceCrawler hello -n 1 -v 3``` will crawl you one sentence
containing word "hello".

```
[
    {
        "date": "2015-09-07 19:19:26.907794",
        "url": "http://rssjgroup.com/",
        "concordance": "Hello !",
        "keyword": "hello",
				"id": 1
    }
]
```

Here you can see some informations about progress of crawling:
```
ConcordanceCrawler apple -n 1
```

```
2016-03-17 15:42:38,776 STATUS: ConcordanceCrawler version 0.3.0 started, press Ctrl+C for 	interrupt
2016-03-17 15:42:39,418 DETAILS: crawled SERP, parsed 50 links
2016-03-17 15:42:39,418 STATUS: Crawling status 
serp		1 (0 errors) 
links crawled	50 (0 filtered because of format suffix, 0 crawled repeatedly)
pages visited	0 (0 filtered by language filter, 0 errors)
concordances	0 (0 crawled repeatedly)
2016-03-17 15:42:41,060 DETAILS: page https://discussions.apple.com/thread/5524646?start=0&tstart=0 visited, 6 concordances found
2016-03-17 15:42:41,060 STATUS: Crawling status 
serp		1 (0 errors) 
links crawled	50 (0 filtered because of format suffix, 0 crawled repeatedly)
pages visited	1 (0 filtered by language filter, 0 errors)
concordances	1 (0 crawled repeatedly)
[
    {
        "url": "https://discussions.apple.com/thread/5524646?start=0&tstart=0",
        "keyword": "apple",
        "concordance": "Apple may provide or recommend responses as a possible solution based on the information provided; every potential issue may involve several factors not detailed in the conversations captured in an electronic forum and Apple can therefore provide no guarantee as to the efficacy of any proposed solutions on the community forums.",
        "date": "2016-03-17 15:42:41.060341",
        "id": 1
    }
]
```

### Use in your own code

You can also use ConcordanceCrawler as a library in your own project. Then
you would be interested in a subpackage ```core```. There isn't any other
code documentation yet, but will be available later.

## How does ConcordanceCrawler work?

ConcordanceCrawler finds links on Bing.com search engine, visits them and
finds there sentences containing the target word.

There's a little problem, you can find on Bing.com at most first 1000 links
for every keyword, and that's too few. Therefore ConcordanceCrawler lets
finding keywords as for example "sdtn look", "naxe look", "jzmw look" and
similar combinations of bazword and target word. By this approach it gets
sufficient number of different links to crawl concordances.

You can find more informations [here](https://github.com/Gldkslfmsd/concordance-crawler/tree/master/doc), but in Czech.

## Contact me!

I'll be pleased if you contact me. You can send me anything (except a spam
:), a review, a request or idea for other feature, you can report an issue, fix
a bug, and of course ask me a question about anything.

You can contact me via [GitHub](https://github.com/Gldkslfmsd) or email: gldkslfmsd-at-gmail.com.

