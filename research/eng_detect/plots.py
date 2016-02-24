import matplotlib.pyplot as plt
from similarities import similarities as sims

def plot(sims):
	keys = sorted(list(sims.keys()))
	print(keys)
	plt.boxplot([sims[k] for k in keys])
	plt.show()

def roc(sims):
	'''doesn't work for all languages'''
	neng = sorted(sims["neng"])
	eng = sorted(sims["eng"])

	d = [(a,1) for a in neng] + [(b,0) for b in eng]
	d = sorted(d, key=lambda a: a[0])
	after = [len(eng), len(neng)]
	before = [0, 0]

	X = [0]
	Y = [0]
	for x,t in d[:-1]:
		before[t] += 1
		after[t] -= 1
		tnr = after[0] / (after[0] + before[0])
		fpr = 1-tnr
		tpr = before[1] / (before[1] + after[1])
		X.append(fpr)
		Y.append(tpr)
	X.append(1)
	Y.append(1)
	print(X,Y)
	plt.plot(X,Y)
	plt.show()

	
plot(sims)
try:
	roc(sims)
except:
	keys = list(sims.keys())
	x = []
	for k in keys:
		if k == "eng":
			continue
		x.extend(sims[k])
		del sims[k]
	sims["neng"] = x
	roc(sims)
