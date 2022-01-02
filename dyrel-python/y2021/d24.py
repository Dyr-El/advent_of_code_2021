from re import S
from common import getPuzzle, submitSecure
from collections import deque, Counter
from functools import reduce
from operator import mul
from itertools import permutations, takewhile, accumulate, count, islice

NEIGHBOUR4 = (-1, -1j, 1, +1j)
NEIGHBOUR5 = (-1, -1j, 1, +1j, 0)
NEIGHBOUR8 = (-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j)
NEIGHBOUR9 = (-1-1j, -1j, 1-1j, -1, 0, 1, -1+1j, 1j, 1+1j)

rawInput = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -16
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -8
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -1
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y"""


testProg1 = """inp x
mul x -1"""

testProg2 = """inp z
inp x
mul z 3
eql z x"""

testProg3 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

def parseInput(inp):
    prog = list()
    for line in inp.splitlines():
        prog.append(list(line.split()))
    return prog

def runProg(prog, inps):
    reg = {"w":0, "x":0, "y":0, "z":0}
    i = iter(inps)
    for step in prog:
        if len(step) > 2:
            if step[2] in reg:
                argv = reg[step[2]]
            else:
                argv = int(step[2])
        else:
            try:
                argv = int(next(i))
            except StopIteration:
                return (reg["w"], reg["x"], reg["y"], reg["z"])
        if step[0] == "inp":
            reg[step[1]] = argv
        elif step[0] == "add":
            reg[step[1]] += argv
        elif step[0] == "mul":
            reg[step[1]] *= argv
        elif step[0] == "div":
            reg[step[1]] = int(reg[step[1]] / argv)
        elif step[0] == "mod":
            reg[step[1]] %= argv
        elif step[0] == "eql":
            if reg[step[1]] == argv:
                reg[step[1]] = 1
            else:
                reg[step[1]] = 0
        else:
            assert False
        print(' '.join(step), reg)
    return (reg["w"], reg["x"], reg["y"], reg["z"])

def runTestProg(ri, s):
    p = parseInput(ri)
    return runProg(p, s)

# print(runTestProg(testProg1, "9"))
# print(runTestProg(testProg2, "26"))
# print(runTestProg(testProg2, "89"))
# print(runTestProg(testProg3, "9"))

inp = parseInput(rawInput)
testInp = "31162141116841"
d = list(map(int, testInp))
print(runProg(inp, testInp), d[3], 1, d[3]+8, (((d[0]+12)*26+d[1]+7)*26+d[2]+8)*26+d[3]+8)
# submitSecure(puzzle, "a", "answer a")

# submitSecure(puzzle, "b", "answer b")
