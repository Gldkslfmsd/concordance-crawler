# ConcordanceCrawler

[![Build Status](https://travis-ci.org/Gldkslfmsd/concordance-crawler.svg?branch=master)](https://travis-ci.org/Gldkslfmsd/concordance-crawler)

ConcordanceCrawler is a tool for automatic concordance extraction from the
Internet. A concordance is a sentence containing some given word. Take an
English word, and ConcordanceCrawler will be able to download you hundreds
thousands of sentences with your word. 

ConcordanceCrawler is a console application whose main purpose is
crawling of English verbs or other words, but you can also use its API. It allows you to
adapt ConcordanceCrawler to any other language. 

## Try web demo!

Will be launched soon.

## Installation

I recommend ConcordanceCrawler installation in Python virtual environment (see
https://virtualenv.pypa.io/ ). All dependent libraries will be installed automaticaly except one.
The only nontrivial dependency is `lxml`, you must install it globaly with root permissions. On the other hand it's needed 
for fast parsing. Install `lxml` by following command (if you use Python 3) or follow instructions on its [homepage](http://lxml.de/installation.html):

```
sudo apt-get install python3-lxml
```

If you have working `lxml` library, you can create your new Python virtual environment with access to the global `lxml` installation, and then install ConcordanceCrawler there.
For Python3:

```
virtualenv -p python3 p3 --system-site-packages
source p3/bin/activate
pip install git+https://github.com/Gldkslfmsd/concordance-crawler.git
```

(For Python2 just substitute 3 for 2.)

If you want to use also automatic conjugating of English verbs (or
inflecting of nouns or comparing of adjectives), then install also
`textblob` library, but it's not necessary, you can use ConcordanceCrawler
pretty well without it. It's quite huge, because it uses `nltk`. For
installing it just type `pip install textblob` and `python -m textblob.download_corpora`.

Now you can use simply ```ConcordanceCrawler -h``` to run it and see its options.

## Python versions

ConcordanceCrawler works with Python2 >= 2.7 and with Python3 >= 3.2.

Unfortunately you cannot use `textblob` together with Python3.2, so you
cannot use automatic morphological analysis with this Python version. However all
other features work well.

## Usage

You can use ConcordanceCrawler like a command-line application just as
a Python library. This is a part of ConcordanceCrawler's help message summarizing
all your options:

```
usage: ConcordanceCrawler [-h] [-n NUMBER_OF_CONCORDANCES] [-m MAX_PER_PAGE]
                          [--disable-english-filter] [-o OUTPUT]
                          [-b {RANDOM,WIKI_ARTICLES,WIKI_TITLES,NUMBERS}]
                          [-f {json,xml}] [-v {0,1,2,3}] [-p PART_OF_SPEECH]
                          [-e ENCODING] [--backup-off]
                          [--backup-file BACKUP_FILE]
                          [--extend-corpus EXTEND_CORPUS]
                          [--continue-from-backup CONTINUE_FROM_BACKUP]
                          [word [word ...]]
```

### Brand-new crawling job

ConcordanceCrawler allows you to create a brand-new crawling job or continue crawling
with an old job which was unexpectedly interrupted before finishing.

During creating a new job you may want to use following options:

`word [word ...]` is the target word in the centre of your interest. You can specify
more of its forms, then all sentences containing at least one of this words
will be crawled. The first word is considered as canonical form and
ConcordanceCrawler will use it for seeking links on a search engine.

`-p REGEX`, `--part-of-speech REGEX` is target word's part-of-speech tag
regex, they're values are adopted from Penn Treebank II tagset. See 
http://www.clips.ua.ac.be/pages/mbsp-tags for detailed description.

Default value for this option is `.*`, it means any arbitrary
part-of-speech.  If you select other regex (e.g.  `V.*` for verbs, `N.*` for
nouns, `J.*` for adjectives), then a `textblob` library will be used.  Size
of this library is not neglible, because it uses `nltk`, therefore it's not
an integral part of ConcordanceCrawler.  You must install it manually, if you
wish.  Instead of it you can omit this option, decline your target word
manually and use all its forms as additional values for `word` argument.

*Example usage:* assume that target word is `fly` and given regex is
`V.*`, it means we want to crawl only verbs. Then a word `flies` (tagged
`VBS`) matches, as well as `flew` whose tag is `VBD`.  On the other hand an
insect `fly` with tag `NN` doesn't match, so sentences with this word will
be ignored.  




`-n N`, `--number-of-concordances N` is a number of concordances that you
wish a program would crawl. By default it's 10.

`-m M`, `--max-per-page M` is a maximum number of concordances that will be
crawled from one site. They are gotten from top to down. Default is to skip
this option and then this number won't be limited. 

`--disable-english-filter` option disables filtering of Non-English sentences from
concordances. By default it's enabled. This option affects quality of resulting corpus.

`-e ENCODING, --encoding ENCODING`. If not given,
documents without respect to their encoding will be
crawled. If you select ASCII as encoding, all concordances containing
any non-ASCII character will be ignored.
If you select any other charset, e.g. utf-8, all documents without
this charset specification in http header or in html
metatag will be ignored (as well as documents with
unequal charset values in http header and in metatag).
This option has an impact on quality of corpus and speed of crawling.



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


`-o OUTPUT`, `--output OUTPUT` is a name of an output "file". It can be e.g.
`concordances.xml`, `concordances.json` or any other "file" as `/dev/null`.
If a file exists, then it's overwritten, otherwise a new one is created.
Default `OUTPUT` is standard output. 


`-f {json, xml}, --format` is an output format, default is json.

`-v {0,1,2,3}, --verbosity` is verbosity level, see rest of help message
(`ConcordanceCrawler -h`) for more info.

`--buffer-size BUFFER_SIZE` -- setup maximal number of items in memory buffers which
                        are used to prevent repeated visit of the same url and
                        repeated crawling of the same concordance. Default
                        value is 1000000. Selecting of too big number can lead
                        to out of memory error (but this should happen only
                        after a very long time). Selecting of small number can
                        lead to repeated visit of same url or repeated
                        crawling of the same concordance, because the buffers
                        are like queues, when they are full they delete the
                        old values to save the new ones.


`--backup-file BACKUP_FILE` -- name for backup file. This backup file allows you to
continue aborted crawling job and extend corpus.
Default name is `ConcordanceCrawler.backup` and is created in working directory.

`--backup-off` -- don't create a backup file

### Restarting of crawling job

If you want to restart a crawling job that was interrupted earlier, you must 
start ConcordanceCrawler with this 2 options:

`--extend-corpus EXTEND_CORPUS` -- an output file created in previous crawling job which will
be extended now.

`--continue-from-backup CONTINUE_FROM_BACKUP` -- backup file

## Examples

```ConcordanceCrawler hello -n 1 -v 3``` will crawl you one sentence
containing word "hello".

```
[
    {
        "start": 0,
        "keyword": "hello",
        "end": 5,
        "url": "http://grokbase.com/t/mysql/maxdb/0469p5zksn/error-in-complete-backup",
        "date": "2016-04-30 14:45:01.220790",
        "concordance": "Hello Marco,you can find the output and error output of TSM's adint2 in the files dbm.ebp and dbm.ebl.",
        "id": 1
    }
]
```

Here you can see some informations about progress of crawling. We ordered one sentence with a verb *think*.

```
 ConcordanceCrawler think -p 'V.*' -n 1
```

```
2016-04-30 14:52:53,220 STATUS: ConcordanceCrawler version 1.0.0 started, press Ctrl+C for 	interrupt
2016-04-30 14:52:53,811 DETAILS: crawled SERP, parsed 50 links
2016-04-30 14:52:53,812 STATUS: Crawling status 
serp		1 (0 errors) 
links crawled	50 (0 filtered because of format suffix, 0 crawled repeatedly)
pages visited	0 (0 filtered by encoding filter, 0 filtered by language filter, 0 errors)
concordances	0 (0 crawled repeatedly)
2016-04-30 14:53:04,387 ERROR: 'HTTPConnectionPool(host='spknclothing.com', port=80): Read timed out. (read timeout=10)' occured during getting http://spknclothing.com/about/
2016-04-30 14:53:09,411 DETAILS: page http://spknclothing.com/ visited, 1 concordances found
2016-04-30 14:53:09,411 STATUS: Crawling status 
serp		1 (0 errors) 
links crawled	50 (0 filtered because of format suffix, 0 crawled repeatedly)
pages visited	1 (0 filtered by encoding filter, 0 filtered by language filter, 1 errors)
concordances	0 (0 crawled repeatedly)
2016-04-30 14:53:09,411 STATUS: Crawling status 
serp		1 (0 errors) 
links crawled	50 (0 filtered because of format suffix, 0 crawled repeatedly)
pages visited	1 (0 filtered by encoding filter, 0 filtered by language filter, 1 errors)
concordances	1 (0 crawled repeatedly)
[
    {
        "date": "2016-04-30 14:53:09.411287",
        "concordance": "not everyone thinks about BMX when they think of Maine but these guys have a great scene…",
        "url": "http://spknclothing.com/",
        "id": 1,
        "keyword": "think",
        "end": 19,
        "start": 13
    }
]
```

Without `textblob` installation we could get the same input by this command:

```
ConcordanceCrawler think thinks thinking thought -n 1
```

## Customize ConcordanceCrawler!

You can also use ConcordanceCrawler as a library in your own project. Then you can for example
adapt it for your own language, improve or customize its functions or do anything else.

Check this [documentation](https://github.com/Gldkslfmsd/concordance-crawler/wiki/Customizing-ConcordanceCrawler) 
and [example](https://github.com/Gldkslfmsd/concordance-crawler/blob/master/examples/czech_concordance_crawler.py).

## How does ConcordanceCrawler work?

ConcordanceCrawler finds links on Bing.com search engine, visits them and
finds there sentences containing the target word.

There's a little problem, you can find on Bing.com at most first 1000 links
for every keyword, and that's too few. Therefore ConcordanceCrawler lets
finding keywords as for example "sdtn look", "naxe look", "jzmw look" and
similar combinations of bazword and target word. By this approach it gets
sufficient number of different links to crawl concordances.

## Contact me!

I'll be pleased if you contact me. You can send me anything (except a spam
:), a review, a request or idea for other feature, you can report an issue, fix
a bug, and of course ask me a question about anything.

You can contact me via [GitHub](https://github.com/Gldkslfmsd) or email: gldkslfmsd-at-gmail.com.

