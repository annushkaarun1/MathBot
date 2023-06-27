from tkinter import *
#from chat import get_response, bot_name
from chatFunction import final_Response #imports the function from chatFunction.py file

bg_gray = "#03045e"
bg_colour = "#457b9d"
text_colour = "#EAECEE"
font = "Helvetica 14"
boldedFont = "Helvetica 13 bold"

class ChatApplication:  # creates a class for the whole application
    def __init__(self): # constructor
        self.window = Tk()  # creates tkinter root
        self._setup_main_window() #setup main window method is run

    def runscreen(self): # run method just runs the app using mainloop()
        self.window.mainloop()

    def _setup_main_window(self): # method to set up main window
        self.window.title("MathBot") # assigns title
        self.window.resizable(width=False, height=False) # makes it non resizeable
        self.window.configure(width=470, height=550, bg=bg_colour) # assigns height and width with background colour


        # creates head label
        head_label = Label(self.window, bg="#001219", fg=text_colour,
                           text="Welcome to MathBot", font=boldedFont, pady=10)
        head_label.place(relwidth=1) # places it with relative width of 1

        # creates tiny divider
        line = Label(self.window, width=450, bg=bg_gray)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=15, height=2, bg=bg_colour, fg=text_colour, font=font, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED) # when hovered over, cursor turns arrow

        # creates a bottom label
        bottom = Label(self.window, bg=bg_gray, height=80)
        bottom.place(relwidth=1, rely=0.825)
        # message entry box for user input
        self.msg_entry = Entry(bottom, bg="#1a759f", fg=text_colour, font=font)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus() # focus function makes the entry box more active
        self.msg_entry.bind("<Return>", self._on_enter_pressed) # on enter pressed function called

        # send button
        send_button = Button(bottom, text="Send", font=boldedFont, width=20, bg=bg_gray,
                             command=lambda: self._on_enter_pressed(None)) #command calls the on enter pressed function
        send_button.place(relx=0.55, rely=0.008, relheight=0.06, relwidth=0.22)

        # end button
        end_button = Button(bottom, text = "End", font=boldedFont, width = 10, bg = bg_gray, command=lambda: self._on_end_pressed(None)) # adds the function of on end pressed to the button
        #command calls the on end pressed function
        end_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22) # places the end buttone using the place function of tkinter

    def _on_end_pressed(self,event):  # when end is pressed, the screen is destroyed and closed leading back to original interface
        self.window.destroy() # the root window is closed


    def _on_enter_pressed(self, event): # function adds the user input to the window screen
        msg = self.msg_entry.get() # gets the entered message
        self._insert_message(msg, "You") # calls the insert message function to enter the user's message with 'You'

    def _insert_message(self, msg, sender): # method to insert message
        if not msg: # if it is empty
            return # returns nothing

        self.msg_entry.delete(0, END) # deletes the message from the box and appends to screen
        msg1 = f"{sender}: {msg}\n\n" # f string to format the message entry
        self.text_widget.configure(state=NORMAL) # the widget is enabled (NORMAL)
        self.text_widget.insert(END, msg1) # inserts the message
        self.text_widget.configure(state=DISABLED) # the widget is disabled

        bot_name = "MathBot" # assigns the name of the bot

        msg2 = f"{bot_name}: {final_Response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2) # inserts the second message which has been initialised in the previous line
        self.text_widget.configure(state=DISABLED) # sets the text widget to be disabled
        self.text_widget.see(END) # the method 'see' allows it to be shown on the screen

if __name__ == "__main__": # runs the application
    app = ChatApplication() # instantiates the class
    app.runscreen() # run