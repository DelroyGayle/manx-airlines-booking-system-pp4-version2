# Test generating a random pnr

from random import randint
n = 5
for i in range(10):
    s = "".join(["{}".format(randint(0, 9)) for num in range(0, n)])
    print(s)

# Removed similar-looking characters such as l, 1, I, O and 0.
CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
THELIST = [*CHARACTERS]
print(THELIST)
THELIST = list(CHARACTERS)
print(THELIST)
print(len(THELIST))  # 32 CHARACTERS

FIRST_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
THELIST2 = [*FIRST_LETTERS]
print(THELIST2)
print(len(THELIST2))  # 24 CHARACTERS

"""
['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q',
'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'2', '3', '4', '5', '6', '7', '8', '9']
"""

n = 5
for i in range(20):
    chars5 = "".join(["{}".format(THELIST[randint(0, 32)])
                      for num in range(0, n)])
    chars1 = THELIST2[randint(0, 23)]
    print(chars1 + chars5)


quit()
