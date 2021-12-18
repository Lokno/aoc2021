import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import product

def out(str):
    print(str)
    pyperclip.copy(str)

# target area: x=20..30, y=-10..-5
def read_data(filename):
    with open(filename) as fin:
        coord_range_str = fin.readline().rstrip()
    x_range_str,y_range_str = coord_range_str[coord_range_str.find('x'):].split(', ')
    xmin,xmax = x_range_str[2:].split('..')
    ymin,ymax = y_range_str[2:].split('..')
    return int(xmin),int(xmax),int(ymin),int(ymax)

def test_velocity(vx,vy,bounds,max_steps=1000):
    px,py = 0,0
    xmin,xmax,ymin,ymax = bounds

    max_height = 0
    valid = False
    for i in range(max_steps):
        px += vx
        py += vy
        vy -= 1
        vx = vx-1 if vx > 0 else vx+1 if vx < 0 else 0
        if xmin <= px <= xmax and ymin <= py <= ymax:
            valid = True
        max_height = max(max_height,py)

    return valid,max_height

def part1(filename):
    bounds = read_data(filename)
    highest = 0
    for x,y in product(range(1,120),range(-120,120)):
        valid,max_height = test_velocity(x,y,bounds)
        if valid:
            highest = max(highest,max_height)
    out(highest)

def part2(filename):
    bounds = read_data(filename)
    xmin,xmax,ymin,ymax = bounds
    count = 0
    for x,y in product(range(1,500),range(ymin,500)):
        valid,_ = test_velocity(x,y,bounds)
        if valid:
            count += 1
    out(count)

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