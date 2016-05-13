'''Displays boxplots of englishnesses from similarities.py and ROC curve.
'''

import matplotlib.pyplot as plt
import numpy as np
from similarities import similarities as sims

def plot(sims):
	keys = sorted(list(sims.keys()))
	keys.pop(keys.index('English'))
	keys.append('English')
	print(keys)
	fig, ax1 = plt.subplots(figsize=(len(keys), 10))
	# this is quite useless
	fig.canvas.set_window_title('similarity_of_languages')
#	plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

	bp = plt.boxplot([sims[k] for k in keys], notch=0, sym='+', vert=1, whis=1.5)

	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
	plt.setp(bp['fliers'], color='red', marker='+')


# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

# Hide these grid behind plot objects
	ax1.set_axisbelow(True)
#	ax1.set_title(u'Podobnost textů v různých jazycích s referenčním '
#	'textem',fontsize=22)
	ax1.set_xlabel('jazyky',fontsize=15)
#	ax1.set_ylabel('podobnost', fontsize=15)
#	plt.boxplot([sims[k] for k in keys])


	# Set the axes ranges and axes labels
#	ax1.set_xlim(0.5, len(keys) + 0.5)
	ax1.set_ylim(0.3, 1)
	xtickNames = plt.setp(ax1, xticklabels=keys)
	plt.setp(xtickNames, rotation=45, fontsize=15)










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
import sys
sys.exit()
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
