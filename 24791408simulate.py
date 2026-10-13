import sys
from collections import namedtuple

BLANK = "·"
HALTING = {"✔", "❗"}  

Result = namedtuple("Result", "status state tape head writes steps")


def parse(lines):
    #rule table
    rules = {}
    problems = []

    for lineno, line in enumerate(lines, start=1):
        line = line.rstrip("\n")

        if line == "":
            continue

        state, symbols, move, write, nextstate = line.split("\t")

        for symbol in symbols.split(" "):
            if (state, symbol) in rules:
                problems.append(f"line {lineno}: duplicate rule for ({state}, {symbol})")
            rules[(state, symbol)] = (move, write, nextstate)

    if problems:
        raise ValueError("invalid machine file:\n  " + "\n  ".join(problems))

    return rules


def load(path):
    with open(path, encoding="utf-8") as f:
        return parse(f)

def run(rules, tape_str):
    tape = dict(enumerate(tape_str))
    pos = 0
    state = "⎆"

    for _ in range(10 ** 6):
        if state == "✔" or state == "❗":
            break

        symbol = tape.get(pos, BLANK)
        if (state, symbol) not in rules:
            break

        move, write, nextstate = rules[(state, symbol)]
        if write != "":
            tape[pos] = write

        state = nextstate
        if move == "⏹":
            break

        pos += 1 if move == "→" else -1
        if pos < 0:
            state = "❗"

    end = max(tape) + 1 if tape else 0
    result = "".join(tape.get(i, BLANK) for i in range(end)).rstrip(BLANK)
    return state, result

if __name__ == "__main__":
    rules = load(sys.argv[1])
    tape_str = sys.argv[2] if len(sys.argv) > 2 else ""
    state, result = run(rules, tape_str)
    print(state, "[" + result + "]")
