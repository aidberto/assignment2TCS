HEX = "0123456789ABCDEF"
MARKED = "ghijklmnopqrstuv"
STRUCT = "[],;"
ALPHABET = HEX + MARKED + STRUCT

rules = []

def add(state, symbols, move, write, nextstate):
    rules.append((state, symbols, move, write, nextstate))


# read [
# step onto first word
add("⎆", "[", "→", "", "list_start")

# empty list
add("list_start", "]", "←", "", "rewind")

# word follows
# skip digits
for digit in HEX:
    add("list_start", digit, "→", "", "skip_word")

for digit in HEX:
    add("skip_word", digit, "→", "", "skip_word")

# single word
# already sorted
add("skip_word", "]", "←", "", "rewind")

# second word
# compare A with B
add("skip_word", ",", "←", "", "to_A0")
for sym in ALPHABET.replace("[", ""):
    add("to_A0", sym, "←", "", "to_A0")
add("to_A0", "[", "→", "", "scanA")

# mark first unmarked A digit
# carry its value
for mark in MARKED:
    add("scanA", mark, "→", "", "scanA")
for val, a in enumerate(HEX):
    add("scanA", a, "→", MARKED[val], "carryA_" + a)
add("scanA", ",", "←", "", "adv_toA_exh")  # all equal: no swap

# walk right
# rest of A into B
for a in HEX:
    for digit in HEX:
        add("carryA_" + a, digit, "→", "", "carryA_" + a)
    add("carryA_" + a, ",", "→", "", "carryB_" + a)

# decide at B[k]
for a in HEX:
    a_val = HEX.index(a)
    for mark in MARKED:
        add("carryB_" + a, mark, "→", "", "carryB_" + a)
    for b_val, b in enumerate(HEX):
        if a_val < b_val:
            add("carryB_" + a, b, "←", "", "adv_toA_less")
        elif a_val > b_val:
            add("carryB_" + a, b, "←", "", "to_restore_swap")
        else:
            # equal
            # mark B[k]
            # return to A for next digit
            add("carryB_" + a, b, "←", MARKED[b_val], "ret_toA")


# equal
# return to this word's start
# cross B
# stop before A
for sym in HEX + MARKED:
    add("ret_toA", sym, "←", "", "ret_toA")
add("ret_toA", ",", "←", "", "ret_toA2")
for sym in HEX + MARKED:
    add("ret_toA2", sym, "←", "", "ret_toA2")
for sep in "[,;":
    add("ret_toA2", sep, "→", "", "scanA")

# less: no swap, go to A start (cross B, stop before A)
for sym in HEX + MARKED:
    add("adv_toA_less", sym, "←", "", "adv_toA_less")
add("adv_toA_less", ",", "←", "", "adv_toA_less2")
for sym in HEX + MARKED:
    add("adv_toA_less2", sym, "←", "", "adv_toA_less2")
for sep in "[,;":
    add("adv_toA_less2", sep, "→", "", "restore_adv")

# exhaustion: all equal, go to A start
for sym in HEX + MARKED:
    add("adv_toA_exh", sym, "←", "", "adv_toA_exh")
for sep in "[,;":
    add("adv_toA_exh", sep, "→", "", "restore_adv")

# restore marks in A and B in place, then advance
for val, mark in enumerate(MARKED):
    add("restore_adv", mark, "→", HEX[val], "restore_adv")
for digit in HEX:
    add("restore_adv", digit, "→", "", "restore_adv")
add("restore_adv", ",", "→", "", "restore_adv2")
for val, mark in enumerate(MARKED):
    add("restore_adv2", mark, "→", HEX[val], "restore_adv2")
for digit in HEX:
    add("restore_adv2", digit, "→", "", "restore_adv2")
add("restore_adv2", ",", "←", "", "to_next")   # next pair
add("restore_adv2", "]", "⏹", "", "pass_end")  # end of pass
add("restore_adv2", ";", "⏹", "", "pass_end")

# position at B start
# compare with next word
for sym in HEX + MARKED:
    add("to_next", sym, "←", "", "to_next")
for sep in "[,;":
    add("to_next", sep, "→", "", "scanA")

# swap
# go to [
# sweep marks into hex, swap
for sym in ALPHABET.replace("[", ""):
    add("to_restore_swap", sym, "←", "", "to_restore_swap")
add("to_restore_swap", "[", "→", "", "restore_swap")

for val, mark in enumerate(MARKED):
    add("restore_swap", mark, "→", HEX[val], "restore_swap")
for digit in HEX:
    add("restore_swap", digit, "→", "", "restore_swap")
add("restore_swap", ",", "→", "", "restore_swap")
add("restore_swap", "]", "←", "", "to_swap")

# swap
# go to [
# swap A and B char by char
for sym in ALPHABET.replace("[", ""):
    add("to_swap", sym, "←", "", "to_swap")
add("to_swap", "[", "→", "", "swap_scan")

# mark first unmarked A digit
# carry its value
for mark in MARKED:
    add("swap_scan", mark, "→", "", "swap_scan")
for val, a in enumerate(HEX):
    add("swap_scan", a, "→", MARKED[val], "swap_carryA_" + a)
add("swap_scan", ",", "→", "", "to_unmark")   # all swapped

# walk right
# rest of A into B
for a in HEX:
    for digit in HEX:
        add("swap_carryA_" + a, digit, "→", "", "swap_carryA_" + a)
    add("swap_carryA_" + a, ",", "→", "", "swap_carryB_" + a)

# at B[k]
# write twin(a)
# carry old b back
for a in HEX:
    a_val = HEX.index(a)
    for mark in MARKED:
        add("swap_carryB_" + a, mark, "→", "", "swap_carryB_" + a)
    for b in HEX:
        add("swap_carryB_" + a, b, "←", MARKED[a_val], "swap_carryC_" + b)

# carry
# b left over B
# cross , into A
for b in HEX:
    for mark in MARKED:
        add("swap_carryC_" + b, mark, "←", "", "swap_carryC_" + b)
    add("swap_carryC_" + b, ",", "←", "", "swap_findA_" + b)

# write twin(b) at A[k]
# restart
for b in HEX:
    b_val = HEX.index(b)
    for digit in HEX:
        add("swap_findA_" + b, digit, "←", "", "swap_findA_" + b)
    for mark in MARKED:
        add("swap_findA_" + b, mark, "←", MARKED[b_val], "to_swap")

# go to [
# turn twins into hex
for sym in ALPHABET.replace("[", ""):
    add("to_unmark", sym, "←", "", "to_unmark")
add("to_unmark", "[", "→", "", "unmark")
for val, mark in enumerate(MARKED):
    add("unmark", mark, "→", HEX[val], "unmark")
for digit in HEX:
    add("unmark", digit, "→", "", "unmark")
add("unmark", ",", "→", "", "unmark")
add("unmark", "]", "⏹", "", "swap_done")


# walk left to cell 0
# accept
for sym in ALPHABET.replace("[", ""):
    add("rewind", sym, "←", "", "rewind")

add("rewind", "[", "⏹", "", "✔")


if __name__ == "__main__":
    for rule in rules:
        print("\t".join(rule))
