import keyGeneration, math

publicKey, privateKey = keyGeneration.keyGen(1024) 

SYMBOL_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !"£$%^&*()-_=+#~:;\'@.,>/?\|`¬'

# Main body of the RSA
def main(modes, msg):
    '''Initiate encryption or decryption.'''
    msg = str(msg)
    mode = modes # set to encrypt or decrypt.
    if mode == 'encrypt':
        encryptedText = encrypt(publicKey, msg)
        return encryptedText
    elif mode == 'decrypt':
        decryptedText = decrypt(privateKey, msg)
        return decryptedText
    

def textToBlocks(message, blockSize):
    '''Convert the text from a string to integer blocks.'''
    for char in message:
        if char not in SYMBOL_SET: # Can't encrypt if the message contains a character not in SYMBOL_SET
            print(f"The symbol set does not contain the character {character}.")
            sys.exit() # exit the program
    blockInts = [] # create an empty list to hold the blocks of integers
    for blockStart in range(0, len(message), blockSize): # Calculates where each block will start in the text
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))): 
            blockInt += (SYMBOL_SET.index(message[i])) * ((len(SYMBOL_SET) ** (i % blockSize))) # (i % blockSize) because for long messages i will evantually be bigger than blockSize.
                                                                                                # need i to be the chars position in the block of text.
        blockInts.append(blockInt) # add each block to the blockInts list
    return blockInts # Return the list of blockInts

def blocksToText(blockInts, messageLength, blockSize):
    '''Convert blocks of integers to text'''
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                charIndex = blockInt // (len(SYMBOL_SET) ** i) # find the character from the symbol set.
                blockInt = blockInt % (len(SYMBOL_SET) ** i) # find the next block to perform the above step on.
                blockMessage.insert(0, SYMBOL_SET[charIndex]) # add the character to the beginning of blockMessage each time
        message.extend(blockMessage)
    return ''.join(message) # return the decrypted message.

def encryptBlocks(message, key, blockSize):
    '''encrypt integer blocks'''
    encryptedBlocks = []
    n, e = key
    for block in textToBlocks(message, blockSize):
        encryptedBlocks.append(pow(block, e, n)) # pow function is equivalent to block**e(mod n). This is how we encrypt each block
    return encryptedBlocks

def decryptBlocks(encryptedBlocks, messageLength, key, blockSize):
    '''Decrypt integer blocks'''
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n)) # equivalent to block**d(mod n). This is how we decrypt the blocks.
    return blocksToText(decryptedBlocks, messageLength, blockSize) # Once the blocks have been decrypted, pass them to blocksToText()

def readKey(key):
    keySize, n, EorD = key.split(',')
    return (int(keySize), int(n), int(EorD))

def encrypt(key, message, blockSize=None):
    '''Encrypt the content.'''
    keyBits, n, e = readKey(key) # Split the key into the size of the key, the product of the two large primes, and e.
    if blockSize == None:
        blockSize = int(math.log(2 ** keyBits, len(SYMBOL_SET)))  # Max blocksize must satisfy: 2**keysize > len(SYMBOL_SET)**blocksize.
    if not (math.log(2 ** keyBits, len(SYMBOL_SET)) >= blockSize): # taking logarithms to the base len(SYMBOL_SET) of both sides, we come up with the blockSize.
        sys.exit("Error: Block size is too large")
    encryptedBlocks = encryptBlocks(message, (n, e), blockSize) # pass the message, the public key, and the block size to encryptedBlocks. 

    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    encryptedContent = f"{len(message)}_{blockSize}_{encryptedContent}"
    return encryptedContent

def decrypt(key, content):
    '''Decrypt the content.'''
    keyBits, n, d = readKey(key) 
    content = str(content)
    messageLength, blockSize, encryptedMessage = content.split('_') # split the message up so that we can decrypt with the components.
    messageLength = int(messageLength) # Convert messageLength to an integer.
    blockSize = int(blockSize) # Convert blockSize to an integer.

    if not (math.log(2 ** keyBits, len(SYMBOL_SET)) >= blockSize): # Max blocksize must satisfy: 2**keysize > len(SYMBOL_SET)**blocksize.
        sys.exit("Error: Block size is too large.")

    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    return decryptBlocks(encryptedBlocks, messageLength, (n, d), blockSize)
