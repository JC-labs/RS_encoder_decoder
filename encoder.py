from reed_solomon import initialize
from reed_solomon import encode

polynomial = 0x11d
initialize(polynomial)

message = "382hfl"
print("Encoded message: %s" % encode([ord(x) for x in message], 8))

#message = [1, 2, 3, 4, 5, 6];
#print("Encoded message: %s" % encode(message, 8))