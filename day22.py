import sys
import argparse
from pathlib import Path
import time
import pyperclip

from collections import defaultdict
from itertools import product

def out(str):
    print(str)
    pyperclip.copy(str)

def read_steps(filename):
    steps = []
    with open(filename) as fin:
        for line in fin.readlines():
            state,bound_str = line.rstrip().split(' ')
            bounds = []
            for s in bound_str.split(','):
                bounds.append(tuple([int(x) for x in s[2:].split('..')]))
            steps.append((True if state == 'on' else False,bounds))

    return steps

def part1(filename):
    grid = defaultdict(bool)
    steps = read_steps(filename)
    for state,bounds in steps:
        xmin,xmax = bounds[0]
        ymin,ymax = bounds[1]
        zmin,zmax = bounds[2]
        xmin = max(-50,xmin)
        ymin = max(-50,ymin)
        zmin = max(-50,zmin)
        xmax = min(50,xmax)
        ymax = min(50,ymax)
        zmax = min(50,zmax)
        for x,y,z in product(range(xmin,xmax+1),range(ymin,ymax+1),range(zmin,zmax+1)):
            grid[(x,y,z)] = state

    out(sum(1 for cell in grid.values() if cell))

def handle_nd_sequence(steps,n=3,axis=0,volume=1):
    total = 0
    breaks = set()
    for state,bounds in steps:
        breaks.add(bounds[axis][0])
        breaks.add(bounds[axis][1]+1)
    breaks = sorted(breaks)
    for i in range(len(breaks)-1):
        b = breaks[i]
        volume_prime = volume * (breaks[i+1]-b)
        fsteps = tuple((state,bounds) for state,bounds in steps if bounds[axis][0] <= b <= bounds[axis][1])
        if fsteps:
            if axis < (n-1):
                total += handle_nd_sequence(fsteps,n,axis+1,volume_prime)
            elif fsteps[-1][0]:
                total += volume_prime
    return total

def part2(filename):
    out(handle_nd_sequence(read_steps(filename)))

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