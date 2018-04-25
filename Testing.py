from dependencies import divide_polynomials
from dependencies import initialize_log_tables

initialize_log_tables(0x11d)
print("Result: %s, %s" % divide_polynomials([68, 97, 109, 110, 105, 116, 0, 0, 0, 0, 0, 0, 0, 0], [1, 255, 11, 81, 54, 239, 173, 200, 24]))