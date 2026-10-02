HEX = "0123456789ABCDEF"
MARKED = "ghijklmnopqrstuv"
STRUCT = "[],;"
ALPHABET = HEX + MARKED + STRUCT

rules = []

def add(state, symbols, move, write, nextstate):
    rules.append((state, symbols, move, write, nextstate))


# INIT: read the opening '[' at cell 0, step right
add("⎆", "[", "→", "", "list_start")

# empty list: '[' immediately followed by ']'
add("list_start", "]", "←", "", "rewind")


# REWIND: walk left back to cell 0 (the '['), then accept
for symbol in ALPHABET.replace("[", ""):
    add("rewind", symbol, "←", "", "rewind")

add("rewind", "[", "⏹", "", "✔")


if __name__ == "__main__":
    for rule in rules:
        print("\t".join(rule))
