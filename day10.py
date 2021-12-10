import sys
import argparse
from pathlib import Path
import time
import pyperclip

def read_lines(filename):
    with open(filename) as fin:
        data = [line.rstrip() for line in fin]
    return data

def out(str):
    print(str)
    pyperclip.copy(str)

def validate(line):
    syntax_points = {')' : 3, ']' : 57, '}' : 1197, '>' : 25137}
    ob = '([{<'
    cb = ')]}>'
    empties = [o+c for o,c in zip(ob,cb)]
    while any(oc in line for oc in empties):
        for o,c in zip(ob,cb):
            oc = o+c
            line = line.replace(oc,'')
    first_closing = len(line)-1
    any_found = False
    for c in cb:
        idx = line.find(c)
        if idx >= 0 and idx < first_closing:
            first_closing = idx
            any_found = True
    if any_found and first_closing >= 0:
        return line,syntax_points[line[first_closing]]
    else:
        return line,0;

def calc_completion_score(s):
    completion_points = {')' : 1, ']' : 2, '}' : 3, '>' : 4}
    score = 0
    for c in s:
        score *= 5
        score += completion_points[c]
    return score

def part1(filename):
    data = read_lines(filename)
    total_score = 0
    for line in data:
        _,score = validate(line)
        total_score += score
    out(total_score)

def part2(filename):
    ob = '([{<'
    cb = ')]}>'
    data = read_lines(filename)
    scores = []
    for line_num,line in enumerate(data):
        unmatched,score = validate(line)
        if score == 0:
            completion_string = [cb[ob.find(s)] for s in unmatched[::-1]]
            scores.append(calc_completion_score(completion_string))
    scores.sort()
    out(scores[len(scores)//2])

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