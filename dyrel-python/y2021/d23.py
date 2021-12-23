from re import S
from collections import deque, Counter, defaultdict
from functools import reduce
from operator import mul
from itertools import permutations, takewhile, accumulate, count, islice
import heapq as hq

NEIGHBOUR4 = (-1, -1j, 1, +1j)
NEIGHBOUR5 = (-1, -1j, 1, +1j, 0)
NEIGHBOUR8 = (-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j)
NEIGHBOUR9 = (-1-1j, -1j, 1-1j, -1, 0, 1, -1+1j, 1j, 1+1j)


rawInput = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#  
  #########  """
testRaw = """#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########"""

def parseInput(inp):
    d = dict()
    for ri, r in enumerate(inp.splitlines()):
        for ci, c in enumerate(r):
            d[(ri, ci)] = c
    return d

def calcMoves():
    moves = dict()
    for srow in (2, 3):
        for scol in (3, 5, 7, 9):
            moves[(srow, scol)] = list()
            drow = 1
            for dcol in (1, 2, 4, 6, 8, 10, 11):
                forbid = list()
                if srow == 3:
                    forbid.append((2, scol))
                col = scol
                while col != dcol:
                    forbid.append((1, col))
                    if col > dcol:
                        col -= 1
                    else:
                        col += 1
                forbid.append((drow, dcol))
                moves[(srow, scol)].append(((drow, dcol), forbid))
    moves2 = dict()
    for src, dstl in moves.items():
        for dst, forb in dstl:
            if dst not in moves2:
                moves2[dst] = list()
            forb2 = list(reversed(forb[:-1]))
            forb2.append(src)
            moves2[dst].append((src, forb2))
    moves.update(moves2)
    return moves

allMoves = calcMoves()
for k, v in allMoves.items():
    print(k)
    for dst, forbid in v:
        print(" ",dst, forbid)

def calcState(mp):
    state = list()
    for k, v in mp.items():
        if v in 'ABCD':
            state.append((v, k, 0))
    return tuple(sorted(state))

def endState(state):
    for si, s in enumerate(state):
        if s[1] != (2+si%2, 3+(si//2)*2):
            return False
    return True

def deadState(state):
    for si, s in enumerate(state):
        if s[2] > 0 and s[1][0] in (2,3) and s[1][1] != 3+(si//2)*2:
            return True
    return False

def findMoves(start, state, allMoves):
    for dest, forbid in allMoves[start]:
        allowed = True
        for _, pos, _ in state:
            if pos in forbid:
                allowed = False
                break
        if allowed:
            yield dest, len(forbid)

costFactor = {"A":1, "B":10, "C":100, "D":1000}

def findAllMoves(state, allMoves):
    for letter, startPosition, noMoves in state:
        if noMoves > 1:
            continue
        for endPosition, steps in findMoves(startPosition,
                                            state,
                                            allMoves):
            yield (startPosition, 
                   endPosition,
                   costFactor[letter] * steps)

def compareStates(st1, st2):
    for s1, s2 in zip(st1, st2):
        if s1[0] != s2[0] or s1[1] != s2[1]:
            return False
    return True

inp = parseInput(rawInput)
testInp = parseInput(testRaw)
testState = calcState(testInp)
state = calcState(inp)
print(rawInput)
d = []
hq.heappush(d, (0, state))
found = set()
while len(d)>0:
    cost, st = hq.heappop(d)
    if endState(st):
        print(cost, state)
        break
    if deadState(st):
        continue
    if compareStates(st, testState):
        print(cost, st)
        break
    for start, end, addCost in findAllMoves(st, allMoves):
        # print(start, end, addCost)
        newState = list()
        for letter, pos, moves in st:
            if pos == start:
                newState.append((letter, end, moves+1))
            else:
                newState.append((letter, pos, moves))
        newState = tuple(sorted(newState))
        newCost = cost + addCost
        if newState in found:
            continue
        found.add(newState)
        hq.heappush(d, (newCost, newState))
    print(cost, len(found), len(d))
    # input()
# print(findAllMoves(inp, state, forbidden))
# submitSecure(puzzle, "a", "answer a")

# submitSecure(puzzle, "b", "answer b")
