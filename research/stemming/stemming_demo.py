# this will test all algoritms in stemming 

from samples import test


from stemming.porter2 import stem
print()
print("porter2")
test(stem)

try:
	print()
	print("porter")
	from stemming.porter import stem
	test(stem)
except Exception as e:
	print(e)

from stemming.lovins import stem
print()
print("lovins")
test(stem)

from stemming.paicehusk import stem
print()
print("paicehusk")
test(stem)

