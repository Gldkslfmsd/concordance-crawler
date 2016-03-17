from textblob import TextBlob, Word

# https://textblob.readthedocs.org/en/dev/quickstart.html#part-of-speech-tagging

import time
start = time.time()
wiki = TextBlob("Python is a high-level, general-purpose programming language.")
print(wiki.tags)
end = time.time()
print(end-start)

start = time.time()
print(TextBlob("I fly from Prague to NY. I'm flying! He flew home. He has never flown before. A fly flies regurarly.").tags)
end = time.time()
print(end-start)
#print(wiki.noun_phrases)

start = time.time()
print(Word("flying").lemmatize("v"))
end = time.time()
print(end-start)

start = time.time()
print(TextBlob("I fly from Prague to NY. I'm flying! He flew home. He has never flown before. A fly flies regurarly.").words.lemmatize())
end = time.time()
print(end-start)


start = time.time()
for i in range(1000):
	x = Word("flew"+str(i)).lemmatize("r")
	break
#	print(x)
end = time.time()
print(end-start)

print(Word('would').lemmatize('v'))
print(Word('earliest').lemmatize('a'))
