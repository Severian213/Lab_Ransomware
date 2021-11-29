import keyGeneration, math

publicKey, privateKey = keyGeneration.keyGen(1024) 

SYMBOL_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !"£$%^&*()-_=+#~:;\'@.,>/?\|`¬'

# Main body of the RSA
def main(modes, msg):
    msg = str(msg)
    mode = modes
    if mode == 'encrypt':
        encryptedText = encrypt(publicKey, msg)
        return encryptedText
    elif mode == 'decrypt':
        decryptedText = decrypt(privateKey, msg)
        return decryptedText
    

def textToBlocks(message, blockSize):
    for character in message:
        if character not in SYMBOL_SET:
            print(f"The symbol set does not contain the character {character}.")
            sys.exit()
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += (SYMBOL_SET.index(message[i])) * ((len(SYMBOL_SET) ** (i % blockSize)))
        blockInts.append(blockInt)
    return blockInts

def blocksToText(blockInts, messageLength, blockSize):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                charIndex = blockInt // (len(SYMBOL_SET) ** i)
                blockInt = blockInt % (len(SYMBOL_SET) ** i)
                blockMessage.insert(0, SYMBOL_SET[charIndex])
        message.extend(blockMessage)
    return ''.join(message)

def encryptBlocks(message, key, blockSize):
    encryptedBlocks = []
    n, e = key
    for block in textToBlocks(message, blockSize):
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks

def decryptBlocks(encryptedBlocks, messageLength, key, blockSize):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return blocksToText(decryptedBlocks, messageLength, blockSize)

def readKey(key):
    keySize, n, EorD = key.split(',')
    return (int(keySize), int(n), int(EorD))

def encrypt(key, message, blockSize=None):
    keySize, n, e = readKey(key)
    if blockSize == None:
        blockSize = int(math.log(2 ** keySize, len(SYMBOL_SET)))
    if not (math.log(2 ** keySize, len(SYMBOL_SET)) >= blockSize):
        sys.exit("Error: Block size is too large")
    encryptedBlocks = encryptBlocks(message, (n, e), blockSize)

    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    encryptedContent = f"{len(message)}_{blockSize}_{encryptedContent}"
    return encryptedContent

def decrypt(key, content):
    keySize, n, d = readKey(key)
    content = str(content)
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    if not (math.log(2 ** keySize, len(SYMBOL_SET)) >= blockSize):
        sys.exit("Error: Block size is too large.")

    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    return decryptBlocks(encryptedBlocks, messageLength, (n, d), blockSize)
