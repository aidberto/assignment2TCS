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
check([]) #empty
check([word("1")]) #1 word
check([word("1"), word("2")])i#sorted
check([word("2"), word("1")]) #one swap
check([word("5"), word("5")]) # two equal

print("Ordering tests:")
check([word("A"), word("9")]) #letters after digits
check([word("F"), word("0")]) #descending
check([word("1A"), word("1B"), word("19")]) #different last digit
check([word("3"), word("1"), word("2")]) #three out of order

print("Duplicate tests:")
check([word("7"), word("7"), word("7")]) #all same
check([word("B"), word("A"), word("B"), word("A")]) #dups mixed in

print("Big test:")
big_list = [word(digit) for digit in "FEDCBA987654321"] 
check(big_list)
