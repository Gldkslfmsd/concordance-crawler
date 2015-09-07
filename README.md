# ConcordanceCrawler

ConcordanceCrawler is a tool for automatic concordance extraction from the Internet. A concordance is a sentence containing some given word. You can choose a word in any language, and ConcordanceCrawler will download you hundreds of thousands sentences with the chosen word. 

## Installation

How to install ConcordanceCrawler as a command-line application and Python3
module?

```
git clone https://github.com/Gldkslfmsd/concordance-crawler.git
cd concordance-crawler
virtualenv -p python3 p3
source p3/bin/activate
python3 setup.py install
```

Now you can use simply ```ConcordanceCrawler -h``` to see its options.

## Usage

You can use ConcordanceCrawler like a command-line application just as a . This is a part of ConcordanceCrawler's help message:

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

## How does it work?

ConcordanceCrawler finds links on Bing.com search engine, visits them and finds there the sentences containing the target word.

There's a little problem, you can find on Bing.com at most first 1000 links for every keyword, and that's too few. Therefore ConcordanceCrawler lets finding keywords as for example "sdtn look", "naxe look", "jzmw look" and similar combinations of bazword and target word. By this approach it (should) get sufficient number of (idealy) different links to crawl concordances.

```
    {
        "date": "2015-09-07 19:19:26.907794",
        "url": "http://rssjgroup.com/",
        "concordance": "Hello !",
        "keyword": "hello"
    }
```


