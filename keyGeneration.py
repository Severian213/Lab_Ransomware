import primeNumbers, random

def gcd(a, b):
    '''Use the Euclidean algorithm to find the greates common divisor.'''
    while a != 0:
        a, b = b % a, a
    return b

def modInverse(a, m):
    '''Use the extended Euclidean algorithm to find the modular inverse of e, and phi_n'''
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % m


def keyGen(bits):
    '''Generate the private and public keys'''
    # Initialize the two variables that will hold the prime numbers
    p = 0 
    q = 0

    while p == q:
        p = primeNumbers.largePrime(bits)
        q = primeNumbers.largePrime(bits)

    n = p * q # n is the product of the two large prime numbers.
    phi_n = (p - 1) * (q - 1) # phi_n is the number of coprimes that n has.

    while True:
        e = random.randrange(2 ** (bits - 1), 2 ** (bits)) # e must be between 1 and phi_n, and coprime with n and phi_n
        if gcd(e, phi_n) == 1 and gcd(e, n) == 1:
            break

    d = modInverse(e, phi_n) # d is the modular inverse of e and phi_n

    publicKey = f"{bits}, {n}, {e}" # Public key is composed of the key size, the product of the two large primes, and the encryption key.
    privateKey = f"{bits}, {n}, {d}" # Private key is composed of the key size, the product of the two large primes, and the decryption key.

    return publicKey, privateKey
