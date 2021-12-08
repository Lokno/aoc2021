import sys
import argparse
from pathlib import Path
import time
import string

# digit value to wire representation
digit_to_str = { 0 : 'abcefg', 
                 1 : 'cf',     
                 2 : 'acdeg',  
                 3 : 'acdfg',  
                 4 : 'bcdf',    
                 5 : 'abdfg',   
                 6 : 'abdefg',  
                 7 : 'acf',     
                 8 : 'abcdefg', 
                 9 : 'abcdfg'   }

# wire representation to digit value
str_to_digit = { 'abcefg'  : 0, 
                 'cf'      : 1,     
                 'acdeg'   : 2,  
                 'acdfg'   : 3,  
                 'bcdf'    : 4,    
                 'abdfg'   : 5,   
                 'abdefg'  : 6,  
                 'acf'     : 7,     
                 'abcdefg' : 8, 
                 'abcdfg'  : 9  }

# digits grouped by the number of on wires in their representation
len_to_digit = {2 : (1,),
                3 : (7,),
                4 : (4,),
                5 : (2,3,5),
                6 : (0,6,9),
                7 : (8,)}

# wires grouped by the number of times they appear in a digit
appear_to_wire = { 4 : ('e',),
                   6 : ('b',),
                   7 : ('d','g'),
                   8 : ('a','c'),
                   9 : ('f',) }

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
# 
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

# given a list of wire representations for all 10 digits
# determine the mapping from the wire letters used in this set
# to the wire letters used in the diagram above
def determine_mapping( digits ):
    mapping = {'abcdefg'[i] : set('abcdefg') for i in range(7)}

    for digit in digits:
        m = len(digit)
        if (2 <= m <= 4) or m == 7:
            to_digits = digit_to_str[len_to_digit[m][0]]
            for k in digit:
                mapping[k] = mapping[k].intersection(set(to_digits))

    for w in 'abcdefg':
        count = sum(1 for digit in digits if w in digit)
        possible = appear_to_wire[count]
        if len(possible) == 1:
            mapping[w] = set(possible[0])

    while len(mapping) != sum(len(x) for x in mapping.values()):
        for i,w1 in enumerate('abcdefg'):
            if len(mapping[w1]) == 1:
                r = list(mapping[w1])[0]
                for j,w2 in enumerate('abcdefg'):
                    if i == j:
                        continue
                    if r in mapping[w2]:
                        mapping[w2].remove(r)

    mapping = {k:list(v)[0] for k,v in mapping.items()}
    return mapping


# convert a wire representation to a digit value
def get_digit(m,o):
    key = [m[d] for d in o]
    key.sort()
    key = ''.join(key)
    return str_to_digit[key]

# parse a file with lines with the following format:
# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
def read_data(filename):
    with open(filename) as fin:
        data = [[[y for y in x.split(' ')] for x in line.rstrip().split(' | ')] for line in fin]
    return data

def part1(filename):
    data = read_data(filename)
    print(sum(1 for _,o in data for x in o if ((2 <= len(x) <= 4) or len(x) == 7)))

def part2(filename):
    data = read_data(filename)
    s = 0
    for digits,output in data:
        n = len(output)
        mapping = determine_mapping(digits)
        s += sum(get_digit(mapping,o)*10**(n-i) for i,o in enumerate(output))
    print(s)

if __name__ == "__main__":
    day = sys.argv[0][-5:-3]
    parser = argparse.ArgumentParser(description=f'Solution to Advent of Code 2021 Day {day:s}')
    parser.add_argument('file', help='path to input file')
    parser.add_argument('--part', dest='part', type=int, default=1, choices=range(1, 3), 
                        help='select part (1) or part (2) solution')
    args = parser.parse_args()

    file_path = Path(args.file)

    if not file_path.exists():
        print("ERROR: Input file does not exist", file=sys.stderr)
    elif not file_path.is_file():
        print("ERROR: Input path is not a file", file=sys.stderr)
    else:
        start = time.time()
        if args.part == 1:
            part1(args.file)
        else:
            part2(args.file)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))