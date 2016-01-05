# coding=utf-8

# some samples of languages for testing of detectors

# there are mistakes in comments
# nothing => tools were correct

samples = [

# English
open("table.txt","r").read(),

# Slovak
# cheap nltk: True
u"""Bahrajnské úrady úplne pozastavili letecké spojenie s Iránom.
Toto rozhodnutie bolo prijaté v období eskalácie napätia medzi Iránom
a Saudskou Arábiou, uviedli v utorok svetové agentúry. """,

# Czech
u"""    po celém světě se rozhodli sérií protestů dát najevo, co
si o praktikách této služby myslí. Podnětem byl další případ z loňského
listopadu, kdy norské úřady zabavily pět dětí z norsko-rumunské rodiny
Bodnariových. Jako první se lidé sešli v Os
""",

# Czech without diacritics
u"""    po celem svete se rozhodli serii protestu dat najevo, co
si o praktikach teto sluzby myslí. Podnetem byl dalsi pripad z lonskeho
Jako prvni se lide sesli v Os
""",

# Slovak withoud diacritics
# cheap nltk: True
u"""Pomahat s riesenim migracnej krizy by malo od 1. februara
dalsich 25 slovenskych policajtov.""",

# Czech
u"""by přemítal bůhví o čem . Ten pitomec ! Zklamání 	bylo 	příliš silné
a Maddie zaklela . Okamžitě jí přestal hladit
by""",

# Czech without diacritics
# cheap nltk: True
u"""Jestli budete chtit poslat novou verzi, dejte vedet do konce tydne,
""",

# Old English
# langdetect: [en:0.571426726502, nl:0.428572243193]
# langid: ('la', 0.9999973464287126)
# cheap nltk: False
u"""WILCUME on þā Engliscan Wikipǣdie!

Hēr mōt man findan cȳþþu ymbe manig þing þisse worulde and ofer þisse
worulde, gewriten on þāra ealdena Engliscena 
""",

# Swedish
u"""ge sedan slutet av 1800-talet och sedan 1926 sköts den av staten.
Ansvaret för isbrytningen ligger hos Sjöfartsverket och verksamheten leds
från isbrytarledningen i. Bemanningen av isbrytarna sköttes
kostnaden för den svenska isbr""",

# Dutch
u"""Algebra (van het Arabische woord Al-Gibr dat hereniging, verbinding of
vervollediging betekent) is dat deel van de wiskunde dat zich bezighoudt met
de betrekkingen van door letters en tekens aangeduide grootheden. In de
algebra worden getallen""",

# Latin
# langdetect: [en:0.445075496178, ca:0.326433860401, es:0.228193386635]
# langid: ('la', 0.9999678245910306)

u"""Pinus est genus plantarum florentium in familia Pinacearum, quod circa
115 species, praecipue indigenae hemisphaerae septentrionalis, pinorum
comprehendit.""",

# English from Twitter
"""Dha BEszt You Eva MEet.!(: Off to the stupid shyt I have to go to egh but
bby going with meh:)
No ps wow seriously did he really?""",

# HTML with lots of urls
# langdetect: [en:0.857142128905, ca:0.142857191674]
# langid: ('it', 0.38072174981174967)
# cheap nltk: False
"""<head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object:
http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile:
http://ogp.me/ns/profile#">
<meta charset='utf-8'>
<meta http-equiv="X-UA-Compatible" content="IE=edge">""",

# English
"""Add support for Python 3.5, drop support for Python 2.6, sentiment
analysis package and several corpora, improved POS tagger, Twitter package,
multi-word expression tokenizer, wrapper for Stanford Neural Dependency
Parser, improved translation/alignment module including stack decoder,
skipgram and everygram methods, Multext East Corpus and MTECorpusReader,
minor bugfixes and enhancements For details see:
https://github.com/nltk/nltk/blob/develop/ChangeLoga""",

# Shakespeare's English
"""SHYLOCK
I'll have my bond; speak not against my bond:
I have sworn an oath that I will have my bond.
Thou call'dst me dog before thou hadst a cause;
But, since I am a dog, beware my fangs:""",

]
