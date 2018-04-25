from reed_solomon import initialize
from reed_solomon import decode
from dependencies import ReedSolomonError

def output_bin(message):
    for x in (message):
        print(format(x, '#08b'), end=' ')
    print()
def output_dec(message):
    for x in (message):
        print(format(x, ' 8'), end=' ')
    print()


polynomial = 0x61
initialize(polynomial)

message = [58, 58, 58, 58, 58, 58, 58, 59, 59, 59, 59, 25, 47, 25, 49, 44, 58, 17]#
#message[5] = 18
#message[2] = 62
#message[8] = 12
#message[1] = 10

print("Received Message:  ", end='')
output_bin(message)
print("Received Message:  ", end='')
output_dec(message)
try:
    message, check_block = decode(message, 8)
    print("Corrected Message: ", end='')
    output_bin(message + check_block)
    print("Corrected Message: ", end='')
    output_dec(message + check_block)
    print()
    output_bin(message)
    output_dec(message)
except ReedSolomonError as e:
    print("Decoder Error: {0}".format(e))
