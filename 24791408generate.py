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


# walk left to cell 0, accept
for symbol in ALPHABET.replace("[", ""):
    add("rewind", symbol, "←", "", "rewind")

add("rewind", "[", "⏹", "", "✔")


if __name__ == "__main__":
    for rule in rules:
        print("\t".join(rule))
