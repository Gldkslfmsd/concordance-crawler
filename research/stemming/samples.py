
samples = [
	"factionally",
	"bringing",
	"engaged",
	"samples",
	"hello",
	"victim",
	"threshold",
	"string",
	"strange",
	"straight",
]

def test(stem):
	try:
		for s in samples:
			print(s,stem(s))
	except Exception as e:
		print(e)
