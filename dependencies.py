exponents = [0] * 128
logarithms = [0] * 64
def multiply_wo_look_up(x, y, polynomial = 0, field_characters_full = 64):
    r = 0
    while y:
        if y & 1: r = r ^ x
        y = y >> 1
        x = x << 1
        if polynomial > 0 and x & field_characters_full:
            x = x ^ polynomial
    return r
def multiply_integers(x,y):
    if x==0 or y==0:
        return 0
    return exponents[logarithms[x] + logarithms[y]]
def multiply_polynomials(p,q):
    r = [0] * (len(p)+len(q)-1)
    for j in range(0, len(q)):
        for i in range(0, len(p)):
            r[i+j] ^= multiply_integers(p[i], q[j])
    return r
def power(x, power):
    return exponents[(logarithms[x] * power) % 63]
def divide_polynomials(dividend, divisor):
    output = list(dividend)
    for i in range(0, len(dividend) - (len(divisor)-1)):
        coef = output[i]
        if coef != 0:
            for j in range(1, len(divisor)):
                if divisor[j] != 0:
                    output[i + j] ^= multiply_integers(divisor[j], coef)
    separator = -(len(divisor)-1)
    return output[:separator], output[separator:]
def initialize_log_tables(polynomial):
    global exponents, logarithms
    exponents = [0] * 128
    logarithms = [0] * 64
    x = 1
    for i in range(0, 63):
        exponents[i] = x
        logarithms[x] = i
        x = multiply_wo_look_up(x, 2, polynomial)
    for i in range(63, 128):
        exponents[i] = exponents[i - 63]
    return [logarithms, exponents]


class ReedSolomonError(Exception):
    pass
def evaluate_polynomial(polynomial, x):
    y = polynomial[0]
    for i in range(1, len(polynomial)):
        y = multiply_integers(y, x) ^ polynomial[i]
    return y
def calculate_syndromes(msg, length):
    synd = [0] * length
    for i in range(0, length):
        synd[i] = evaluate_polynomial(msg, power(2,i))
    return [0] + synd
def scale_polynomial(p,x):
    r = [0] * len(p)
    for i in range(0, len(p)):
        r[i] = multiply_integers(p[i], x)
    return r
def inverse_polynomial(x):
    return exponents[63 - logarithms[x]]
def add_polinomials(p,q):
    r = [0] * max(len(p),len(q))
    for i in range(0,len(p)):
        r[i+len(r)-len(p)] = p[i]
    for i in range(0,len(q)):
        r[i+len(r)-len(q)] ^= q[i]
    return r
def substract_integers(x, y):
    return x ^ y
def find_error_locations(syndromes, length):
    error_locations = [1]
    old_error_locations = [1]
    for i in range(0, length):
        K = i
        if len(syndromes) > length:
            K += len(syndromes) - length
        delta = syndromes[K]
        for j in range(1, len(error_locations)):
            delta ^= multiply_integers(error_locations[-(j+1)], syndromes[K - j])

        old_error_locations = old_error_locations + [0] #shift
        if delta != 0:
            if len(old_error_locations) > len(error_locations):
                new_error_locations = scale_polynomial(old_error_locations, delta)
                old_error_locations = scale_polynomial(error_locations, inverse_polynomial(delta))
                error_locations = new_error_locations
            error_locations = add_polinomials(error_locations, scale_polynomial(old_error_locations, delta))
    while len(error_locations) and error_locations[0] == 0: del error_locations[0]
    error_number = len(error_locations) - 1
    if (error_number) * 2 > length:
        raise ReedSolomonError("Too many errors.")
    return error_locations
def find_errors(error_locations, length):
    error_number = len(error_locations) - 1
    error_positions = []
    for i in range(length):
        if evaluate_polynomial(error_locations, power(2, i)) == 0:
            error_positions.append(length - 1 - i)
    if len(error_positions) != error_number:
        raise ReedSolomonError("Too many errors were found. It's impossible to restore the message.")
    return error_positions
def find_error_polynomial(error_positions):
    error_polynomial = [1]
    for i in error_positions:
        error_polynomial = multiply_polynomials(error_polynomial, add_polinomials([1], [power(2, i), 0]))
    return error_polynomial
def find_error_values(syndromes, error_locations, length):
    _, remainder = divide_polynomials( multiply_polynomials(syndromes, error_locations), ([1] + [0]*(length+1)))
    return remainder
def divide_integers(x,y):
    if y==0:
        raise ZeroDivisionError()
    if x==0:
        return 0
    return exponents[(logarithms[x] + 63 - logarithms[y]) % 63]
def correct_errors(input, syndromes, error_positions):
    coeficient_positions = [len(input) - 1 - p for p in error_positions]
    error_locations = find_error_polynomial(coeficient_positions)
    error_values = find_error_values(syndromes[::-1], error_locations, len(error_locations) - 1)[::-1]
    errors = []
    for i in range(0, len(coeficient_positions)):
        l = 63 - coeficient_positions[i]
        errors.append(power(2, -l))
    error_magnitudes = [0] * (len(input))
    errors_length = len(errors)
    for i, Xi in enumerate(errors):
        Xi_inv = inverse_polynomial(Xi)
        err_loc_prime_tmp = []
        for j in range(0, errors_length):
            if j != i:
                err_loc_prime_tmp.append(substract_integers(1, multiply_integers(Xi_inv, errors[j])))
        err_loc_prime = 1
        for coef in err_loc_prime_tmp:
            err_loc_prime = multiply_integers(err_loc_prime, coef)
        y = evaluate_polynomial(error_values[::-1], Xi_inv)
        y = multiply_integers(power(Xi, 1), y)

        magnitude = divide_integers(y, err_loc_prime)
        error_magnitudes[error_positions[i]] = magnitude
    return add_polinomials(input, error_magnitudes)
