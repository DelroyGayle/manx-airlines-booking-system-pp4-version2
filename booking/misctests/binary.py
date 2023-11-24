# Test my seat allocation algorithm using 'bitstring'
# from bitstring import Bits, BitArray, BitStream, pack TODO
from bitstring import BitArray



CAPACITY = 96 # Number of seats in the aircraft
LEFT_BIT_POS = CAPACITY - 1 # I.E. 95

# Find me a number of seats
def row_of_N_seats(number_needed, allocated, available):
    zeros = "0b" + "0"*number_needed
    result = available.find(zeros)
    if not result:
        return (False, allocated, available)
    
    # Set the bits to 1 to represent 'taken' seats 
    bitrange = range(result[0], result[0] + number_needed)
    available.invert(bitrange)
    print(bitrange)
    """
    Airlines generally seat passengers from the back of the aircraft
    So interpret the leftmost bit as position 95
    95 94 93 ... 2 1 0
     0  0  0 ... 0 0 0
    
    Then add that range of seats to the 'allocated' list
    """

    allocated += [*bitrange]
    print(allocated)
    print(available.bin)
    return(True, allocated, available)


# 96 bits
hexstring = "0" * 12
print(hexstring)
# 000000000000
hexstring = "0x" + hexstring
print(hexstring)
# 0x000000000000
seatmap = BitArray(bin = "0" * 96 ) # Empty Plane - All zeros
print(seatmap)
print(seatmap.bin)
"""
IN HEX
0x000000000000000000000000
IN BINARY
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""

# Find one empty seat i.e. one zero
result=seatmap.find("0b0")
print(result, len(result)) 
# (0,) 1

# Find 96 seats i.e. 96 zeros
result=seatmap.find("0b" + "0"*96)
print(result, len(result)) 
# (0,) 1

# This ought to fail - Find 97 seats i.e. 97 zeros
result=seatmap.find("0b" + "0"*97)
print(result, len(result))
# () 0 # FAILED! I.E. False

# Find one seat
result = row_of_N_seats(1, [], seatmap)
print(result)
print(result[2].bin)
"""
(True, [0], BitArray('0x800000000000000000000000'))
100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""

# Find another seat
seatmap = result[2]
allocated = result[1]
result = row_of_N_seats(1, allocated, seatmap)
print(result)
print(result[2].bin)

"""
(True, [0, 1], BitArray('0xc00000000000000000000000'))
110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""

# Find 3 more seats
seatmap = result[2]
allocated = result[1]
result = row_of_N_seats(3, allocated, seatmap)
print(result)
print(result[2].bin)
"""
(True, [0, 1, 2, 3, 4], BitArray('0xf80000000000000000000000'))
111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""
quit()
