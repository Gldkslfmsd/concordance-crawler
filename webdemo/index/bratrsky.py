import re

def velka_pismena(text):
	nahrad = [
		# háčky
		("Š", "Sf"),
		("Č", "Cž"),
		("Ř", "Rž"),
		("Ť", "Tž"),
		("Ž", "Zž"),
		("Ď", "Dž"),
		("Ň", "Nž"),

		# G
		("G", "Gž"),
		("Ó", "O"),

	]
	for co, jak in nahrad:
		text = re.sub(co, jak, text)
	return text

def mala_pismena(text):
	nahrad = [
		(r"([czsš])i",r"\1y"),
		(r"([czsš])í",r"\1ý"),
		("ou", "au"),
		("v", "w"),
		(r"(\W|^)u", r"\1v"),
		("s(\w)", r"f\1"),
		("š(\w)", r"ff\1"),

		("g", "ǧ"),
		("j","g"),
		("í", "j"),
	]

	for co, jak in nahrad:
		text = re.sub(co, jak, text)
	return text

def bratrsky(text):
	text = velka_pismena(text)
	text = mala_pismena(text)
	return text

if __name__ == "__main__":
	from sys import stdin
	text = stdin.read()
	print(bratrsky(text))


text = """Toto je vzorový text v českém bratrském pravopise. pravopis
Jinonice jsou u stolu u umyvadla se umývaj uuuu Ó svatý Tomáši"""
#print(bratrsky(text))
modlitba = """Ó svatá Panno a Mučedlnice Boží Starosto! že ty své
pannensktví Ženichu Nebeskému zaslíbila, z poručení Otce svého bla si na
kříž pověšená: já tebe za mou při Bohu věrnou Orodovnici v tomto mém
zármutku vyvoluji, žádajic tebe, ať ten zárkumet a to protivenství, jimž mé
srdce velice obtíženo jest, skrze tvou věrnou přímluvu odemene jest
odvráceno, abych vinšovaného pokoje myslí mé vžila,"""
#print(bratrsky(modlitba))
#print(bratrsky("Český lev"))

