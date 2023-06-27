#imports all the necessary libraries

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import smtplib
import re
import datetime
import hashlib

class MainApplication(tk.Tk): # class created for the whole interface
    def __init__(self): # constructor
        super().__init__() # tkinter widget needs super()
        self.title("MathBot") # assigns the class a title
        self.geometry('550x310') # gives the window a size pixel wise
        self.resizable(width=0, height=0) # makes it not resizeable such that the window size is fixed
        self.notebook = ttk.Notebook(self) # notebook provides the tabular access for users

        # creates four frames for the four tabs
        self.Frame1 = WelcomePage(self.notebook)
        self.Frame2 = RulesPage(self.notebook)
        self.Frame3 = ChatWindowPage(self.notebook)
        self.Frame4 = AdminPage(self.notebook)

        # adds text to each of the tabs to show title
        self.notebook.add(self.Frame1, text='Welcome')
        self.notebook.add(self.Frame2, text='Rules')
        self.notebook.add(self.Frame3, text='Chat')
        self.notebook.add(self.Frame4, text='Admin Login')

        self.notebook.pack() # function which declares the position of widgets next to each other rather than specific grid points


# ------ For saving student details in file function ----------

def save(): # new function created called save
    f = open("EntryDetails.txt", "a") # opens the text file EntryDetails in the append mode

    for entry in studentsinfo: # for loop which adds the content in the entry box to this file and a comma
        f.write(entry + ", ")

    f.write("\n") # new line added after each student enters all details

    messagebox.showinfo("Successful Entry", "Details successfully entered. Read Rules and proceed to the Chat Window") # a message box is shown with the message
    f.close() # file is closed

studentsinfo = [] # empty list to input entries in frame 1


class WelcomePage(ttk.Frame): # first tab - Welcome
    def __init__(self, container): # constructor
        super().__init__() # constructor gives access to all methods and attributes of first class

        self.titleA = ttk.Label(self, text = "Welcome to Math Bot") # label
        self.titleA.grid(column=0, row=0, padx = 10, pady = 15) # uses the grid coordinates to position the label

        self.studentName = ttk.Label(self, text="Student Name")  # creates label for student name input
        self.studentName.grid(column=0, row=15)

        self.studentNameBox = ttk.Entry(self, text="")  # creates entry box for the student name
        self.studentNameBox.grid(column=4, row=15)

        self.yearGroup = ttk.Label(self, text="Year Group")  # creates label for year group input
        self.yearGroup.grid(column=0, row=20)

        self.yearGroupBox = ttk.Entry(self, text="")  # creates entry box for the year group
        self.yearGroupBox.grid(column=4, row=20)

        self.teacherEmail = ttk.Label(self, text="Maths Teacher Email")  # creates label for email input
        self.teacherEmail.grid(column=0, row=25)

        self.teacherEmailBox = ttk.Entry(self, text="")  # creates entry box for the teacher's email
        self.teacherEmailBox.grid(column=4, row=25)

        self.Topic= ttk.Label(self, text="Topic")  # creates label for topic input
        self.Topic.grid(column=0, row=35)

        self.TopicBox = ttk.Entry(self, text="")  # creates entry box for topic input
        self.TopicBox.grid(column=4, row=35)

        loginbutton = ttk.Button(self, text="Enter",
                                 command=self.enter)  # login button command runs enter function
        loginbutton.grid(column=2, row=50)

    def enter(self):  # function which gets called when 'entered'
        regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[-]\w+[.]\w{3}[.]\w{2}$'  # regex for alice smith school email
        # regex explanation -
        # 1) one or more letters or numbers
        # 2) optional underscore or full stop
        # 3) one or more letters or numbers
        # 4) @ symbol followed by one or more of any character
        # 5) full stop followed by 3 letters (eg. edu)
        # 6) full stop followed by 2 letters (eg. my)

        # validates the email entry and makes sure all of them are in appropriate format

        # regex makes sure the email is in the correct format

        try:  # exception handling
            int(self.yearGroupBox.get())  # function to check if the input can be converted to an integer
        except ValueError:  # if there is an error with the conversion
            messagebox.showinfo("",
                                "Invalid Year Group")  # a message box is output with the message indicating invalid year group
        else:
            if 7 <= int(self.yearGroupBox.get()) <= 13:  # if the integer is within the range 7 - 13
                if str(self.studentNameBox.get()) and str(self.TopicBox.get()) and re.search(regex_email,
                                                                                             self.teacherEmailBox.get()) and int(
                        self.yearGroupBox.get()):
                    # the variable types of the name and topic are strings
                    # the input of the email is checked against the regular expression rule

                    studentsinfo.append(
                        self.studentNameBox.get())  # appends the student name to empty list students info
                    studentsinfo.append(self.yearGroupBox.get())  # appends the year group to empty list students info
                    studentsinfo.append(
                        self.teacherEmailBox.get())  # appends the teacher's email to empty list students info
                    studentsinfo.append(self.TopicBox.get())  # appends the topic to empty list students info
                    studentsinfo.append(
                        str(datetime.datetime.now()))  # appends the time at which the details are entered
                    save()  # calls the function 'save' to save the inputs to the text file
                else:  # else
                    messagebox.showinfo("Error",
                                        "Please enter details correctly")  # an output message is presented saying the input is invalid
            else:
                messagebox.showinfo("", "Invalid Year Group")  # if the year group is not within the range, a message box is output

