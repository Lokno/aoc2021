import sys
import argparse
from pathlib import Path
import time
import pyperclip

def out(str):
    print(str)
    pyperclip.copy(str)

def read_data(filename):
    dot_list = True
    dots = set()
    instructions = []
    with open(filename) as fin:
        for line in fin:
            if dot_list and line == '\n':
                dot_list = False
                continue
            if dot_list:
                dots.add(tuple([int(x) for x in line.split(',')]))
            elif len(line) > 12:
                axis,pos = line[11:].split('=')
                instructions.append((axis,int(pos)))
    return dots,instructions

def get_dims(dots):
    w = 0
    h = 0
    for x,y in dots:
        w = x if x > w else w
        h = y if y > h else h
    return w+1,h+1

def print_paper(dots,w,h):
    for y in range(h):
        row = ''
        for x in range(w):
            row += '#' if (x,y) in dots else '.'
        print(row)
    print('')

def fold(dots,axis,pos,w,h):
    result = set()

    if axis == 'x':
        for x,y in dots:
            if x > pos:
                x = w-x-1
            result.add((x,y))
        w = w-pos-1
    else:
        for x,y in dots:
            if y > pos:
                y = h-y-1
            result.add((x,y))
        h = h-pos-1

    return result,w,h

def part1(filename):
    dots,instructions = read_data(filename)

    w,h = get_dims(dots)

    axis,pos = instructions[0]
    dots,w,h = fold(dots,axis,pos,w,h)

    out(len(dots))

def part2(filename):
    dots,instructions = read_data(filename)

    w,h = get_dims(dots)

    for axis,pos in instructions:
        dots,w,h = fold(dots,axis,pos,w,h)

    print_paper(dots,w,h)

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