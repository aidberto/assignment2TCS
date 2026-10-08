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
add("scanA", ",", "←", "", "to_restore_adv")  # all equal: no swap

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
            add("carryB_" + d, e, "←", "", "to_restore_adv")
        elif di > ei:
            add("carryB_" + d, e, "←", "", "to_restore_swap")
        else:
            # equal: mark B[k], return to A for next digit
            add("carryB_" + d, e, "←", MARKED[ei], "to_A0")


# no swap: go to '[', sweep marks into hex, advance
for s in ALPHABET.replace("[", ""):
    add("to_restore_adv", s, "←", "", "to_restore_adv")
add("to_restore_adv", "[", "→", "", "restore_adv")

for i, m in enumerate(MARKED):
    add("restore_adv", m, "→", HEX[i], "restore_adv")
for d in HEX:
    add("restore_adv", d, "→", "", "restore_adv")
add("restore_adv", ",", "→", "", "restore_adv")
add("restore_adv", "]", "⏹", "", "adv_todo")

# swap: go to '[', sweep marks into hex, swap
for s in ALPHABET.replace("[", ""):
    add("to_restore_swap", s, "←", "", "to_restore_swap")
add("to_restore_swap", "[", "→", "", "restore_swap")

for i, m in enumerate(MARKED):
    add("restore_swap", m, "→", HEX[i], "restore_swap")
for d in HEX:
    add("restore_swap", d, "→", "", "restore_swap")
add("restore_swap", ",", "→", "", "restore_swap")
add("restore_swap", "]", "⏹", "", "swap_todo")


# walk left to cell 0, accept
for symbol in ALPHABET.replace("[", ""):
    add("rewind", symbol, "←", "", "rewind")

add("rewind", "[", "⏹", "", "✔")


if __name__ == "__main__":
    for rule in rules:
        print("\t".join(rule))
