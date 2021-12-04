import sys
import argparse
from pathlib import Path
import time

def read_values(filename):
    with open(filename) as fin:
        values = [line.rstrip() for line in fin]
    return values

def part1(filename):
    values = read_values(filename)
    n = len(values[0])

    t = []
    for i in range(n):
        t.append([0,0])
    for bits in values:
        for i in range(n):
            t[i][1 if bits[i] == '1' else 0] += 1

    gamma = int(''.join( '1' if one > zero else '0' for zero,one in t ),2)
    epsilon = int(''.join( '1' if one < zero else '0' for zero,one in t ),2)
    print(gamma*epsilon)

def find_rating(values,n,k):
    vals = list(values)
    i = 0
    while len(vals) > 1 and i < n:
        t = [0,0]
        for bits in vals:
            t[1 if bits[i] == '1' else 0] += 1
        if k == 'most':
            filter_bit = 0 if t[0] > t[1] else 1
        else:
            filter_bit = 1 if t[1] < t[0] else 0
        vals = [v for v in vals if int(v[i]) == filter_bit]
        i += 1
    return int(vals[0],2)

def part2(filename):
    values = read_values(filename)
    n = len(values[0])

    oxygen_rating = find_rating(values,n,'most')
    scrubber_rating = find_rating(values,n,'least')

    print(oxygen_rating*scrubber_rating)


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