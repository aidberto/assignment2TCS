import sys
from collections import namedtuple

BLANK = "·"
HALTING = {"✔", "❗"}  

Result = namedtuple("Result", "status state tape head writes steps")


def parse(lines):
    #rule table
    rules = {}
    problems = []
    halt_targets = set()
    continue_targets = set()

    for lineno, line in enumerate(lines, start=1):
        line = line.rstrip("\n")
        if line == "":
            continue

        state, symbols, move, write, nextstate = line.split("\t")
        for symbol in symbols.split(" "):
            if (state, symbol) in rules:
                problems.append(f"line {lineno}: duplicate rule for ({state}, {symbol})")
            rules[(state, symbol)] = (move, write, nextstate)

        (halt_targets if move == "⏹" else continue_targets).add(nextstate)

    clash = halt_targets & continue_targets
    if clash:
        problems.append("states reached as both halting and continuing: " + ", ".join(sorted(clash)))

    if problems:
        raise ValueError("invalid machine file:\n  " + "\n  ".join(problems))
    return rules

def render(tape):
    #tape dict back to str
    if not tape:
        return ""
    end = max(tape) + 1
    return "".join(tape.get(i, BLANK) for i in range(end)).rstrip(BLANK)

def load(path):
    with open(path, encoding="utf-8") as f:
        return parse(f)

def run(rules, tape_str, max_steps=10 ** 7):
    tape = dict(enumerate(tape_str))
    head = 0
    state = "⎆"
    writes = 0
    steps = 0

    while steps < max_steps:
        if state in HALTING:
            status = "accept" if state == "✔" else "error"
            return Result(status, state, render(tape), head, writes, steps)

        symbol = tape.get(head, BLANK)
        action = rules.get((state, symbol))
        if action is None:
            return Result("stuck", state, render(tape), head, writes, steps)

        move, write, nextstate = action
        steps += 1
        if write != "":
            tape[head] = write
            writes += 1
        state = nextstate

        if move == "⏹":
            status = "accept" if state == "✔" else ("error" if state == "❗" else "halt")
            return Result(status, state, render(tape), head, writes, steps)

        head += 1 if move == "→" else -1
        if head < 0:
            return Result("error", "❗", render(tape), 0, writes, steps)

    return Result("timeout", state, render(tape), head, writes, steps)

if __name__ == "__main__":
    path = sys.argv[1]
    tape_str = sys.argv[2] if len(sys.argv) > 2 else ""
    max_steps = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 7

    r = run(load(path), tape_str, max_steps)
    print(f"status: {r.status}")
    print(f"state:  {r.state}")
    print(f"head:   {r.head}")
    print(f"writes: {r.writes}")
    print(f"steps:  {r.steps}")
    print(f"tape:   {r.tape}")
