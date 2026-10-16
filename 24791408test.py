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
