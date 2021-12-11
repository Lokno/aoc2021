import sys
import argparse
from pathlib import Path
import time
from itertools import product
import pyperclip

def out(str):
    print(str)
    pyperclip.copy(str)

def read_grid(filename):
    with open(filename) as fin:
        file_str = fin.read()
    h = file_str.rstrip('\n').count('\n')+1
    w = file_str.find('\n')
    g = [(int(x),False) for x in list(file_str.replace('\n', ''))]
    return w,h,g

def print_grid(octos,w,h):
    s = ''
    for y in range(h):
        for x in range(w):
            s += str(octos[y*w+x][0])
        s += '\n'
    print(s)

def run_step(octos,w,h):
    
    adj = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))
    flash_count = 0

    for i,(v,_) in enumerate(octos):
        octos[i] = (v+1,False)

    s = [(x,y) for x,y in product(range(w),range(h)) if octos[y*w+x][0] > 9]
    while len(s) > 0:
        l = len(s)
        for ox,oy in s:
            flash_count += 1
            octos[oy*w+ox] = (v,True)
            for x,y in adj:
                nx,ny = (ox+x,oy+y)
                if 0 <= nx < w and 0 <= ny < h:
                    v,has_flashed = octos[ny*w+nx]
                    if not has_flashed:
                        octos[ny*w+nx] = (v+1,False)

        s = []
        for x,y in product(range(w),range(h)):
            v,has_flashed = octos[y*w+x]
            if not has_flashed and v > 9:
                s.append((x,y))

    for x,y in product(range(w),range(h)):
        _,has_flashed = octos[y*w+x]
        if has_flashed:
            octos[y*w+x] = (0,False)

    return flash_count

def part1(filename, steps = 100):
    w,h,octos = read_grid(filename)
    flash_count = 0
    for i in range(steps):
        flash_count += run_step(octos,w,h)
    out(flash_count)

def part2(filename):
    w,h,octos = read_grid(filename)
    steps = 0
    while sum(v for (v,_) in octos) > 0:
        steps += 1
        run_step(octos,w,h)
    out(steps)

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