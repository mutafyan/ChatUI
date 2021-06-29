import random
import tkinter as tk

#main window class
class SimpleChat(tk.Tk):
    #Constructor
    def __init__(self):
        tk.Tk.__init__(self)
        self.ui_init()
        self.is_open = True
        #Defining change-sensitive for the receive thread callback 
        self.receivedCheck = tk.StringVar()
        self.receivedCheck.trace("w", self.receive_callback)
        #Create send object
        #...

    #Building the gui
    def ui_init(self):
        self.title("Simple Chat")
        self.geometry("300x600") #DEFAULT SIZE
        self.minsize(220, 480) #MINIMUM SIZE
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        # Add icon
        # self.iconphoto(False, tk.PhotoImage(file='path/to/icon.png'))
        self.mainframe = tk.Frame(self, bg="grey")
        self.mainframe.pack(fill="both", expand=True)

        self.frame1 = tk.Frame(self.mainframe)
        self.frame1.pack(side="top", fill="x", expand=False)

        self.frame2 = tk.Frame(self.mainframe)
        self.frame2.pack(side="top", fill="both", expand=True)

        self.userName = tk.StringVar()
        self.userName.set(f"User {str(random.randint(0, 999))}")  # Generates Random username (e.g "User 965")
        
        self.userNameLabel = tk.Label(self.frame1, textvariable=self.userName, anchor="w", relief=tk.RAISED)
        self.userNameLabel.pack(side = "left", fill = "both", expand = True)

        self.edit_button = tk.Button(self.frame1, text="Edit", command=lambda obj=self: SimpleChat.edit_cback(obj))
        self.edit_button.pack(side="right")

        self.receiveText = tk.Text(self.frame2, state='disabled')
        self.receiveText.pack(side="top", fill="both", expand=True)

        self.frame3 = tk.Frame(self.mainframe, bg="green")
        self.frame3.pack(side="top", fill="x", expand=False)

        self.sendText = tk.Entry(self.frame3)
        self.sendText.pack(side="left", fill="both", expand=True)

        self.sendbutton = tk.Button(self.frame3, text="Send", command=lambda obj=self: SimpleChat.send_callback(obj))
        self.sendbutton.pack(side="left")
    
    #Edit button callback //CHANGE USERNAME
    #Disable all the widgets in order to avoid messaging and taking input for the new username 
    def edit_cback(self):
        for child in self.frame2.winfo_children():
            child.configure(state='disable')
        for child in self.frame3.winfo_children():
            child.configure(state='disable')
        self.edit_button.pack_forget()
        self.userNameLabel.pack_forget()

        self.ok_button = tk.Button(self.frame1, text="Ok", command=lambda obj=self: SimpleChat.ok_callback(obj))
        self.ok_button.pack(side="right")

        self.userNameInput = tk.Entry(self.frame1, textvariable=self.userName)
        self.userNameInput.pack(side="left", fill="both", expand=True)

    #ok button callback //SAVE CHANGES
    #Saves new username input from user and enabling all the widgets disabled before
    def ok_callback(self):
        self.userName.set(self.userNameInput.get())
        self.userNameInput.destroy()
        self.userNameLabel.pack(side="left", fill="both", expand=True)
        self.ok_button.destroy()
        self.edit_button.pack(side="right")
        for child in self.frame2.winfo_children():
            child.configure(state='normal')
        for child in self.frame3.winfo_children():
            child.configure(state='normal')
        

    #Configures the message to be send
    def send_callback(self):
        #Configuring the message to be sent
        send_message = self.sendText.get()
        if not len(send_message):
            return
        else:
            send_message = self.userName.get() + ': ' + send_message + '\n'
            #Implement sending logic...

            #inserting the sent message to receiveText textbox
            self.receiveText.configure(state='normal')
            self.receiveText.insert(tk.END, send_message)
            self.receiveText.configure(state='disabled')
            #cleaning the input field
            self.sendText.delete(0, tk.END)
    
    #Receives messages via LoRa device, decodes them from base64 and prints them in the receiveText textbox
    #works in a separate thread until the close button is pressed
    def receive_callback(self, *args):
        self.receiveText.configure(state='normal')
        # rmessage = self.receivedCheck.get()
        self.receiveText.insert(tk.END, self.receivedCheck.get())
        self.receiveText.configure(state='disabled')

    #close button callback 
    #changes is_open to False and waits for receiveThrad to join, then destroys the window
    def on_exit(self):
        self.is_open = False
        #you would also need to wait for the sending thread to join here
        self.destroy()

root = SimpleChat()
root.mainloop()
