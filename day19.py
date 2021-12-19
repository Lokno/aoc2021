import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import permutations
from collections import defaultdict

from math import sqrt

orientations = [(( 1, 0), ( 1, 1), ( 1, 2)),
                (( 1, 0), (-1, 2), ( 1, 1)),
                (( 1, 0), (-1, 1), (-1, 2)),
                (( 1, 0), ( 1, 2), (-1, 1)),

                (( 1, 2), ( 1, 0), ( 1, 1)),
                (( 1, 2), (-1, 1), ( 1, 0)),
                (( 1, 2), (-1, 0), (-1, 1)),
                (( 1, 2), ( 1, 1), (-1, 0)),

                (( 1, 1), ( 1, 2), ( 1, 0)),
                (( 1, 1), (-1, 0), ( 1, 2)),
                (( 1, 1), (-1, 2), (-1, 0)),
                (( 1, 1), ( 1, 0), (-1, 2)),

                ((-1, 0), ( 1, 2), ( 1, 1)),
                ((-1, 0), (-1, 1), ( 1, 2)),
                ((-1, 0), (-1, 2), (-1, 1)),
                ((-1, 0), ( 1, 1), (-1, 2)),

                ((-1, 2), ( 1, 1), ( 1, 0)),
                ((-1, 2), (-1, 0), ( 1, 1)),
                ((-1, 2), (-1, 1), (-1, 0)),
                ((-1, 2), ( 1, 0), (-1, 1)),

                ((-1, 1), ( 1, 0), ( 1, 2)),
                ((-1, 1), (-1, 2), ( 1, 0)),
                ((-1, 1), (-1, 0), (-1, 2)),
                ((-1, 1), ( 1, 2), (-1, 0))]

def vadd(x1,y1,z1,x2,y2,z2):
    return x1+x2,y1+y2,z1+z2

def vsub(x1,y1,z1,x2,y2,z2):
    return x1-x2,y1-y2,z1-z2

def vmult(x1,y1,z1,x2,y2,z2):
    return x1*x2,y1*y2,z1*z2

def vmdist(x1,y1,z1,x2,y2,z2):
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)

def vtransform(v,o):
    p,(a,b,c) = zip(*o)
    return vmult(*p,v[a],v[b],v[c])

def out(str):
    print(str)
    pyperclip.copy(str)

def read_scanner_data(filename):
    scanners = {}
    reading_beacons = False
    scanner_idx = None
    with open(filename) as fin:
        for line in fin:
            if reading_beacons and line.strip() == '':
                reading_beacons = False
            elif reading_beacons:
                scanners[scanner_idx]['beacons'].append(tuple(int(x) for x in line.split(',')))
            elif line.startswith('--- scanner '):
                scanner_idx = int(line.replace('--- scanner ','').replace(' ---\n',''))
                scanners[scanner_idx] = {'beacons':[]}
                reading_beacons = True
    scanners[0]['position'] = (0,0,0)
    return scanners

def resolve_beacons(filename):
    scanners = read_scanner_data(filename)

    beacons = set(b for b in scanners[0]['beacons'])
    s = [data for idx,data in scanners.items() if idx != 0]
    while s:
        scanner = s.pop(0)
        for o in orientations:
            counts = defaultdict(int)
            found = False
            for v1 in scanner['beacons']:
                for v2 in beacons:
                    delta = vsub(*v2,*vtransform(v1,o))
                    counts[delta] += 1
                    if counts[delta] >= 12:
                        scanner['position']    = delta
                        found = True
                        break
                if found:
                    break
            if found:
                for v in scanner['beacons']:
                    beacons.add(vadd(*vtransform(v,o),*scanner['position']))
                break
        if not found:
            s.append(scanner)

    return scanners,beacons

def part1(filename):
    _,beacons = resolve_beacons(filename)
    out(len(beacons))

def part2(filename):
    scanners,_ = resolve_beacons(filename)

    mdist = 0
    for a,b in permutations(scanners.values(),2):
        mdist = max(mdist,vmdist(*a['position'],*b['position']))

    out(mdist)

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