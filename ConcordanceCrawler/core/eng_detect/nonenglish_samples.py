# -*- coding: utf-8 -*-
samples = [

"""Na počátku bylo Slovo, to Slovo bylo u Boha, to Slovo bylo Bůh.
To bylo na počátku u Boha.
Všechno povstalo skrze ně a bez něho nepovstalo nic, co jest. 
""",


# http://www.lidovky.cz/zemrel-svetoznamy-spisovatel-umberto-eco-autorovi-romanu-jmeno-ruze-bylo-84-let-gfn-/lide.aspx?c=A160220_013646_lide_gib
"""Ve věku 84 let zemřel italský spisovatel Umberto Eco. O jeho pátečním
úmrtí informovala italská média s odvoláním na spisovatelovu rodinu. Eco se
proslavil hned svým prvním románem Jméno růže, podle kterého byl později
natočen známý film se Seanem Connerym v hlavní roli.
""",

"""    Režisér Annaud Eca označil za svého „nejbližšího přítele“. „Umberto
byl člověk, jehož jsem velmi obdivoval a s nímž jsem sdílel radost ze
života. Byl to neobyčejně vzdělaný muž milující veselý život. Bavil se vším,
byl plný radosti. Byl směsicí vědce a člověka, který se uměl smát a dobře
jíst. Měl mimořádnou paměť, všechno si pamatoval. Přečetl si stránku a pak
vám ji bez chyby přeříkal. Byl také politicky angažovaný, hrozně naštvaný na
(bývalého italského premiéra) Silvia Berlusconiho,“ řekl Annaud v rozhovoru
s rozhlasovou stanicí France Info. Eco se v prosinci rozešel
s vydavatelstvím Bompiani, když je koupil dům Berlusconiho vydavatelský dům
Mondadori. Levicově orientovaný Eco podle italského tisku odmítal představu,
že by jeho dílo mohl vydávat Berlusconi.

    Eco, který proslul nejen jako spisovatel, ale také jako filozof
		a jazykovědec, zemřel ve svém domově v pátek kolem 22:30 SEČ, oznámila
		rodina. Spisovatel dlouhou dobu bojoval s rakovinou, uvedla agentura
		AFP.
""",

# KSP
"""
 Začínající programátoři se velmi často potýkají s tím, jak by měli do svého
 programu dostat vstup a jak ho zpracovat. V tomto článku a v sesterském
 článku o jazyce C se vám s tím pokusíme pomoci. Úvodní kapitolu mají oba
 články stejnou, ale poté se již každý zabývá svým jazykem.
 Klávesnice versus soubory

 Nejjednodušší je ve většině jazyků načítat vstup od uživatele. To je dobré
 pro rychlé testování nebo pro programy přijímající jenom jednu vstupní
 hodnotu. Ale co když program přijímá na vstupu více hodnot?

 Jedna možnost je změnit jeho vnitřnosti tak, aby místo toho načítal vstup
 ze souboru. Ale nejrychlejší většinou bývá zachovat program tak, jak je,
 a jen mu místo vstupu z klávesnice předhodit soubor.

 Programu totiž většinou neví o klávesnici nic, má jen věc, které se říká
 standardní vstup. Ten je většinou představovaný klávesnicí (obdobně je pak
 standardní výstup většinou představovaný vypisováním na terminál), ale dá
 se jednoduše přesměrovat.

 Jak na to? Představme si, že máme nějaký svůj program (spustitelný
 zkompilovaný program v C nebo skript v Pythonu) a soubor 1.in, který mu
 chceme předhodit na vstupu. V příkazové řádce všech hlavních operačních
 systémů (Linux a obecně všechny UNIXy, Windows) to uděláme pomocí operátoru
 přesměrování ve tvaru menšítka (<):

 ./program < 1.in           -- UNIXový svět
 program.exe < 1.in         -- Windows
 python3 program.py < 1.in  -- oboje

 (Pozor: V UNIXovém světě se při spuštění programu z aktuálního adresáře
 musí explicitně uvést adresář tečka jako odkaz na aktuální umístění.)

 Stejným způsobem pak lze přesměrovat i výstup, jen s použitím šipky na
 druhou stranu (většítka). Pokdu tedy budete řešit třeba opendatové úlohy
 v KSP a budete mít program v Pythonu 3, může celý příkaz vypadat jako:

 python3 program.py < 1.in > 1.out

 Zpracování standardního vstupu

 Úvodem varujeme, že se při načítání vstupu liší chování Pythonu 2 a Pythonu
 3. Hlavně v tom, že ve starší verzi se funkce input() pokoušela vyhodnotit
 vstup jako Pythoní výraz, kdežto v nové verzi se vstup načte jednoduše jen
 jako string (to ve starší verzi šlo pomocí raw_input()) a zpracování je pak
 plně v naší režii.

 Již zmíněná funkce input() načte celý řádek jako string. Pokud například
 vstup obsahuje dvě čísla, každé na novém řádku, můžeme je načíst jako
 stringy a převést na číselnou hodnotu takto:

 a = int(input())
 b = int(input())

 O trochu složitější situace nastává, když jsou čísla na stejném řádku
 oddělená jen mezerou. V tuto chvíli se nám velmi hodí funkce .split(),
 která rozdělí řetězec podle bílých znaků (nebo podle jiného oddělovače,
 pokud jí ho předáme jako parametr) a vrátí ho jako seznam stringů. Příklad
 výše by se tedy dal převést na:

 pole = input().split()
 a = int(pole[0])
 b = int(pole[1])

 Všimněte si, že tady musíme dělat trochu neohrabanou konstrukci kvůli tomu,
 že .split() nám vrátí seznam stringů. U dvou čísel to ještě nevadí, ale
 představte si to třeba pro vstup o délce deset nebo třeba tisíc prvků. Dalo
 by se to vyřešit nějakým cyklem, ale existuje jedna velmi pěkná syntaktická
 zkratka.

 Tou je velmi mocná funkce map(), která v jednoduchosti dovoluje spustit
 zvolenou funkci na všechny prvky seznamu. Nevrací ale bohužel čistý seznam,
 což ale jednoduše můžeme vyřešit ještě zabalením do převodní funkce list().
 Celá konstrukce pak může vypadat takto:

 pole = list(map(int, input().split()))

 Hodí se pro zpracování rozumně velkých řádků (řekněme v jednotkách až
 desítkách megabajtů), pro větší řádky raději zvolte přístup přes skutečnou
 práci se soubory. Stejně tak pokud předem nevíte, kolik chcete načíst řádek
 a chcete skončit až ve chvíli, kdy dojdete na konec vstupu, je lepší použít
 souborové funkce.
 Vypisování

 Náplní článku je sice hlavně načítání vstupů, ale zmíníme se krátce
 i o vypisování. Základem všeho je v Pythonu 3 funkce print() (jako varování
 dodáme, že v Pythonu 2 to nebyla funkce, ale příkaz, a ještě k tomu
 s odlišnou syntaxí).

 Této funkci je možné předat skoro jakýkoliv objekt Pythonu a ona ho vypíše
 a odřádkuje. Pokud ji předáme více parametrů, vypíše je všechny oddělené
 jednou mezerou a teprve poté odřádkuje:

 print(1)    # vypíše: 1
 a = 7.6
 print(a, 1) # vypíše: 7.6 1

 Ilustrace: Procesor

 Ale počkat, co když chci vypisovat bez odřádkování, třeba když mám nějaké
 pole a chci ho v cyklu vypsat? Na to existuje řešení, funkci print() se
 totiž dá předefinovat koncový znak (defaultně odřádkování) i oddělovač
 (defaultně mezera) a to pomocí pojmenovaných parametrů.

 Následující konstrukce vypíše každý prvek z pole a jeho dvojnásobek
 oddělené dvojtečkou a tyto dvojice oddělené tabulátorem:

 for prvek in seznam:
	 	print(prvek, prvek*2, sep=":", end="\t")

		Příkaz výše má jediný problém a to, že i po poslední dvojici se vypíše
		tabulátor. To se sice dá obejít nějakými podmínkami, ale existuje
		elegantnější varianta pomocí funkce .join(). Ta dostane jako parametr
		seznam stringů, které má spojit, a spojí je pomocí stringu, na kterém je
		volána. Nejlépe to ukáže příklad:

		seznam = ["1", "2", "3"]
		s = ":".join(seznam)
# Vrátí "1:2:3"

		Ale co když budeme chtít .join() předat seznam čísel? Pak opět přichází
		na scénu naše známá funkce map(), kterou všechna čísla převedeme na
		stringy:

		seznam = [1, 2, 3]
		s = ":".join(map(str, seznam))
# Vrátí "1:2:3"

		Čtení ze souborů

		Python má pro přístup k souborům odlišnou syntaxi, než pro standardní
		vstup, ale spousta principů zmíněných výše se dá aplikovat i zde.
		Nejdříve je nutné soubor otevřít voláním funkce open(), která nám vrátí
		odkaz na soubor. Po skončení práce se souborem ho zavřeme voláním
		.close() na něm samotném.

		Té předáme jako první parametr cestu k souboru a jako druhý parametr
		volitelně mód otevření (bez uvedení otevře soubor ke čtení). Parametr
		r otevírá jen pro čtení, parametr w pak pro zápis a parametr a pro
		přidávání na konec.

		vstup = open("1.in", "r")
# nějaká práce se souborem
		vstup.close()

		Další příkazy se ale volají již přímo na objektu vstup (zde se pěkně
		projevuje objektový přístup Pythonu). Dá se voláním .readline() načíst
		celá jedna řádka ze souboru (a dále s ní pracovat jako při použití
		input()), nebo se dá pomocí .read() načítat vstup po znacích:

		vstup = open("1.in", "r")
		slova = vstup.readline().split()
		pismeno = vstup.read()
		vstup.close()

		Při volání .read(10) si ještě číslem můžeme říct, že chceme načíst více
		bytů najednou. Při vypisování pak můžete použít funkci .write(). Ta ale
		narozdíl od print() nepřidává na konec automaticky znak nového řádku
		a je potřeba ho přidat ručně, pokud ho chceme:

		vystup = open("1.out", "w")
		vystup.write("bagr\n")
		vystup.close()

		Dodejme ještě, že příkazy pro práci se soubory lze použít i pro práci se
		standardním vstupem a výstupem. Stačí importovat modul sys a pak je
		možné místo objektu reprezentujícího vstup a výstup použít sys.stdin
		a sys.stdout:

		import sys;
		radek = sys.stdin.readline()
		sys.stdout.write("bagr\n")

		Pěkná syntaktická perlička, kterou vám závěrem ukážeme, je jak jednoduše
		zpracovat v Pythonu celý soubor, dokud nedojdete na jeho konec:

		vstup = open("1.in", "r")
		for radek in vstup:
			    # dělej něco
					vstup.close()

					Doufáme, že pro vás návod byl alespoň trochu užitečný a že i díky
					němu porozumíte Pythonu o trochu více.
					Článek pro vás sepsal

					Jirka Setnička
""",

# German wikipedia
"""
Das Teatro Argentina, eines der ältesten Theater in Rom, wurde am 31. Januar
1732 mit der Oper Berenice von Domenico Sarro eingeweiht. Am 20. Februar
1816 fand hier die Uraufführung des Barbiers von Sevilla von Rossini statt.
Die Premiere war zwar ein Fiasko, doch in den folgenden Aufführungen wurde
die Oper zu einem immer größeren Erfolg. Auch einige Opern von Saverio
Mercadante und Giuseppe Verdis Oper I due Foscari wurden hier uraufgeführt.

Heute dient das Teatro Argentina als Sprechtheater sowie zur Aufführung von
Opern und Sinfonien. Das Innere des Hauses beherbergt ein historisches
Theatermuseum (Museo Storico del Teatro) mit einem Bilder- und
Dokumentenarchiv.""",

# Slovak wikipedia
"""
Bathory je slovensko-česko-maďarsko-britský koprodukčný film režiséra Juraja
Jakubiska. Nakrúcanie filmu sa začalo v decembri 2005 a film bol uvedený
v júli 2008. Je to prvý film Juraja Jakubiska v angličtine.

Film je založený na príbehu Alžbety Bátoriovej, uhorskej šľachtičnej 16.
a 17. storočia, odohrávajúci sa na území Horného Uhorska, dnešnom Slovensku.
Alžbeta Bátoriová bola známa tým, že zavraždila mnoho mladých dievčat.

Réžia: Juraj Jakubisko
Scenár: Juraj Jakubisko
Hrajú: Anna Friel, Vincent Regan, Hans Matheson, Karel Roden,
Franco Nero, Deana Jakubisková-Horváthová, Bolek Polívka, Jiří
Mádl, Lucie Vondráčková
Rozpočet: cca 400 mil. slovenských korún

Obsadenie

Na konci januára 2006 bola vyhlásená ako predstaviteľka Báthoriovej
holandská herečka Famke Janssen a do médií sa dostali jej fotky
s Jakubiskom. Jej prvé účinkovanie bolo naplánované na 6. marca 2006.
Zatiaľ boli nakrúcané iné časti filmu (v ktorých neúčinkovala).  Okolo 8.
marca 2006 vyhlásili tlačové agentúry, že Janssenovú nahradila anglická
herečka Anna Friel.  Hrajú v hlavných úlohách
""",

"""Fekvése

Magyarkeszi Tolna megye északnyugati, a Somogy-Tolnai dombság északi részén,
3 megye találkozásánál (Tolna, Somogy, Fejér) fekszik. Területének nagysága
3185 ha, ebből a belterület 356 ha.

A Tita-patak völgyében meghúzódó községet a 65-ös főútról az Iregszemcsénél
leágazó mellékúton Nagyszokolyon keresztül érhetjük el. Fejér megye felől
Felsőnyéken át vezet ide az út. Viszonylag jól járható földúton Ozora felől
(Fürgeden át) is megközelíthető a falu. Legközelebbi város a 20 km-re lévő
Tamási, de Siófoktól - így a Balatontól is - mindössze 35 km távolságra van.
Története

1703-ig Kesze vagy Keszi volt a hely elnevezése. A török hódoltság után
elpusztult települést I. Lipót király az Esterházy családnak adományozta,
akik felvidékről telepítettek ide új lakókat, s a helység neve ekkor
Kesziről Tótkeszire változott, s csak 1903-tól viseli mai nevét,
Magyarkeszit.

A hely már a kőkorszakban is lakott volt. A honfoglalás után a gutkeled
nemzetség vette birtokba. Egyházi dokumentumok alapján 1274-ben temploma és
plébániája volt, mely a török uralom alatt elpusztult. Az 1514-es Dózsa
György-féle parasztfelkelés idejére a falu lakossága elérte a hatszáz főt.
Az 1526-os mohácsi vész után az akkor 500 lelket számláló falu lakosságát
a török rabláncra fűzte és az időseket elpusztította. Akik életben maradtak,
a környék erdeiben elbujdostak. Hazafias tetteikért I. Lipót magyar király
(1640-1705) e területeket az Esterházy családnak adományozta, ők voltak
a legjelentősebb telepítők.

Az Osztrák–Magyar Monarchia idején is említik Tótkeszit, mint a megye
- dombóvári járás néven ismert - nyugati részén található 30 jelentősebb
	község egyikét. A forrás ekként emlékezik meg a környékről: "Ez a föld
	a somogyival egyező, s mint mondva volt, alacsony hegyekkel ritkásan
	szegdelt hullámos domborzatú, gazdagon termő mezőség. Népe egészen magyar;
	s mint a föld, úgy a nép is a somogyival alkatban, színben, viseletben,
	szójárásban, életfoglalkozásban, erkölcsben rokon; erős, dolgos, kitartó,
	barátkozó, ingerlékeny, makacs s a végletekben szilaj." (Forrás: Az
	Osztrák–Magyar Monarchia Irásban és Képben; Arcanum, 2001)
""", 

# Dutch
"""Klimaatbuffer

Een klimaatbuffer is een gebied waar niets aan veranderd mag worden, zodat
de natuur haar gang kan gaan. Zo kan men zien hoe het klimaat verandert en
zich aanpast.

Een voorbeeld van een kustgebied is het waddengebied. Dit is een gebied dat
nooit is veranderd door de mens; planten en dieren kunnen er gewoon hun gang
gaan. Er broeden bijvoorbeeld heel veel vogels en er groeien bijzondere
planten.

Een ander voorbeeld van een klimaatbuffer langs een rivier is de monding
Steenbergse Vliet. Het gebied bestaat vooral uit moerassen. Doordat het
gebied vaak onderloopt, kunnen er ook bijzondere planten groeien.
""",

# Dutch
"""Als schrijver brak Eco in 1980 internationaal door met zijn roman Il Nome
della Rosa (De naam van de roos), een spannende detectiveroman die zich in
1327 afspeelt in het kader van de strijd tussen het centrale gezag van de
Rooms-katholieke Kerk en verschillende stromingen daarin die met geweld
werden onderdrukt. De historische achtergrond wordt uitgebreid geschetst.
Het boek ademt het ritme van het kloosterleven en de hoofdstukken zijn
ingedeeld naar de gebedstijden binnen de kloostermuren.

Een tweede roman, De slinger van Foucault, speelt zich af in het heden, maar
gaat vooral over de erfenis van de tempeliers en de rozenkruisers,
laat-middeleeuwse mystieke bewegingen.

Daarnaast zijn van Eco nog een aantal bundels met essays verschenen en drie
romans: Het eiland van de vorige dag (1995), Baudolino (2001) en De
mysterieuze vlam van koningin Loana (2005). In 2001 schreef hij samen met de
gepensioneerde aartsbisschop van Milaan, Carlo Maria Martini het boek
Geloven of niet geloven: een confrontatie.

Eco stond tevens te boek als een autoriteit op het gebied van James Bond.[2]
Hij kreeg in 1998 de exclusieve Duitse onderscheiding "Pour le Mérite". Eco
is tevens schrijver van kinderboeken.

In 2012 ontving hij de Vrede van Nijmegen Penning.""",

# Finnish
"""The Beatles on popmusiikin keskeisimpiä yhtyeitä. Yhtyeessä ilmeni
ensimmäistä kertaa rock- ja popyhtyeiden merkittävimmät osatekijät
samanaikaisesti. Yhtyeen jäsenet sävelsivät musiikkia itse ja myös esittivät
sekä studiossa että lavalla. Beatles vakiinnutti The Shadowsin ohella
peruskokoonpanon kaksi kitaraa, basso ja rummut. Yhtyeessä ei ollut
perinteistä tähtisolistia, vaan yhtyettä seurattiin kokonaisuutena vaikkakin
eri jäsenillä oli ihailijoita. Yhtye hyötyi tehokkaasta tiedonvälityksestä,
ja oheistuotteet olivat merkittävä osa ihailijakulttuuria. Manageri Brian
Epstein loi yhtyeelle tietoisen ulkoisen tyylin ja julkisuuskuvan, muttei
puuttunut musiikkiin. Beatlesilla oli suuri vaikutus siihen, että muusikot
alkoivat enemmän itse tehdä musiikkiaan ja että pop-musiikkia alettiin pitää
omana taiteen lajina.

The Beatles aloitti levytysuransa lauluharmonioiden leimaamalla
popmusiikilla esittäen albumeilla sekä omia lauluja että cover-versioita.
Yhtye kehittyi ja uudistui musiikillisesti sekä studioteknisesti. Vuoteen
1967 mennessä yhtye oli siirtynyt pääasiassa psykedeelisen rockiin ja
kokeellisempiin sovituksiin, joissa hyödynnettiin studiotekniikan kehitystä.
Kuitenkin myös tuolloin melodisuus säilyi kappaleiden ollessa yksittäisiä
esityksiä. Psykedeelisen kauden jälkeen yhtye pyrki palaamaan
studioteknisesti karsitumpaan ilmaisuun.

The Beatles on säilyttänyt suuren suosionsa myös vuonna 1970 tapahtuneen
hajoamisensa jälkeen, ja sen levytyksistä on otettu uusintapainoksia ja
niitä on siirretty uusiin formaatteihin. Beatlesin nousua suursuosiota on
musiikin ohella selitetty yhteiskunnan muutoksilla, joita olivat esimerkiksi
1960-luvun voimakas taloudellinen kasvu, suurten ikäluokkien muodostama uusi
teini- ja nuorisoyleisö ja sen parempi taloudellinen asema.
""",

# Portugese
"""Palmira (em aramaico: ܬܕܡܘܪܬܐ‎; transl.: Tedmurtā; em árabe:
تدمر‎; transl.: Tadmor) foi uma antiga cidade semita, situada num oásis
perto da atual cidade de Tadmor, na província de Homs, no centro da Síria,
215 km a nordeste da capital síria, Damasco. Fundada durante o Neolítico,
a cidade foi documentada pela primeira vez no início do segundo milénio a.C.
como uma paragem de caravanas que atravessavam o deserto Sírio. A cidade
aparece nos anais dos reis assírios e é possível que seja mencionada na
Bíblia hebraica. Foi incorporada no Império Selêucida (séculos IV a.C.–I
d.C.) e posteriormente no Império Romano, sob o qual prosperou.

A localização estratégica da cidade, aproximadamente a meio caminho entre
o mar Mediterrâneo e o rio Eufrates, fez dela num ponto de paragem
obrigatório para muitas das caravanas que percorriam importantes rotas
comerciais, nomeadamente a Rota da Seda. A riqueza da cidade possibilitou
a edificação de estruturas monumentais. No século III d.C., Palmira era uma
metrópole próspera e um centro regional, com um exército suficientemente
poderoso para derrotar o Império Sassânida em 260, durante o reinado de
Odenato, que foi assassinado em 267. Odenato foi sucedido pelos seus jovens
filhos, sob a regência da rainha Zenóbia, que começou a invadir as
províncias romanas orientais em 270. Os governantes palmirenses adotaram
títulos imperiais em 271. O imperador romano Aureliano derrotou a cidade em
272 e destruiu-a em 273, na sequência de uma segunda rebelião fracassada.
Palmira foi um centro de menor importância durante os períodos bizantino,
Rashidun, omíada, abássida e mameluco e os seus vassalos. Os Timúridas
destruíram-na em 1440 e a partir ficou reduzida a uma pequena aldeia, que
pertenceu ao Império Otomano até 1918, depois ao Reino da Síria e ao Mandato
Francês da Síria. O local da antiga cidade foi definitivamente abandonado em
1932, quando os últimos habitantes foram transferidos para a nova aldeia de
Tadmur. As escavações sistemáticas e em larga escala das ruínas foram
iniciadas em 1929. Em """,

# Chinese?
"""
第80届奥斯卡颁奖典礼是美国电影艺术与科学学院旨在奖励2007年最优秀电影的一场晚会，于太平洋时区2008年2月24日下午17点30分（北美东部时区晚上20点30分）在美国加利福尼亚州洛杉矶好莱坞的杜比剧院举行，共计颁发24个类别的奥斯卡金像奖（也称学院奖）。晚会通过美国广播公司在美国直播，由吉尔·凯茨担任制片人，路易斯·J·霍维茨导演，曾于两年前主持第78届颁奖晚会的笑匠兼谈话节目主持乔恩·斯图尔特第2次担任主持人。两周前的2月9日，女演员杰西卡·阿尔芭在加利福尼亚州比佛利山的比佛利威尔希尔饭店主持颁发了奥斯卡科技成果奖。《老无所依》获得包括最佳影片在内的4项大奖，是这个夜晚的最大赢家。其它获奖作品包括胜出3项的《谍影重重3》、获奖2项的《玫瑰人生》和《血色将至》，以及胜出1项的《赎罪》、《伪钞制造者》、《伊丽莎白2：黄金时代》、《保险被拒》、《黄金罗盘》、《朱诺》、《迈克尔·克莱顿》、《扒手莫扎特》、《曾经》、《彼得与狼》、《美食总动员》、《理发师陶德》和《开往暗处的的士》。晚会的电视直播平均吸引了约3200万美国观众收看，是电视观众人数最少的一届。
""",

# Japanese
"""雨氷（うひょう）とは、0℃以下でも凍らない過冷却状態の雨（着氷性の雨）が、地面や木などの物体に付着することをきっかけに凍って形成される、硬く透明な氷のこと。着氷現象の一種。
水はふつう凝固点である0℃を下回ると凝固（凍結）し氷となる。しかし、ある条件下では0℃以下であっても凍結しないで液体のままを保つことがある。水を構成する分子が非常に安定しているときに起こるもので、これを過冷却状態という。自然界では、雲や霧を構成する水滴のように3
- 数百μmの大きさでは-20℃程度まで、雨粒のように数百μm
	- 数mmの大きさでは-4℃程度まで、過冷却のものが存在することが知られている。……
	秀逸な記事 / つまみ読み / 選考

文化遺産保護制度（ぶんかいさんほごせいど）では、公的機関による文化遺産の保護に関する制度について述べる。各国政府および国際機関は、人類の文化的活動によって生み出された有形・無形の文化的所産の中でも……
""",

# Polish
"""Największa zanotowana długość ciała samca wynosi 12,75 cm, samicy zaś
14,3 cm[3]. Zwykle jednak wymiary te wynoszą odpowiednio 10,5-12 cm oraz
11-14 cm[5]. Skóra jest szorstka, pokryta nawet na brzusznej stronie ciała
rogowaciejącymi na czubku guzkami, szarawa, oliwkowa bądź czarnawa[3], wedle
innych źródeł także zielona czy brązowa[5]. Jej chropowatość musiała
rozwinąć się wtórnie, gdyż bardzo różni się od gładkiej skóry spotykanej
u bliskich krewnych traszki pirenejskiej. Mogą pokrywać ją żółte cętki
zbiegające się w okolicy kręgosłupa w szeroką podłużną linię, zauważalną
zwłaszcza u osobników młodych i jeszcze nie dorosłych[3]. W miarę upływu
czasu może ona zanikać, aczkolwiek nie musi[5]. Na brzusznej stronie ciała
biegnie podłużna żółta, pomarańczowa lub czerwona kreska, a po bokach
znajduje się czarne plamkowanie[3].

Traszka posiada płaską głowę, u samców proporcjonalnie szerszą i dłuższą niż
u samic, o małych oczach; parotydy nie występują[5]. Spuchnięte brzegi
kloaki samic w kształcie opuszkowo-stożkowym są szersze u podstawy[3].
Porównuje się je do dzwona lub gruszki. Niewielki okrągły otwór pomiędzy
nimi skierowany jest w dół i w tył. U samców występuje kloaka półkolista ze
szparowatym otworem. Ogon u osobników męskich jest wyższy niż u samic, ale
za to krótszy. Tylne łapy samców nie dysponują ostrogami[5]. Przyczepność
zwiększają czarne, zrogowaciałe, paznokciowate zakończenia opuszek palców,
obecne u obu przedstawicieli rodzaju Calotriton. Cechą wyróżniającą go
spośród salamandrowatych jest też specyficzna budowa pierwszego z kręgów
odcinka krzyżowo-ogonowego kręgosłupa: jego wyrostki poprzeczne (processus
transversi) układają się pod kątem prostym w stosunku do osi kręgu[3].

Grzebień nie występuje, co odróżnia tą traszkę od blisko z nią
spokrewnionych przedstawicielek rodzaju Triturus. Rozpatruje się trzy modele
ewolucji grzebienia u salamandrowatych. Wedle jednego z nich przodkowie
traszki pirenejskiej posiadali grzebień i wersja ta wydaje się bardziej
prawdopodobna od dwóch pozostałych, w których pochodzi ona od traszek, które
grzebienia nie wykształcały[4].""",

# Russian
"""
Собственно «вопрос» состоял в предложении предать анафеме в связи
с обвинениями в несторианстве личность и труды богословов Феодора
Мопсуестийского, некоторые труды Феодорита Кирского и одно из писем Ивы
Эдесского. Под «главами» (др.-греч. κεφάλαια) в данном случае понимаются как
письменно изложенные высказывания в форме анафематизмов[2], так и сами
предметы осуждения[3]. Первоначально высказанные в форме императорского
эдикта в середине 540-х годов, анафематизмы были затем утверждены Вторым
Константинопольским собором 553 года. Их принятие вызвало оживлённую
полемику и было в целом неодобрительно встречено христианскими церквями.
Поскольку все осуждённые церковные деятели ко времени событий были, с одной
стороны, уже давно мертвы, а, с другой, пользовались уважением в некоторых
поместных церквях, посягательство на их память привело к бурным событиям
в жизни церкви. Противоречивая роль в событиях папы римского Вигилия
существенно подорвала престиж апостолического престола.

Разногласия между различными христианскими церквями, вызванные спором о трёх
главах, не преодолены до сих пор. Так, например, в коммюнике, принятом после
состоявшихся в июле 1997 года консультаций церквей сирийской традиции[en],
рекомендовалось пересмотреть решения Второго Константинопольского собора
в части осуждения личности и трудов Феодора Мопсуестийского[4].""",

# Spanish
"""
En su tercera temporada en la Segunda División, el equipo tachirense logra
el segundo lugar del Grupo Occidental, al conseguir 34 puntos, dos menos que
el Carabobo FC, producto de 10 victorias, 4 empates y 4 derrotas. Esto le
permite disputar, por segunda temporada consecutiva, el Torneo de Ascenso
a la Primera División de Venezuela. La tabla al final del torneo le otorga
al Ureña SC el quinto lugar, al consechar 29 unidades producto de
9 triunfos, 2 empates y 7 derrotas. marcando 27 goles y recibiendo 26.

Tras su gran desempeño en el Torneo de Ascenso 2013, toma parte en la
Segunda División Venezolana 2013/14, temporada que comenzó con el Torneo
Apertura 2013, donde el equipo ureñense culmina en la octava posición del
Grupo Centro-Occidental, tras sumar 22 unidades y sólo obtener 6 victorias
a lo largo del semestre, pasando a disputarse su permanencia en la categoría
de plata del balompié venezolano en la siguiente mitad de la temporada.
Afronta el Torneo de Promoción y Permanencia 2014 formando parte del Grupo
Occidental, teniendo rivales como el Deportivo JBL del Zulia, ULA FC y el
Club Deportivo San Antonio. Tras superar algunos problemas administrativos,
el equipo tiene un comienzo un tanto irregular, pero, con el avanzar del
torneo logra mejorar su rendimiento y culmina siendo primero de grupo,
sumando un total de 25 puntos y 8 victorias a lo largo de torneo, asegurando
así su permanencia en la segunda categoría para la siguiente temporada.""",

# Italian
"""Lo sbarco di Anzio (nome in codice operazione Shingle, conosciuto anche
come "sbarco di Anzio e Nettuno" o "fronte di Anzio e Nettuno") fu
un'operazione militare di sbarco anfibio, condotta dagli Alleati sulla costa
tirrenica antistante gli abitati di Anzio e Nettuno, durante la campagna
d'Italia nella seconda guerra mondiale. L'obiettivo di tale manovra era la
creazione di una testa di ponte oltre lo schieramento tedesco sulla linea
Gustav, in modo tale da aggirarla e costringere gli avversari a distogliere
ingenti forze dal fronte di Cassino, permettendo così lo sfondamento della
5ª Armata del generale Mark Wayne Clark lungo il settore tirrenico della
Gustav. In contemporanea, le truppe sbarcate ad Anzio e Nettuno avrebbero
occupato i colli Albani, impedendo la ritirata delle divisioni tedesche: la
loro distruzione avrebbe consentito di conquistare Roma e abbreviare la
campagna.""",

# French
"""Clements Robert Markham, né le 20 juillet 1830 à Stillingfleet dans le
Yorkshire et mort le 30 janvier 1916 à Londres, est un fonctionnaire,
géographe, explorateur et écrivain britannique. Il est secrétaire de la
Royal Geographical Society (RGS) entre 1863 et 1888, puis président de
l'institution pendant douze années. Durant cette dernière position, il est
principalement responsable de l'organisation de l'expédition Discovery
(1901-1904), ainsi que du lancement de la carrière d'explorateur polaire de
Robert Falcon Scott.

Markham commence sa carrière en tant que cadet et aspirant dans la Royal
Navy. Il est envoyé dans l'Arctique avec l'HMS Assistance dans l'une des
nombreuses opérations de recherche de l'expédition perdue de John Franklin.
Plus tard, Markham sert en tant que géographe au bureau de l'Inde et est
responsable de l""",

# Turkish
"""Türkiye Türkçesi, dünya dilleri sınıflandırmasında Ural-Altay Dil
Ailesi’nin Altay dilleri kolunda bulunur. Ural-Altay dil birliği temelinde
yapılan derinlemesine araştırmalar, bu iki grubu aynı dil ailesi içinde
birleştirme bakımından gittikçe zayıflayan sonuçlar vermiştir.[16] Bu
sebeple Türkçe, bazı sınıflandırmalarda Altay dillerinden biri olarak
belirtilmekle yetinilir; sınıflama buradan başlatılır.

Ünlü Türkolog Reşit Rahmeti Arat’ın “Türk Şivelerinin Tasnifi” makalesinde
ayrıntılıca anlatıldığı gibi Türkiye Türkçesinin de yer aldığı Türk yazı
dillerinin sınıflandırması konusunda geçmişten bugüne kadar çeşitli bilimsel
görüşler ortaya atılmıştır. Bütün sınıflandırma çalışmalarından da hareketle
Arat’ın yaptığı sınıflandırmaya göre Türkiye Türkçesi, “Türk şive
grupları”nın “VI. daġlı grubu (Cenup)” içinde yer alır.[17] Türk dil ailesi,
Doğu Avrupa, Orta Asya ve Sibirya’da konuşulan 30 kadar yaşayan dili
kapsar.[18] Türk dili konuşurlarının %40 civarında bir kesimi Türkiye
Türkçesi konuşmaktadır.[19] British Council tarafından yapılan bir
araştırmada Türkçe, geleceğin 10 dili arasında dokuzuncu sırada yer
almıştır.[20]""",

# languages using latin alphabet without diacritics or special letters:
# http://linguistics.stackexchange.com/questions/6173/is-english-the-only-language-except-classical-latin-cyrillic-symbol-languages

# Malay/Indonesian

"""dapat diertikan berbeza-beza menurut biologi, rohani, dan istilah
kebudayaan, atau secara campuran. Secara biologi, manusia dikelaskan sebagai
Homo sapiens (Bahasa Latin untuk manusia bijak), sebuah spesies primat dari
golongan mamalia yang dilengkapi otak berkemampuan tinggi. Dalam hal
kerohanian, mereka dijelaskan menggunakan konsep jiwa yang bervariasi di
mana, dalam agama, dikaikan dalam hubungannya dengan kekuatan ketuhanan atau
makhluk hidup; dalam mitos, mereka juga seringkali dibandingkan dengan
bangsa lain. Dalam antropologi kebudayaan, mereka dijelaskan berdasarkan
penggunaan bahasanya, organisasi mereka dalam masyarakat majemuk serta
perkembangan teknologinya, dan terutama berdasarkan kemampuannya untuk
membentuk kelompok dan lembaga untuk dokongan satu sama lain serta
pertolongan.
Manusia dari segi psikologinya merupakan haiwan yang bersosial. Cara
bersosial berbagai-bagai, walaupun tidak disedari oleh kebanyakan manusia,
kaedah sosial manusia sangat kompleks dan lebih maju dari pelbagai aspek
dari haiwan yang paling terdekat kebijakannya dari manusia.
Sosial sangat perlu dan merupakan cara paling efektif untuk mendapatkan
manfaat secara bersama di antara individu. Oleh yang demikian, manusia yang
terkecuali daripada aktivit sosial amat sedikit ataupun mereka
diklasifikasikan sebagai manusia abnormal ataupun manusia gila.
""",

# Tagalog
"""pagpapaunlad ng mga pinapatakbo ng gatong(fuel) na mga teknolohiya at
napabuting kalusugan na nagsanhi sa populasyon ng tao na tumaas ng
eksponensiyal. Sa pagkalat sa bawat kontinente maliban sa Antarctica, ang
mga tao ay isang kosmopolitanng espesye at sa 2012, ang populasyon ng
daigdig ay tinatayang mga 7 bilyon.[14][15] Ang mga tao ay inilalarawan sa
pagkakaroon ng malaking utak na relatibo sa sukat ng katawan nito na may
isang partikular na mahusay na neokorteks, preprontal na korteks at lobong
temporal na gumagawa sa mga ito na may kakayahan sa pangangatwirang
abstrakto, wika, instrospeksiyon, paglutas ng problema at kultura sa
pamamagitan ng pagkatutong panlipunan. Ang kakayahang pang-isip na ito na
sinamahan ng pag-aangkop sa lokomosyong bipedal na nagpapalaya sa mga kanya
sa pagmamanipula ng mga bagay ay pumayag sa mga to na gumawa ng mas higit na
paggamit ng kasangkapan kesa sa anumang mga ibang nabubuhay na espesye ng
daigdig. Ang mga tao ang mga tanging nabubuhay na espesye ng hayop na alam
na makagagawa ng apoy at pagluluto gayundin ang tanging mga espesyeng
makapagdadamit sa kanilang at lumikha at gumamit ng maraming ibang mga
teknolohiya at mga sining. Ang pag-aaral ng mga tao ang disiplinang
pang-agham na antropolohiya. Ang mga tao ay walang katulad na labis na may
kasanayan sa paggamit ng mga sistema ng komunikasyong simboliko gaya ng wika
para sa paghahayag ng sarli, ang pagpapalit ng mga ideya at organisasyon.
Ang mga tao ay lumilikha ng mga komplikadong mga istrakturang panlipunan na
binubuo ng maraming mga nakikipagtulungan at nakikipagtunggaling mga pangkat
mula sa pamilya at ugnayang kamag-anak hanggang sa mga estado. Ang mga
interaksiyong panlipunan sa pagitan ng mga tao ay naglatag ng isang
sukdulang maluwag na uri ng mga halaga, mga asal panlipunan, at mga ritwal
na ang magkakasamang ang bumubuo ng basehan ng lipunang pantao. Ang mga tao
ay kilala sa pagnananis ng mga ito na maunawaan at maimpluwensiyahan ang
kapaligiran nito na naghahangad na ipaliwag at imanipula ang phenomena sa
pamamagitan ng agham, pilosopiya, mitolohiya at relihiyon."""

# Hmong

"""Ib tug Hmoob Asmeskas yog ib tug neeg nyob hauv lub teb chaws As Mes Lis
Kas uas yog haiv neeg Hmoob qhovntsej thiaj tsis mob. Hmoob Asmeskas yog ib
pawg neeg Esxias Asmeskas. Ntau Nplog Hmoob tawg rog rog tsiv mus rau U.S.
tom qab tau hauj cov kooj tsham lwm cov teb chaws Nplog xyoo 1975. Thaum pib
nyob rau nqeg ntawm xyoo ntawd, cov thawj Hmoob tawg rog txog nyob rau
tebchaws Meskas, kev ntawm refugee camps hauv Thaib teb; Txawm li ntawd los,
cov 3,466 xwb tau kev tso cai ncuab lub sij hawm no nyob rau hauv qhov
Refugee Assistance Act ntawm xyoo 1975. (saib cov lus tshaj...)""",

# 

]
