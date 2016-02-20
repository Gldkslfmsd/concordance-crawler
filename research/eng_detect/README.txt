frequencies.py
	extracts frequencies of n-grams from given files

frequencies_odd_version.py
	odd unsuccesful attempt

freq
	frequencies from English wikipedia (output of frequencies.py), counted
	1,2,3-grams

sortfreq
	freq sorted via `sort` command 

countsortfreq
	freq sorted via `sort` command by numbers of occurrences



I decided to make my own English detector, a function that decides, whether
an input text is English or not. It will use cosine similarity of vector of
frequencies of n-grams and thresholding.
