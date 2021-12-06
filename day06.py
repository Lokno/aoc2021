import sys
import argparse
from pathlib import Path
import time
from itertools import product

def calc_fish_count(filename,days):
    m = 8
    total_count = 0;
    counts = [0]*(m+1)
    with open(filename) as fin:
        for c in fin.readline().split(','):
            counts[int(c)] += 1
            total_count += 1

    for i in range(days):
        counts = counts[1:] + counts[:1]
        total_count += counts[8]
        counts[m-2] += counts[8]

    print(total_count)

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
            calc_fish_count(args.file,80)
        else:
            calc_fish_count(args.file,256)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))