class RulesPage(ttk.Frame): # second tab - Rules
    def __init__(self, container): #constructor
        super().__init__() #automatically calls superclass
        # ------- following lines create labels for each line with rules content--------
        # the positions are of the same column but one extra row each time
        # padx and pady provides a padding around the label
        # sticky = NSWE shows that if dragged, all 4 directions are increased

        self.titleB = ttk.Label(self, text = "Rules") # title
        self.titleB.grid(column=1, row=1, padx=10, pady=15, sticky="NSWE")

        self.Rules1 = ttk.Label(self, text = "1. You can ask for help on a specific topic. Make sure it is a broad one.")
        self.Rules1.grid(row=2, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))

        self.Rules2 = ttk.Label(self, text = "2. Prefix your message with 'search' when requesting for urls")
        self.Rules2.grid(row=3, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))

        self.Rules2a = ttk.Label(self,
                                text="from the Bot")
        self.Rules2a.grid(row=4, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))


        self.Rules3 = ttk.Label(self, text="3. Make sure to use appropriate language - remember it is a bot and all")
        self.Rules3.grid(row=5, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))

        self.Rules3a = ttk.Label(self,
                                text="your conversations are recorded.")
        self.Rules3a.grid(row=6, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))


        self.Rules4 = ttk.Label(self, text="4. You must follow the KLASS Acceptable Use Policy at all times")
        self.Rules4.grid(row=7, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))

        self.Rules4a = ttk.Label(self,
                                text=" - Your chat will be recorded")
        self.Rules4a.grid(row=8, column=1, sticky="NSWE", padx=(10, 10), pady=(7.5, 0))

def openChatWindow(): #function to open the chatWindowInterface file with chat window
    os.system('python chatWindowInterface.py')  # opens the window


def emailReport(): #email function
    messagebox.showinfo("Success", "Email report has been sent") # message box is outputted with the following message

    conversation = open('ChatBotConversation.txt', 'r')  # opens the file with contents of the conversation
    conversationcontents = conversation.read()  # reads into the conversationcontents variable

    sender_email = "neamathbot@gmail.com"  # assigns sender email address

    with open("EntryDetails.txt", "r") as file: # opens the text file
        first_line = file.readline() # reads the first line
        for last_line in file: # for each line in the file
            pass # pass
        wholelastline = (list(last_line.split(","))) # the last line is split by commas and made into a list


    rec_email = wholelastline[2]  # assigns receiver's email address by indexing the 3rd element of the last line
    password = "MathBot123"  # password for the sender's email

    message = 'Subject: {}\n\n{}'.format("Your student used the MathBot. Find the conversation below:",
                                         conversationcontents)  # formats the subject header of the email

    server = smtplib.SMTP('smtp.gmail.com', 587)  # opens the server using port 587
    server.starttls()  # protocol starts negotiation between client and server; makes sure secure delivery of message (encrypted)
    server.login(sender_email, password)  # login to sender account using details

    server.sendmail(sender_email, rec_email, message)  # sends email using the sender and receiver email and message
    server.quit()  # closes the server connection with client

    messagebox.showinfo("Success", "Email report has been sent") # message box is outputted with the following message
    conversation.close()
    file = open("ChatBotConversation.txt", "w") # opens the file again
    file.close() # closes it without writing - leads to all contents being erased

class ChatWindowPage(ttk.Frame): #third tab - chat window
    def __init__(self, container):
        super().__init__()

        self.titleC = ttk.Label(self, text = "Chat") # label for title
        self.titleC.grid(column=1, row=1, padx=10, pady=15)

        self.openChatButton = ttk.Button(self, text="Open Chat Window", command=openChatWindow) # creates a button to open the chat window
        # command refers to the function openChatWindow()
        self.openChatButton.grid(row=4, column=6) # grids the button

        self.emailReport = ttk.Button(self, text="Generate & Send Conversation Report", command=emailReport) # creates a button to open the chat window
        self.emailReport.grid(row=6, column=6) # grids the button

class AdminPage(ttk.Frame): #fourth tab - Admin Login
    def __init__(self, container):
        super().__init__()

        self.titleD = ttk.Label(self, text="Admin Login") # creates label for title and grids it
        self.titleD.grid(column=1, row=1, padx=10, pady=15)

        self.uninput = ttk.Label(self, text="Username")  # creates label for username input
        self.uninput.grid(column=1, row=15, padx=5, pady=10)

        self.uninputbox = ttk.Entry(self, text="")  # creates entry box for the username
        self.uninputbox.grid(column=4, row=15)

        self.pwinput = ttk.Label(self, text="Password")  # creates label for password input
        self.pwinput.grid(column=1, row=20, padx=5, pady=10)

        self.pwinputbox = ttk.Entry(self, text="", show="*")  # creates entry box for the password
        self.pwinputbox.grid(column=4, row=20)

        loginbutton = ttk.Button(self, text="Login", command= self.login)  # login button command runs login function
        loginbutton.grid(column=2, row=30)

    def login(self): # method to login
        user_name = self.uninputbox.get() # gets the variable in the entry box and stores in variable
        password = self.pwinputbox.get() # gets the variable in the entry box and stores in variable

        hash_object = hashlib.sha256(bytes(password, encoding='utf8')) # checks the hash of the entered password
        hex_digest = hash_object.hexdigest() # uses the hash object to create has and stores in hex_digit

        actualpassword = "MathBotAdmin123*"  # actual password of the admin page
        hash_object = hashlib.sha256(bytes(actualpassword, encoding='utf8')) # creates a hash object after converting it to bytes
        hex_digest2 = hash_object.hexdigest() # stores the hashed object in the variable hex_dig2

        if user_name == "admin" and hex_digest == hex_digest2: # if the username and password are correct
            os.system('python adminPage.py') #admin page opens
        else: # else if it is not correct
            messagebox.showinfo("Login Fail", "Login Fail. Try Again") # error message is outputted

if __name__ == '__main__': # executes code if file run
    app = MainApplication() # class Main Application
    app.mainloop() # runs the application