import sys
import argparse
from pathlib import Path
import time

def read_moves(filename):
    with open(filename) as fin:
        moves = [l.split(' ') for l in fin.readlines()]
    return moves

def part1(filename):
    moves = read_moves(filename)
    depth = 0
    x = 0

    for d,c in moves:
        c = int(c)
        if d == 'forward':
            x += c
        else:
            depth += -c if d == 'up' else c  

    print(x*depth)

def part2(filename):
    moves = read_moves(filename)
    depth = 0
    x = 0
    aim = 0

    for d,c in moves:
        c = int(c)
        if d == 'forward':
            x += c
            depth += aim*c
        else:
            aim += -c if d == 'up' else c  

    print(x*depth)

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