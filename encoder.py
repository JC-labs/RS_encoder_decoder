from reed_solomon import initialize
from reed_solomon import encode

polynomial = 0x61
initialize(polynomial)

#message = "382hfl"
#print("Encoded message: %s" % list(bin(x) for x in encode([ord(x) for x in message], 8)))
message = [3, 5, 7] #[0b100111, 0b100001, 0b111111, 0b101101, 0b000101]
for x in encode(message, 8): print(format(x, '#08b'), end=', ')
print()
for x in encode(message, 8): print(x, end=', ')
#print("Encoded message: %s" % list(bin(x) for x in encode([message], 8)))
#message = [1, 2, 3, 4, 5, 6];
#print("Encoded message: %s" % encode(message, 8))