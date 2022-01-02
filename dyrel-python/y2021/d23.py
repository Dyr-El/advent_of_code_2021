import heapq as hq


startInput = """#############
#...........#
###D#B#D#A###
  #C#C#A#B#
  #########"""

extraStartLines = """  #D#C#B#A#
  #D#B#A#C#
"""

goalInput = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

extraGoalLines = """  #A#B#C#D#
  #A#B#C#D#
"""


def parseInput(inp, extraLines=""):
    inpLines = list(inp.splitlines())
    inpLines[-2:-2] = list(extraLines.splitlines())
    inp = "\n".join(inpLines)
    return {(ri, ci):c
            for ri, r in enumerate(inp.splitlines())
            for ci, c in enumerate(r)}


def calcState(mp):
    firstRow = [" ", " ", "|", " ", "|", " ", "|", " ", "|", " ", " "]
    startColumns = [["", "", "", ""] for i in range(4)]
    endColumns = ["" for i in range(4)]
    maxDepth = 3
    for (r, c), v in mp.items():
        if v in 'ABCD':
            if r == 1:
                firstRow[c-1] = v
            if r > 1:
                startColumns[c//2-1][r-2] = v
                maxDepth = max(maxDepth, r)
    firstRow = ''.join(firstRow)
    startColumns = list((''.join(x) for x in startColumns))
    for ci in range(4):
        while len(startColumns[ci])>0 and startColumns[ci][-1] == "ABCD"[ci]:
            l = startColumns[ci][-1]
            endColumns[ci] = endColumns[ci] + l
            startColumns[ci] = startColumns[ci][:-1]
    return (firstRow, tuple(startColumns), tuple(endColumns), maxDepth-1)



costFactor = {"A":1, "B":10, "C":100, "D":1000}

MovementBlock = {('A', 0):((1,), 2), ('B', 0):((3, 1), 4), ('C', 0):((5, 3, 1), 6), ('D', 0):((7, 5, 3, 1), 8),
                 ('A', 1):((), 1), ('B', 1):((3,), 3), ('C', 1):((5, 3), 5), ('D', 1):((7, 5, 3), 7),
                 ('A', 3):((), 1), ('B', 3):((), 1), ('C', 3):((5,), 3), ('D', 3):((7, 5), 5),
                 ('A', 5):((3,), 3), ('B', 5):((), 1), ('C', 5):((), 1), ('D', 5):((7,), 3),
                 ('A', 7):((3, 5,), 5), ('B', 7):((5,), 3), ('C', 7):((), 1), ('D', 7):((), 1),
                 ('A', 9):((3, 5, 7,), 7), ('B', 9):((5, 7), 5), ('C', 9):((7,), 3), ('D', 9):((), 1),
                 ('A', 10):((3, 5, 7, 9), 8), ('B', 10):((5, 7, 9), 6), ('C', 10):((7, 9), 4), ('D', 10):((9,), 2),}

def findMoveDown(state):
    firstRow = state[0]
    for srcIdx, ch in enumerate(firstRow):
        if ch in "ABCD":
            destIdx = ord(ch) - ord('A')
            destinationBlock = state[1][destIdx]
            if len(destinationBlock) > 0:
                continue
            blocked, firstRowLength = MovementBlock[(ch, srcIdx)]
            if any((firstRow[idx] in "ABCD" for idx in blocked)):
                continue
            newFirstRow = firstRow[:srcIdx] + " " + firstRow[srcIdx+1:]
            endContainers = state[2]
            newEndContainers =  endContainers[:destIdx] + (endContainers[destIdx]+ch,) + endContainers[destIdx+1:]
            depth = state[3]
            totLength = firstRowLength + depth - len(endContainers[destIdx])
            return (newFirstRow, state[1], newEndContainers, depth), totLength * costFactor[ch]
    return None, 0

def findMovesUp(state):
    firstRow = state[0]
    containerRow = state[1]
    destCont = state[2]
    depth = state[3]
    for containerIdx, container in enumerate(containerRow):
        if len(container) == 0:
            continue
        for destIdx, ch in enumerate(firstRow):
            if ch in 'ABCD|':
                continue
            blocked, firstRowLength = MovementBlock[("ABCD"[containerIdx], destIdx)]
            if any((firstRow[idx] in "ABCD" for idx in blocked)):
                continue
            firstRowLength = abs(destIdx - containerIdx*2 - 2)
            newFirstRow = firstRow[:destIdx] + container[0] + firstRow[destIdx+1:]
            newContRow = containerRow[:containerIdx] + (container[1:],) + containerRow[containerIdx+1:]
            totLength = firstRowLength + depth - len(container) - len(destCont[containerIdx]) + 1
            yield (newFirstRow, newContRow, state[2], depth), totLength * costFactor[container[0]]


def findAllMoves(state):
    newState, cost = findMoveDown(state)
    if newState != None:
        yield newState, cost
        return
    for state, cost in findMovesUp(state):
        yield state, cost 

def compareStates(st1, st2):
    return st1 == st2

def calcMoveCost(startState, endState):
    d = []
    hq.heappush(d, (0, startState))
    found = set()
    while len(d)>0:
        cost, st = hq.heappop(d)
        if st in found:
            continue
        found.add(st)
        if compareStates(st, endState):
            return cost
        for newState, addCost in findAllMoves(st):
            newCost = cost + addCost
            hq.heappush(d, (newCost, newState))

startState = calcState(parseInput(startInput))
endState = calcState(parseInput(goalInput))
print(calcMoveCost(startState, endState))
startState = calcState(parseInput(startInput, extraStartLines))
endState = calcState(parseInput(goalInput, extraGoalLines))
print(calcMoveCost(startState, endState))