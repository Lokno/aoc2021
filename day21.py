import sys
import argparse
from pathlib import Path
import time
import pyperclip

from collections import defaultdict
from math import prod

def out(str):
    print(str)
    pyperclip.copy(str)

def read_positions(filename):
    p = {}
    with open(filename) as fin:
        items = fin.readline().split(" ")
        p[int(items[1])] = int(items[4])
        items = fin.readline().split(" ")
        p[int(items[1])] = int(items[4])
    return [p[1],p[2]]

def sim_practice_game(positions):
    dice = list(range(1,101))
    rolls = 0

    # 0-index positions
    for i in range(2):
        positions[i] -= 1

    scores = [0] * 2
    turn = 0
    while all([s < 1000 for s in scores]):
        turn += 1
        for i in range(2):
            rolls += 3
            positions[i] = (positions[i] + sum(num for num in dice[:3])) % 10
            scores[i] += positions[i]+1
            dice = dice[3:] + dice[:3]
            if scores[i] >= 1000:
                break

    out(rolls * min(scores))

def sim_quantum_game(positions):

    s = [(positions[0]-1,positions[1]-1,0,0,0,1)]

    wins = [0,0]
    while s: 

        p1p,p2p,p1s,p2s,player,count = s.pop() 

        for outcome,universe_count in ((3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)):
            # universe_count games created with the outcome from the combined dice rolls
            positions = [p1p,p2p]
            scores = [p1s,p2s]   
            positions[player]  = (positions[player] + outcome) % 10
            scores[player] += positions[player] + 1

            if scores[player] < 21:
                p1pp,p2pp = positions
                p1sp,p2sp = scores
                s.append((p1pp,p2pp,p1sp,p2sp,(player+1)%2,count*universe_count))
            else:
                wins[player] += count * universe_count

    out(max(wins))

def part1(filename):
    positions = read_positions(filename)
    sim_practice_game(positions)

def part2(filename):
    positions = read_positions(filename)
    sim_quantum_game(positions)

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