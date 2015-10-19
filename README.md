# ConcordanceCrawler

ConcordanceCrawler is a tool for automatic concordance extraction from the
Internet. A concordance is a sentence containing some given word. You can
choose a word in any language, and ConcordanceCrawler is able to download you
hundreds of thousands sentences with the chosen word. 

## Installation

I recommend install ConcordanceCrawler in Python virtual environment (see
https://virtualenv.pypa.io/ ). 

```
virtualenv -p python3 p3
source p3/bin/activate
pip install git+https://github.com/Gldkslfmsd/concordance-crawler.git
```

Now you can use simply ```ConcordanceCrawler -h``` to run it and see its options.

## Version

This is version 1.0. It's intended just for Python 3.4.0. 

Required libraries will be installed automaticaly.

## Usage

You can use ConcordanceCrawler like a command-line application just as
a Python library. This is a part of ConcordanceCrawler's help message:

```
usage: ConcordanceCrawler [-h] [-n N] [-p P] [-o OUTPUT]
                          [-b {RANDOM,WIKI_ARTICLES,WIKI_TITLES,NUMBERS}]
                          [-f {json,xml}] [-v {0,1,2,3}]
                          word
```
`-n N` is a number of concordances that you wish a program would crawl. By default it's 10.

`-p P` is a maximum number of concordances that will be crawled from one site. They are gotten from top to down. Default is to skip this option and then this number won't be limited. 

`-o OUTPUT` is a name of an output "file". It can be e.g. `concordances.xml`, `concordances.json` or any other "file" as `/dev/null`. If a file exists, then it's overwritten, otherwise a new one is created. Default `OUTPUT` is standard output. 

`-b {RANDOM,WIKI_ARTICLES,WIKI_TITLES,NUMBERS}` is a way how ConcordanceCrawler generates or takes bazwords. It uses them for increasing a number of links that can be found at Bing.com.

- `RANDOM` -- bazword will be a random four-letter word. This option is default.

- `WIKI_ARTICLES` -- from https://en.wikipedia.org/wiki/Special:Random will be downloaded random Wikipedia article. Its words will be used as bazwords, one word per one searching request.

- `WIKI_TITLES` -- same as previous, but as bazwords will be chosen just words from titles.

- `NUMBERS` -- bazwords will be 0, 1, 2, 3, ...

`-f {json,xml}` is an output format, default is json

`-v {0,1,2,3}` is verbosity level, see rest of help message (`ConcordanceCrawler -h`) for more info.

`word` is the target word in the centre of your interest.

### Example

```ConcordanceCrawler hello -n 1 -v 3``` will crawl you one sentence
containing word "hello".

```
[
    {
        "date": "2015-09-07 19:19:26.907794",
        "url": "http://rssjgroup.com/",
        "concordance": "Hello !",
        "keyword": "hello"
    }
]
```

Here you can see some informations about progress of crawling:
```
ConcordanceCrawler apple -n 1
```

```
2015-09-07 20:33:37,175 STATUS: ConcordanceCrawler started, press Ctrl+C for interrupt
2015-09-07 20:33:38,068 DETAILS: crawled SERP, parsed 50 links
2015-09-07 20:33:38,354 DETAILS: page http://www.windowsphone.com/en-us/how-to/wp8/cortana/meet-cortana visited, 0 concordances found
2015-09-07 20:33:40,491 DETAILS: page http://www.yelp.com/biz/best-buy-libertyville visited, 4 concordances found
2015-09-07 20:33:40,491 STATUS: Crawling status 
	serp		1 (0 errors) 
	pages visited	2	(2 unique pages, 0 errors)
	concordances	1
[
    {
        "url": "http://www.yelp.com/biz/best-buy-libertyville",
        "concordance": " They killed my Apple computer.",
        "keyword": "apple",
        "date": "2015-09-07 20:33:40.490945"
    }
]
```

Xml output looks like this:
```
<root>
<item>
    <concordance>One Bright Red Apple Isolated on White with Slight Shadow - 24"H x 16"W - Peel and Stick Wall Decal by Wallmonkeys
    </concordance>
    <date>2015-09-07 20:39:48.028556</date>
    <keyword>apple</keyword>
    <url>http://www.amazon.com/Isolated-Wall-Sticker-Wallmonkeys-Decals/dp/B005M9PVNU</url>
</item>
</root>
```
### Use in your own code

You can also use ConcordanceCrawler as a library in your own project. Then
you would be interested in this submodules: links, parse, visitor, urlrequest and
bazwords. Others are used just by the demo command-line application. All
code should be self-explanatory, there isn't any other code documentation.

## How does ConcordanceCrawler work?

ConcordanceCrawler finds links on Bing.com search engine, visits them and
finds there the sentences containing the target word.

There's a little problem, you can find on Bing.com at most first 1000 links
for every keyword, and that's too few. Therefore ConcordanceCrawler lets
finding keywords as for example "sdtn look", "naxe look", "jzmw look" and
similar combinations of bazword and target word. By this approach it
gets sufficient number of different links to crawl
concordances.

You can find more informations [here](https://github.com/Gldkslfmsd/concordance-crawler/tree/master/doc), but in Czech.

## Future plans with ConcordanceCrawler

This is the first version of ConcordanceCrawler, but other versions are also
planned. In plan is that ConcordanceCrawler will be able to extract
sentences with more accuracy (this version detects words just in one form,
e.g. -ing forms of verbs are ignored). At least it will also detect language
of sentence and encoding of document.

It will be published on [Cheeseshop](https://pypi.python.org/pypi) under open-source license and there
will exist a web-page with demo application. This could be finished until June 2016.

## Contact me!

I'll be pleased if you contact me. You can send me anything (except a spam
:), a review, a request or idea for other feature, you can report an issue, fix
a bug, and of course ask me a question about anything.

You can contact me via [GitHub](https://github.com/Gldkslfmsd) or email: gldkslfmsd-at-gmail.com.

