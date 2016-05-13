import stopit
from time import sleep

"""
https://raw.githubusercontent.com/glenfant/stopit/10c52bf840c82f2bacaf42c0c2cfe73ab00e73e8/src/stopit/utils.py

	# Possible values for the ``state`` attribute, self explanative
	EXECUTED, EXECUTING, TIMED_OUT, INTERRUPTED, CANCELED = range(5)
"""

with stopit.ThreadingTimeout(5, swallow_exc=False) as t:
	
	assert t.state == t.EXECUTING

	for i in range(10):
		sleep(1)
		print("asdfsfda")

print(t.state)
print(vars(t))
print(vars(stopit.ThreadingTimeout))
