import sys
import argparse
from pathlib import Path
import time
import pyperclip

def out(str):
    print(str)
    pyperclip.copy(str)

def read_data(filename):
    with open(filename) as fin:
        template = fin.readline().rstrip()
        fin.readline()
        pair_insertions = [line.rstrip().split(' -> ') for line in fin]
    return template,pair_insertions

def pair_insertion(filename,steps):
    template,pair_insertions = read_data(filename)
    elements = {}
    pairs = {}

    mapping = {k:v for k,v in pair_insertions}

    for c in template:
        if c not in elements:
            elements[c] = 0
        elements[c] += 1
    
    for i in range(len(template)-1):
        p = template[i:i+2]
        if p not in pairs:
            pairs[p] = 0
        pairs[p] += 1

    for j in range(steps):
        next_pairs = {}
        for p,e in mapping.items():
            total = 0 if p not in pairs else pairs[p]

            if e not in elements:
                elements[e] = 0
            elements[e] += total

            for pair in [p[0]+e,e+p[1]]:
                if pair not in next_pairs:
                    next_pairs[pair] = 0
                next_pairs[pair] += total
        pairs = next_pairs

    el = [(count,element) for element,count in elements.items()]
    el.sort()

    out(el[-1][0]-el[0][0])

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
            pair_insertion(args.file,10)
        else:
            pair_insertion(args.file,40)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))