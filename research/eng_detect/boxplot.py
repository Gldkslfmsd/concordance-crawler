import matplotlib.pyplot as plt
from similarities import similarities as sims

def plot(sims):
	plt.boxplot([sims["eng"],sims["neng"]])
	plt.show()
	
plot(sims)
