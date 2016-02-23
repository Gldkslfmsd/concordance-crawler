import matplotlib.pyplot as plt
from similarities import similarities as sims

def plot(sims):
	plt.boxplot([sims["eng"],sims["neng"]])
	plt.show()

def roc(sims):
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
roc(sims)
