# Run script for Advent of Code
#
# Handles running a series of scripts in the same directory named
# dayDD.py with the input file input/dayDD_input.txt 
#
# If only one argument is provided, it is read as the part no. [1,2]
# When the day is not provided, today's date is used.
#
# Modify lines 44-45 to change what is being run using the 
# {day} and {part} read from input.
#
# usage: ./run.sh [<day [1-25]> = Today] [<part [1,2]> = 1]

#!/bin/bash

if { [ $# -gt 0 ] && [[ ! $1 =~ ^[0-9]+$ ]]; } || 
   { [ $# -eq 1 ] && [[ ! $1 =~ ^[1-2]$ ]]; } ||
   { [ $# -gt 1 ] && [[ ! $2 =~ ^[1-2]$ ]]; };
then
    echo "   usage $0 [<day 1-25> = Today] [<part 1,2> = 1]"
    exit 1;
fi
part=1
month=$(date -d "$D" '+%m')
day=$(date -d "$D" '+%d')
if [ $# -eq 1 ];
then
    part=$1
elif [ $# -eq 2 ];
then
    printf -v day "%02d" $1
    part=$2
fi

if [ $# -lt 2 ] && [ $month -ne 12 ];
then
    echo "ERROR: Cannot use today's date unless it's Dec. 1st through Dec. 25th!"
    exit 1;
fi

if [ $day -lt 1 ] || [ $day -gt 25 ];
then
    echo "ERROR: '$day' is outside day range [1-25]"
    exit 1;
fi

echo python day${day}.py input/day${day}_input.txt --part $part
python day${day}.py input/day${day}_input.txt --part $part