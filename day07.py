import sys
import argparse
from pathlib import Path
import time
from statistics import median

def read_values(filename):
    with open(filename) as fin:
        values = [int(x) for x in fin.readline().rstrip('\n').split(',')]
    return values

def triangle_number(n):
    return (n*(n+1))//2

def part1(filename):
    data = read_values(filename)
    data.sort()
    n = len(data)
    m = median(data)
    cost = sum([abs(m-x) for x in data])
    print(cost)

def part2(filename):
    data = read_values(filename)

    minx = min(data)
    maxx = max(data)

    min_cost = 2**64
    for i in range(minx,maxx+1):
        cost = sum(triangle_number(abs(x-i)) for x in data)
        if cost < min_cost:
            min_cost = cost

    print(min_cost)


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