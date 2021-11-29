import math, random

def eratosthenes(size):
    '''Find all the prime numbers in a given range.'''
    sieve = [True] * size
    sieve[0] = False
    sieve[1] = False

    for i in range(2, int(math.sqrt(size)) + 1):
        notPrime = i * 2
        while notPrime < size:
           sieve[i] = False
           notPrime += i

    primes = []
    for i in range(size):
        if sieve[i] == True:
            primes.append(i)
    return primes

 # Primality test
def millerRabin(num):
    '''Primality test.'''
    if num % 2 == 0 or num < 2:
        return False
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

smallOnes = eratosthenes(100)

def isPrime(num):
    '''Short test to see if num is prime. Pass to miller-rabin.'''
    if (num < 2):
        return False

    for prime in smallOnes:
        if (num == prime):
            return True
        if (num % prime == 0):
            return False

    return millerRabin(num)

# Generate large primes
def largePrime(keyBits=1024):
    '''Generate a large prime number.'''
    while True:
        num = random.randrange(2 ** (keyBits-1), 2 ** (keyBits))
        if isPrime(num):
            return num






        
