import sys
import argparse
from pathlib import Path
import time
from itertools import product

def read_segments(filename):
    segments = []
    with open(filename) as fin:
        for line in fin:
            xy1,xy2 = line.split(' -> ')
            x1,y1 = xy1.split(',')
            x2,y2 = xy2.split(',')
            segment = (int(x1),int(y1),int(x2),int(y2))
            segments.append(segment)
    return segments

def add_to_grid_hori_vert(grid, x1,y1,x2,y2):
    if x1 == x2 and y1 != y2:
        x = x1
        r = range(y1,y2+1) if y1 < y2 else range(y2,y1+1)
        for y in r:
            if (x,y) not in grid:
                grid[(x,y)] = 1
            else:
                grid[(x,y)] += 1
    elif y1 == y2 and x1 != x2:
        y = y1
        r = range(x1,x2+1) if x1 < x2 else range(x2,x1+1)
        for x in r:
            if (x,y) not in grid:
                grid[(x,y)] = 1
            else:
                grid[(x,y)] += 1 

def add_to_grid_diagonal(grid, x1,y1,x2,y2):
    if x1 != x2 and y1 != y2:
        dx = abs(x2-x1)+1
        dy = abs(y2-y1)+1
        if dx == dy:
            xs = 1 if x1 < x2 else -1
            ys = 1 if y1 < y2 else -1
            for i in range(dx):
                x,y = x1+i*xs,y1+i*ys
                if (x,y) not in grid:
                    grid[(x,y)] = 1
                else:
                    grid[(x,y)] += 1

def part1(filename):
    segments = read_segments(filename)

    grid = {}
    
    for x1,y1,x2,y2 in segments:
        add_to_grid_hori_vert(grid,x1,y1,x2,y2)

    print(sum(1 for v in grid.values() if v > 1))

def part2(filename):
    segments = read_segments(filename)

    grid = {}
    
    for x1,y1,x2,y2 in segments:
        add_to_grid_hori_vert(grid,x1,y1,x2,y2)
        add_to_grid_diagonal(grid,x1,y1,x2,y2)

    print(sum(1 for v in grid.values() if v > 1))


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