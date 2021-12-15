import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import product

from heapq import heappush,heappop

class pqueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<removed-task>'

    def remove(self,data):
        entry = self.entry_finder.pop(data)
        entry[-1] = self.REMOVED

    def add(self,data,priority=0):
        if data in self.entry_finder:
            self.remove(data)
        entry = [priority, data]
        self.entry_finder[data] = entry
        heappush(self.pq, entry)

    def pop(self):
        while self.pq:
            priority, data = heappop(self.pq)
            if data is not self.REMOVED:
                del self.entry_finder[data]
                return priority, data
        raise KeyError('pop from an empty pqueue')

def out(str):
    print(str)
    pyperclip.copy(str)

def read_grid(filename):
    with open(filename) as fin:
        file_str = fin.read()
    h = file_str.rstrip('\n').count('\n')+1
    w = file_str.find('\n')
    grid = file_str.replace('\n', '')
    coords = {(x,y):int(grid[w*y+x]) for x,y in product(range(w),range(h))}
    return w,h,coords

def print_grid(w,h,grid):
    for y in range(h):
        s = ''
        for x in range(w):
            s += str(grid[(x,y)])
        print(s)

def expand_grid(w,h,grid):
    nw = w*5
    nh = h*5
    coords = {}
    for x,y in product(range(nw),range(nh)):
        sx = x % w
        sy = y % h

        risk = grid[(sx,sy)] + x // w + y // h
        risk = risk if risk < 10 else risk-9

        coords[(x,y)] = risk

    return nw,nh,coords

def print_memo(memo,w,h):
    for y in range(h):
        s = ''
        for x in range(w):
            s += '{: 3d} '.format(memo[(x,y)])
        print(s)

def calculate_least_risk(w,h,grid):
    unvisited = set((x,y) for x,y in product(range(w),range(h)))
    risks = {}

    start = (0,0)
    end = (w-1,h-1)

    risks[start] = 0

    pq = pqueue()
    pq.add(start)

    while end in unvisited:
        risk,(x,y) = pq.pop()
        for px,py in ((-1,0),(0,-1),(1,0),(0,1)):
            nc = x+px,y+py
            if nc in unvisited:
                nr = risk+grid[nc]
                onr = w*h if nc not in risks else risks[nc]
                if nr < onr:
                    risks[nc] = nr
                    pq.add(nc,nr)
        unvisited.remove((x,y))

    out(risks[end])

def part1(filename):
    w,h,grid = read_grid(filename)
    calculate_least_risk(w,h,grid)

def part2(filename):
    w,h,grid = read_grid(filename)
    w,h,grid = expand_grid(w,h,grid)
    calculate_least_risk(w,h,grid)

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