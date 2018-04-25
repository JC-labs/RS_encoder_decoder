from reed_solomon import initialize
from reed_solomon import decode
from dependencies import ReedSolomonError

polynomial = 0x11d
initialize(polynomial)

message = [51, 56, 50, 104, 102, 108, 42, 135, 194, 163, 197, 144, 117, 183]
message[13] = 18
message[2] = 91
message[8] = 73
message[4] = 15

print("Received Message: %s" % message)
print(''.join([chr(x) for x in message[0:6]]))
try:
    message, check_block = decode(message, 8)
    print("Corrected Message: %s" % (message + check_block))
    print(''.join([chr(x) for x in message]))
except ReedSolomonError as e:
    print("Decoder Error: {0}".format(e))
