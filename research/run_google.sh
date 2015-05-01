#!/bin/bash

# this script launches demo_google.py, until some error occur (for example
# until google blocks it), output is saved
# then it waits for 5 minutes and tries it again
# it's repeated for 24 hours

# prefix for output files
OUTPUTFILE=output_google
ERRORFILE=error_google

# 5 minutes in seconds
FIVEMINUTES=$((5*60))

# number of five-minute intervals in 24 hours
LIMIT=$((24*3600 / $FIVEMINUTES))

DATE="date +%Y-%m:%d:%H:%M:%S"

echo `$DATE` "script started"

i=0
while [ $i -lt $LIMIT ]; do
	echo "`$DATE` attempt number $i"
	# run demo_google
	python3 demo_google.py starve > `printf "$OUTPUTFILE%03d.txt" $i`
		2> `printf "$ERRORFILE%03d.txt" $i`
	echo "`$DATE` attempt number $i ended"

	sleep $FIVEMINUTES
	i=$(($i + 10))
done

echo "`$DATE` script ends"
