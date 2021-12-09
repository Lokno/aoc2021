import sys
import argparse
from pathlib import Path
import time
from itertools import product
from math import prod

def read_grid(filename):
    with open(filename) as fin:
        file_str = fin.read()
    data = {}
    h = file_str.rstrip('\n').count('\n')+1
    w = file_str.find('\n')
    g = [int(x) for x in list(file_str.replace('\n', ''))]
    coords = {(x,y):(g[y*w+x],False) for x,y in product(range(w),range(h))}
    return coords

def get_low_points(coords):
    lows = []
    for (x1,y1),(v,_) in coords.items():
        is_low_point = True
        for x2,y2 in ((0,-1),(0,1),(-1,0),(1,0)):
            c = (x1+x2,y1+y2)
            if c in coords and coords[c][0] <= v:
                is_low_point = False
                break
        if is_low_point:
            lows.append((x1,y1))
    return lows

def get_basin_sizes(coords,lows):
    sizes = []
    for low in lows:
        count = 0
        s = [low]
        while len(s) > 0:
            c = s.pop()
            if c not in coords:
                continue
            v,visited = coords[c]
            if not visited and v != 9:
                coords[c] = (v,True)
                count += 1
                for x2,y2 in ((0,-1),(0,1),(-1,0),(1,0)):
                    s.append((c[0]+x2,c[1]+y2))
        sizes.append(count)

    return sizes

def part1(filename):
    coords = read_grid(filename)
    s = 0
    for c in get_low_points(coords):
        s += coords[c][0]+1
    print(s)

def part2(filename):
    coords = read_grid(filename)
    lows   = get_low_points(coords)
    sizes  = get_basin_sizes(coords,lows)
    sizes.sort()
    print(prod(s for s in sizes[-3:]))

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