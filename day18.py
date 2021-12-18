import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import permutations
from math import ceil
from copy import deepcopy

def out(str):
    print(str)
    pyperclip.copy(str)

def read_data(filename):
    with open(filename) as fin:
        data = [eval(line.rstrip()) for line in fin]
    return data

def find_simple_pairs_at_depth( pair, depth ):
    s = [(pair,0,0,None)]
    pairs = []
    while s:
        p,d,idx,pp = s.pop(0)
        lft,rgt = p
        if d == depth and isinstance(lft,int) and isinstance(rgt,int):
            pairs.append((p,idx,pp))
        if isinstance(lft,list) and d < depth:
            s.append((lft,d+1,0,p))
        if isinstance(rgt,list) and d < depth:
            s.append((rgt,d+1,1,p))   
    return pairs

def find_nums_gt_base( pair, parent_pair, base ):
    s = [(pair,0,parent_pair,0)]
    nums = []
    while s:
        obj,idx,pp,d = s.pop()
        if isinstance(obj,int) and obj > base:
            nums.append((obj,idx,pp,d))
        elif isinstance(obj,list):
            lft,rgt = obj 
            s.append((rgt,1,obj,d+1))
            s.append((lft,0,obj,d+1))
    return nums

def explode_pair( pair, idx, parent_pair, base_pair ):
    lft,rgt = pair
    nums_in_pair = find_nums_gt_base(base_pair, parent_pair, -1)
    num_count = len(nums_in_pair)
    for i in range(num_count):
        if nums_in_pair[i][2] is pair:
            if i > 0:
                _,j,p,_ = nums_in_pair[i-1]
                p[j] += lft
                pass
            if i < num_count-2:
                val,j,p,_ = nums_in_pair[i+2]
                p[j] += rgt
            break
    parent_pair[idx] = 0

def reduce_pair( pair ):
    pairs_at_depth = find_simple_pairs_at_depth(pair,4)
    for p, idx, parent_pair in pairs_at_depth:
        explode_pair(p,idx,parent_pair,pair)
    while len(nums_gt_base := find_nums_gt_base(pair,None,9)) > 0:
        num,idx,pp,depth = nums_gt_base[0]
        pp[idx] = [num//2,int(ceil(num/2))]
        if depth == 4:
            explode_pair(pp[idx],idx,pp,pair)
    return pair

def magnitude( pair ):
    s = [pair]
    pairs = []
    while s:
        subpair = s.pop()
        pairs.append(subpair)
        for part in subpair:
            if isinstance(part,list):
                s.append(part)
    while pairs:
        p = pairs.pop()
        lft,rgt = p
        p.clear()
        if isinstance(lft,list) and len(lft) == 1 and isinstance(lft[0],int):
            lft = lft[0]
        elif not isinstance(lft,int):
            print('ERROR: Invalid Left Side')
        if isinstance(rgt,list) and len(rgt) == 1 and isinstance(rgt[0],int):
            rgt = rgt[0]
        elif not isinstance(rgt,int):
            print('ERROR: Invalid Right Side')

        p.append(3*lft+2*rgt)
        magn = p[0]
    return magn

def part1(filename):
    data = read_data(filename)
    sum_pair = data.pop(0)
    while data:
        rgt = data.pop(0)
        sum_pair = reduce_pair([sum_pair] + [rgt])
    out(magnitude(sum_pair))
        
def part2(filename):
    data = read_data(filename)
    largest_magn = 0
    for a,b in permutations(data,2):
        largest_magn = max(largest_magn,magnitude(reduce_pair([deepcopy(a)]+[deepcopy(b)])))
    out(largest_magn)

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