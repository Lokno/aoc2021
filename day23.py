import sys
import argparse
from pathlib import Path
import time
import pyperclip

from itertools import product
from copy import deepcopy

def out(str):
    print(str)
    pyperclip.copy(str)

def read_grid(filename):
    first = True
    lines = []
    w = 0
    h = 0
    with open(filename) as fin:
        for line in fin:
            w = max(w,line.find('\n'))
            lines.append(line.rstrip())
            h += 1
        file_str = fin.read()

    grid = []
    for line in lines:
        if len(line) < w:
            line += ' ' * (w-len(line))
        grid += list(line)
    coords = {(x,y):grid[w*y+x] for x,y in product(range(w),range(h)) if grid[w*y+x] != ' '}
    return w,h,grid,coords

energy_dict = {'A' : 1, 'B' : 10, 'C' : 100, 'D' : 1000}
dirs = ((0,1),(0,-1),(1,0),(-1,0))
states = ['src','hall','dst']
room_idx = {'A':0,'B':1,'C':2,'D':3}

def path_clear(x1,y1,x2,y2,x_major,pod_dict):
    path_clear = True
    while (x1,y1) != (x2,y2):
        if x_major:
            if x1 > x2:
                x1 -= 1
            elif x1 < x2:
                x1 += 1
            elif y1 > y2:
                y1 -= 1
            elif y1 < y2:
                y1 += 1
        else:
            if y1 > y2:
                y1 -= 1
            elif y1 < y2:
                y1 += 1
            elif x1 > x2:
                x1 -= 1
            elif x1 < x2:
                x1 += 1
        if (x1,y1) in pod_dict:
            path_clear = False
            break
    return path_clear

def path_clear_room2room(x1,y1,x2,y2,hy,pod_dict):
    return path_clear(x1,y1,x1,hy,False,pod_dict) and path_clear(x1,hy,x2,y2,True,pod_dict) 

def get_moves( idx, pods, hall, rooms, layout ):
    moves = []
    v,x,y,location,energy_used = pods[idx]

    pod_dict = {(x,y): v for v,x,y,_,_ in pods}
    
    if location == 'src':
        for hx,hy in hall:
            if path_clear(x,y,hx,hy,False,pod_dict):
                moves.append((hx,hy,mdist(x,y,hx,hy)*energy_dict[v],'hall'))
    if location == 'src' or location == 'hall':
        i = room_idx[v]

        furthest = 0
        dx,dy = None,None
        for j in range(len(rooms[i])):
            rx,ry = rooms[i][j]
            if location == 'hall' and path_clear(x,y,rx,ry,True,pod_dict): 
                dist = mdist(x,y,rx,ry)
                if dist > furthest:
                    dx,dy = rx,ry
                    furthest = dist
            elif location == 'src' and rx != x and path_clear_room2room(x,y,rx,ry,hall[0][1],pod_dict):
                dist = abs(y-hall[0][1]) + mdist(x,hall[0][1],rx,ry)
                if dist > furthest:
                    dx,dy = rx,ry
                    furthest = dist

        if dx is not None:
            moves.append((dx,dy,furthest*energy_dict[v],'dst'))


    return moves

def print_state( pods, layout ):
    w = 0
    h = 0
    for x,y in layout.keys():
        w = max(w,x)
        h = max(h,y)

    pod_dict = {(x,y): v for v,x,y,_,_ in pods}

    for y in range(h+1):
        line = ''
        for x in range(w+1):
            if (x,y) in pod_dict:
                line += pod_dict[(x,y)]
            elif (x,y) in layout:
                line += layout[(x,y)]
            else:
                line += ' '
        print(line)

def mdist(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def total_energy(pods):
    return sum(used for _,_,_,_,used in pods)

def verify_solution(pods,rooms):
    is_solution = True
    for v,x,y,_,_ in pods:
        if (x,y) not in rooms[room_idx[v]]:
            is_solution = False
            break
    return is_solution

def solve( layout ):
    pods = []
    for (x,y) in layout.keys():
        v = layout[(x,y)]
        if v.isalpha():
            pods.append([v,x,y,'src',0])
            layout[(x,y)] = '.'

    # gather room spaces
    rooms = []
    for (x,y) in layout.keys():
        v = layout[(x,y)]
        empty_neighbors = sum(1 for dx,dy in dirs if (x+dx,y+dy) in layout and layout[(x+dx,y+dy)] == '.')
        if v == '.' and empty_neighbors > 2:
            layout[(x,y)] = '^'
            y += 1
            room = []
            while (x,y) in layout and layout[(x,y)] != '#':
                layout[(x,y)] = '~'
                room.append((x,y))
                y += 1
            rooms.append(room)

    hall = [(x,y) for (x,y),v in layout.items() if v == '.']

    s = [(pods,0)]
    min_cost = 2**64

    highest_depth = 0
    while s:
        pods,depth = s.pop(0)

        if depth > 10: 
            continue

        if verify_solution(pods,rooms):
            cost = total_energy(pods)
            if cost < min_cost:
                min_cost = cost
                print_state(pods,layout)
        else:
            for i in range(len(pods)):
                moves = get_moves(i,pods,hall,rooms,layout)

                for j in range(len(moves)):
                    x,y,cost,location = moves[j]
                    pods_prime = deepcopy(pods)
                    pods_prime[i][1] = x
                    pods_prime[i][2] = y
                    pods_prime[i][3] = location
                    pods_prime[i][4] += cost
                    s.append((pods_prime,depth+1))
                    if depth+1 > highest_depth:
                        highest_depth = depth+1
                        print(f'Depth: {depth+1:d}')
                        print_state(pods_prime,layout)

    out(min_cost)


def part1(filename):
    _,_,_,layout = read_grid(filename)
    solve(layout)

def part2(filename):
    _,_,_,layout = read_grid(filename)

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