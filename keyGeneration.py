import primeNumbers, random

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def modInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % m

# Generate keys {generateKey}
def keyGen(bits):
    p = 0
    q = 0

    while p == q:
        p = primeNumbers.largePrime(bits)
        q = primeNumbers.largePrime(bits)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2 ** (bits - 1), 2 ** (bits))
        if gcd(e, phi_n) == 1:
            break

    d = modInverse(e, phi_n)

    publicKey = f"{bits}, {n}, {e}"
    privateKey = f"{bits}, {n}, {d}"

    return publicKey, privateKey
