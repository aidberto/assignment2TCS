HEX = "0123456789ABCDEF"
MARKED = "ghijklmnopqrstuv"
STRUCT = "[],;"
ALPHABET = HEX + MARKED + STRUCT

rules = []

def add(state, symbols, move, write, nextstate):
    rules.append((state, symbols, move, write, nextstate))


# read '[', step onto first word
add("⎆", "[", "→", "", "list_start")

# empty list
add("list_start", "]", "←", "", "rewind")

# word follows. skip digits
for digit in HEX:
    add("list_start", digit, "→", "", "skip_word")

for digit in HEX:
    add("skip_word", digit, "→", "", "skip_word")

# single word: already sorted
add("skip_word", "]", "←", "", "rewind")

# second word: compare A with B
add("skip_word", ",", "←", "", "to_A0")
for s in ALPHABET.replace("[", ""):
    add("to_A0", s, "←", "", "to_A0")
add("to_A0", "[", "→", "", "scanA")

# mark first unmarked A digit, carry its value
for m in MARKED:
    add("scanA", m, "→", "", "scanA")
for i, d in enumerate(HEX):
    add("scanA", d, "→", MARKED[i], "carryA_" + d)
add("scanA", ",", "⏹", "", "equal")          # all equal

# walk right over rest of A into B
for d in HEX:
    for e in HEX:
        add("carryA_" + d, e, "→", "", "carryA_" + d)
    add("carryA_" + d, ",", "→", "", "carryB_" + d)

# decide at B[k]
for d in HEX:
    for m in MARKED:
        add("carryB_" + d, m, "→", "", "carryB_" + d)
    for ei, e in enumerate(HEX):
        di = HEX.index(d)
        if di < ei:
            add("carryB_" + d, e, "⏹", "", "less")
        elif di > ei:
            add("carryB_" + d, e, "⏹", "", "greater")
        else:
            # equal: mark B[k], return to A for next digit
            add("carryB_" + d, e, "←", MARKED[ei], "to_A0")


# walk left to cell 0, accept
for symbol in ALPHABET.replace("[", ""):
    add("rewind", symbol, "←", "", "rewind")

add("rewind", "[", "⏹", "", "✔")


if __name__ == "__main__":
    for rule in rules:
        print("\t".join(rule))
