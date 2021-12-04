import sys
import argparse
from pathlib import Path
import time

def read_data(filename, board_size):
    data = {}
    row = 0
    with open(filename) as fin:
        nums = [int(x) for x in fin.readline().rstrip().split(',')]
        nums.reverse()
        boards = []
        board = {}
        for line in fin:
            if line == '\n':
                continue
            cells = [v for v in line.split(' ') if v != '']
            board.update({(x,row):int(v) for x,v in enumerate(cells) })
            row += 1
            if row == 5:
                row = 0
                boards.append(board)
                board = {}
        
    data['nums'] = nums
    data['boards'] = boards
    return data

def is_winner(b, board_size):
    # rows
    for x in range(board_size):
        if all([False if (x,y) in b else True for y in range(board_size)]):
            return True
    # columns
    for y in range(board_size):
        if all([False if (x,y) in b else True for x in range(board_size)]):
            return True
    return False

def pull_number( data, board_size ):
    num = data['nums'].pop()

    for b in data['boards']:
        for x,y in b.keys():
            if b[(x,y)] == num:
                del b[(x,y)]
                break
    return num

def part1(filename):
    board_size = 5
    winner = False
    data = read_data(filename,board_size)
    
    while not winner:
        num = pull_number(data, board_size)
        for b in data['boards']:
            if is_winner(b, board_size):
                print(sum(b.values())*num)
                winner = True
                break


def part2(filename):
    board_size = 5
    data = read_data(filename,board_size)

    has_not_won = [True] * len(data['boards'])
    
    while any(has_not_won):
        num = pull_number(data, board_size)
        for i,b in enumerate(data['boards']):
            if is_winner(b, board_size):
                has_not_won[i] = False
                if not any(has_not_won):
                    print(sum(b.values())*num)
                    break

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