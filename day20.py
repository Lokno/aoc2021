import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import product
from collections import defaultdict

def out(str):
    print(str)
    pyperclip.copy(str)

def read_algo_and_image(filename):
    with open(filename) as fin:
        algorithm_str = fin.readline().strip()
        fin.readline()
        file_str = fin.read()
    h = file_str.rstrip('\n').count('\n')+1
    w = file_str.find('\n')
    grid = list(file_str.replace('\n', ''))
    coords = {(x,y):grid[w*y+x] for x,y in product(range(w),range(h))}
    return w,h,grid,coords,algorithm_str

def enhance(image,algo,bounds,space):
    minx,maxx,miny,maxy = bounds
    output = {}

    minx -= 1
    maxx += 1
    miny -= 1
    maxy += 1

    for x in range(minx,maxx+1):
        image[(x,miny)] = space
        image[(x,maxy)] = space

    for y in range(miny+1,maxy):
        image[(minx,y)] = space
        image[(maxx,y)] = space

    for x,y in image:
        pixels = [image.get((x+u,y+v),space) for v,u in product([-1,0,1],[-1,0,1])]
        binary = ''.join(['1' if p == '#' else '0' for p in pixels])
        idx = int(binary,2)
        output[(x,y)] = algo[idx]

    return output,(minx,maxx,miny,maxy)


def iteratively_enhance(filename,steps=2):
    w,h,_,image,algorithm_str = read_algo_and_image(filename)

    bounds = (0,w-1,0,h-1)
    space = '.'

    for i in range(steps):
        image,bounds = enhance(image,algorithm_str,bounds,space)
        space = algorithm_str[0 if space == '.' else 511]

    out(sum(1 for x in image.values() if x == '#'))

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
            iteratively_enhance(args.file)
        else:
            iteratively_enhance(args.file,50)
        end = time.time()
        print( "%f ms" % ((end-start)*1000))