import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import product
from statistics import median

def out(str):
    print(str)
    pyperclip.copy(str)

def read_edges(filename):
    with open(filename) as fin:
        edges = [tuple(line.rstrip().split('-')) for line in fin]
    return edges

def count_paths(edges,validate,set_flag):
    caves = set()
    count = 0
    paths = {}
    for a,b in edges:
        caves.add(a)
        caves.add(b)
        if a in paths:
            paths[a].append(b)
        else:
            paths[a] = [b]
        if b in paths:
            paths[b].append(a)
        else:
            paths[b] = [a]

    s = [(['start'],False)]
    while len(s) > 0:
        path,flag = s.pop()
        name = path[-1]

        for c in paths[name]:
            if c == 'start':
                continue
            elif c == 'end':
                count += 1     
            elif validate(flag,c,path):
                s.append((path+[c],set_flag(flag,c,path)))
    out(count)

def part1(filename):
    edges = read_edges(filename)
    count_paths(edges, lambda flag,cave,path: cave.isupper() or cave not in path
                     , lambda flag,cave,path: False)

def part2(filename):
    edges = read_edges(filename)
    count_paths(edges, lambda flag,cave,path: cave.isupper() or not flag or cave not in path
                     , lambda flag,cave,path: flag or (cave.islower() and cave in path))

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