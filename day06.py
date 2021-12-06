import sys
import argparse
from pathlib import Path
import time
from itertools import product

def read_counters(filename):
    with open(filename) as fin:
        counters = [int(c) for c in fin.readline().split(',')]
    return counters

def calc_fish_count(filename,days):
    counters = read_counters(filename)
    fish = [[c,1] for c in counters]
    total_count = len(fish)

    for i in range(days):
        new_fish_count = 0

        for i in range(len(fish)):
            counter,count = fish[i]
            counter -= 1
            if counter < 0:
                fish[i][0] = 6
                new_fish_count += count
                total_count += count
            else:
                fish[i][0] = counter

        if new_fish_count > 0:
            fish.append([8,new_fish_count])

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