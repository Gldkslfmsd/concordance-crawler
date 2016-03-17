import inflect
p = inflect.engine()

p.classical()
for word in ["fly", "insect", "fish", "sheep", "tree", "car", "clothes",
	"hair", "man", "woman", "mankind", "nucleus", "octopus", "vertex",
	"matrix","formula"]:
	print("The plural of", word, "is", p.plural(word))



	print(p.inflect("The plural of {0} is plural({0})".format(word)))
#	print(p.inflect("The singular of {0} is singular_noun({0})".format(word)))
	#print(p.inflect("I saw {0} plural("cat",{0})".format(cat_count)))
	"""
print(p.inflect("plural(I,{0}) plural_verb(saw,{0}) plural(a,{1}) plural_noun(saw,{1})".format(N1, N2)))
print(p.inflect("num({0},)plural(I) plural_verb(saw) num({1},)plural(a) plural_noun(saw)".format(N1, N2)))
print(p.inflect("I saw num({0}) plural("cat")\nnum()".format(cat_count)))
print(p.inflect("There plural_verb(was,{0}) no(error,{0})".format(errors)))
print(p.inflect("There num({0},) plural_verb(was) no(error)".format(errors)))
print(p.inflect("Did you want a({0}) or an({1})".format(thing, idea)))
print(p.inflect("It was ordinal({0}) from the left".format(position)))
"""

print(p.plural_verb("saw"))
