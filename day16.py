import sys
import argparse
from pathlib import Path
import time
import pyperclip
from bitarray import bitarray
from math import prod

def out(str):
    print(str)
    pyperclip.copy(str)

def parse_data(filename):
    with open(filename) as fin:
        data = fin.readline().rstrip()

    ba = bitarray()
    ba.frombytes(bytes.fromhex(data))

    min_packet_length = 11

    len_ba = len(ba)

    equation = {'type_id':0,'subs':[]}
    packets = {0:(0,len_ba,0,equation,0)}

    s = [0]
    version_sum = 0

    while len(s) > 0:
        pos = s.pop()
        length_type,num,parent_pos,parent_eq_data,depth = packets[pos]
        p = pos

        if ((length_type == 0 and (p+min_packet_length) > num) or 
           (length_type == 1 and (p+min_packet_length) > len_ba)):
            continue

        add_on_end = True

        version = int(ba[p:p+3].to01(),2)
        p += 3
        type_id = int(ba[p:p+3].to01(),2)
        p += 3

        version_sum += version

        eq_data = {'type_id':type_id,'subs':[]}
        
        if type_id == 4:
            literal_bits = ''
            while ba[p] == 1:
                literal_bits += ba[p+1:p+5].to01()
                p += 5
            literal_bits += ba[p+1:p+5].to01()
            p += 5

            literal = int(literal_bits,2)

            parent_eq_data['subs'].append(literal)
        else:
            parent_eq_data['subs'].append(eq_data)
            length_type_ID = ba[p]
            p += 1
            if length_type_ID == 0:
                subpacket_len = int(ba[p:p+15].to01(),2)
                p += 15
                packets[p] = (length_type_ID,p+subpacket_len,pos,eq_data,depth+1)
                s.append(p)
                p += subpacket_len

            else:
                subpacket_count = int(ba[p:p+11].to01(),2)
                p += 11
                packets[p] = (length_type_ID,subpacket_count,pos,eq_data,depth+1)
                s.append(p)
                add_on_end = False

        if add_on_end:
            if length_type == 1:
                # Recurse to next unfinished decendant 
                while length_type == 1 and num == 1 and depth > 0:
                    length_type,num,parent_pos,parent_eq_data,depth = packets[parent_pos]
                if length_type == 1 and num > 1:
                    packets[p] = length_type,num-1,parent_pos,parent_eq_data,depth
                    s.append(p)
                elif length_type == 0 and (p+min_packet_length) <= num:
                    packets[p] = length_type,num,parent_pos,parent_eq_data,depth
                    s.append(p)
            elif length_type == 0 and (p+min_packet_length) <= num:
                packets[p] = length_type,num,parent_pos,parent_eq_data,depth
                s.append(p)

    return version_sum,equation

def part1(filename):
    version_sum,_ = parse_data(filename)
    out(version_sum)

ops = {0: sum,
       1: prod,
       2: min,
       3: max,
       5: lambda a: 1 if a[0]  > a[1] else 0,
       6: lambda a: 1 if a[0]  < a[1] else 0,
       7: lambda a: 1 if a[0] == a[1] else 0}

def part2(filename):
    version_sum,equation = parse_data(filename)

    s = [equation]
    operations = []

    # Gather Operations
    while s:
        eq = s.pop()
        if isinstance(eq,dict):
            s.append(eq['subs'])
            operations.append(eq)
        elif isinstance(eq,list):
            for a in eq:
                s.append(a)

    # Solve Operations
    while operations:
        o = operations.pop()
        arr = []
        type_id = o['type_id']
        is_all_literals = True
        for sub in o['subs']:
            if isinstance(sub,dict) and 'result' in sub:
                arr.append(sub['result'])
            elif isinstance(sub,int):
                arr.append(sub)
            else:
                is_all_literals = False
                print("ERROR: Could not solve sub-equation")
                break

        if is_all_literals:
            o['result'] = ops[type_id](arr)

    out(equation['result'])

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