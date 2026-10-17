import random
import importlib

simulator = importlib.import_module("24791408simulate")
machine = simulator.load("24791408assignment2.tsv")

HEX = "0123456789ABCDEF"

def word(short):
    #Every word is 16 hex digits.
    #leading 0s
    return short.rjust(16, "0")

def check(words, show=True):
    #run machine on 1 list 
    tape_in = "[" + ",".join(words) + "]"
    result = simulator.run(machine, tape_in)
    correct = "[" + ",".join(sorted(words)) + "]"

    assert result.status == "accept", f"did not accept: {result.status}"
    assert result.tape == correct, f"wrong output: {result.tape}"
    assert result.head == 0, f"head ended at cell {result.head}, not 0"

    if show:
        print("  ok:", tape_in, "->", result.tape)

print("Basic tests:")
check([word("1")]) #1 word
check([word("1"), word("2")]) #sorted
check([word("2"), word("1")]) #one swap
check([word("5"), word("5")]) # two equal
check([]) #empty

print("Ordering tests:")
check([word("A"), word("9")]) #letters after digits
check([word("F"), word("0")]) #descending
check([word("1A"), word("1B"), word("19")]) #different last digit
check([word("3"), word("1"), word("2")]) #three out of order

print("Duplicate tests:")
check([word("7"), word("7"), word("7")]) #all same
check([word("B"), word("A"), word("B"), word("A")]) #dups mixed in

print("Big test:")
big_list = []
for digit in "FEDCBA987654321":
    big_list.append(word(digit))
check(big_list)


#random lists
def random_word():
    #one random hex word
    digits = ""
    for _ in range(16):
        digits = digits + random.choice(HEX)
    return digits

print("Random tests:")
random.seed(0)
for _ in range(50):
    how_many = random.randint(0, 6)
    words = []
    for _ in range(how_many):
        words.append(random_word())
    check(words)
print("  ok: 50 random lists all sorted correctly")


#the machine file itself should be valid
def rule(state, symbol, move, write, nextstate):
    #one machine rule
    return "\t".join([state, symbol, move, write, nextstate])

def must_be_rejected(name, lines):
    try:
        simulator.parse(lines)
    except ValueError:
        print("  ok: rejected", name)
    else:
        print("  FAILED: wrongly accepted", name)
        raise SystemExit(1)

print("Validation tests:")
#two rules with the same state and symbol
must_be_rejected("a duplicate rule", [rule("a", "0", "→", "", "b"), rule("a", "0", "→", "", "c")])
#state ' is reached thru halting rule + continuing rule
must_be_rejected("a halt/continue conflict", [rule("a", "0", "→", "", "b"), rule("b", "0", "⏹", "", "b")])

print("\nAll tests passed.")
