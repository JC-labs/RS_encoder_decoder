from dependencies import initialize_log_tables
def initialize(polynomial):
    return initialize_log_tables(polynomial)


from dependencies import multiply_polynomials
from dependencies import divide_polynomials
from dependencies import power
def encode(msg_in, length):
    polynomial = [1]
    for i in range(0, length):
        polynomial = multiply_polynomials(polynomial, [1, power(2, i)])
    _, remainder = divide_polynomials(msg_in + [0] * (len(polynomial)-1), polynomial)
    msg_out = msg_in + remainder
    return msg_out


from dependencies import ReedSolomonError
from dependencies import calculate_syndromes
from dependencies import find_error_locations
from dependencies import find_errors
from dependencies import correct_errors
def decode(input, length):
    if len(input) > 255:
        raise ValueError("Message is too long!!!")
    output = list(input)
    syndromes = calculate_syndromes(output, length)
    if max(syndromes) == 0: # No errors?
        return output[:-length], output[-length:]
    error_locations = find_error_locations(list(syndromes[1:]), length)
    error_position = find_errors(error_locations[::-1], len(output))
    if error_position is None:
        raise ReedSolomonError("It's impossible to locate errors.")
    output = correct_errors(output, syndromes, error_position)

    syndromes = calculate_syndromes(output, length)
    if max(syndromes) > 0:
        raise ReedSolomonError("Message is wrong after the correction.")
    return output[:-length], output[-length:]