from tkinter import * #imports everything from tkinter
from tkinter import messagebox #imports message box function
import subprocess #imports subprocess to open text file using appropriate software - textedit
import hashlib #imports library for hashing
import heapq # imports heapq for the priority queue

master = Tk() #roots tkinter
master.title("Admin Page") #gives the window a title
master.geometry("450x400") #assigns dimensions

labelMain = Label(master, text = "Admin Page") # labels title on page
labelMain.grid(column=4, row=3, padx = 10, pady = 15) # uses the grid coordinates to position the label
labelMain.config(font=('Helvetica bold',30)) #changes font and size to make it bigger

label2 = Label(master, text = "Login success") #label to indicate login success from main interface page
label2.grid(column=2, row=2, padx=5, pady=15) #uses grid coordinates to position the label

def openTextFile(): #function to open the Entry Details file
    subprocess.call(['open', '-a', 'TextEdit', "EntryDetails.txt"]) #opens the file in append mode using the text edit app (for MAC users)
    originalhash = hashing("EntryDetails.txt") # stores the hash of the file in the variable originalhash
    h = open("hashedoriginal.txt", "w")
    h.write(originalhash)
    return originalhash # returns original hash value


def hashing(file): #hashing algorithm for the EntryDetails text file
    BLOCK_SIZE = 65536  # indicated the size of each read from the file in bytes
    file_hash = hashlib.sha256() # creates the hash object
    with open(file, 'rb') as f: # open the file to read bytes
        fb = f.read(BLOCK_SIZE) # reads the file. Take in the amount declared above
        while len(fb) > 0: # while there is still data being read from the file
            file_hash.update(fb) # updates the hash
            fb = f.read(BLOCK_SIZE) # reads the next block from the file
    hashedvalue = file_hash.hexdigest() # gets the hexadecimal digest of the hash
    return hashedvalue

h = open("hashedoriginal.txt","r") #opens file containing original hash of the entrydetails.txt file as soon as an entry has been made on the main interface page
originalHash = h.readline() #reads the hash on the first line
h.close() #closes the file

def verifyHash(): #function to verify the hash and ensure the file hasn't been intercepted
    if hashing("EntryDetails.txt") == originalHash: #compares the hash of the file to the hash indicated in the 'hashedoriginal.txt' file
        messagebox.showinfo("Verified", "Hash verified")# if they are the same, the appropriate message box is shown
    else:
        messagebox.showinfo("Error", "Incorrect Hash") # if they are not the same, the message box with error message is outputted

openFileButton = Button(master, text = "  Open Student Details File  ", command = openTextFile) #button to open the text file
openFileButton.grid(column=4, row = 10, pady=15) # grids the button with column 4 and row 10
openFileButton.config(font=(20)) # makes the font size 20

hashButton = Button(master, text = "  Verify Hash  ", command = verifyHash) # button to verify the hash; carries out the verifyHash function
hashButton.grid(column=4, row = 15, pady=15) # grids the button with column 4 and row 15
hashButton.config(font=(20)) # makes the font size 20

options = [ # options for the dropdown menu
" - Select option - ",
"Most used year groups",
"Most viewed topics",
"Most frequently used user",
"Highest priority student",
]

variable = StringVar(master)
variable.set(options[0]) # default value

labelStatistics = Label(master, text = "Show Statistics of Student Details" )  # label to show the statistics of students
labelStatistics.config(font=("Helvetica bold", 15)) # makes the font helvetica bold and font size 15
labelStatistics.grid(column = 4, row = 20, pady = 15) # grids int in the frame at column 4 and row 20 with a y padding of 15
choice = OptionMenu(master, variable, *options) # creates a dropdown menu using 'OptionMenu' and the options in the list 'options'
choice.grid(column=4, row=25, pady = 30) # grids the dropdown menu accordingly

f = open("EntryDetails.txt","r") # opens the file in read mode

class PriorityQueue:
    def __init__(self):
        self._data = [] # list to store elements
        self._index = 0 # index to keep track of where to insert (counter)
    def push(self, item, priority): # method to add elements to the queue in order of priority
        heapq.heappush(self._data, (-priority, self._index, item)) # inserts items such that the first element of the queue has the lowest priority
        #inserted as a tuple so the highest priority member is the first element of the queue
        self._index += 1 # counter for the index - incremented by one
    def pop(self): # method to return the person with the highest priority
        return heapq.heappop(self._data)[-1] # takes the list with elements and only returns the 'Person' from tuple

class Person: # class to add the name of the student
    def __init__(self, name):
        self.name = name # name of the student
    def __str__(self):
        return f'{self.name}' # f string to return the name of the person

queue = PriorityQueue() # instantiates an object

def converttolist(string): # function to convert a string to list
    listversion = list(string.split(",")) # splits with the commas
    return listversion # returns the list


allYeargroups = []  # empty list to append all yeargroups to
allTopics = [] # empty list to append all topics to
allNames = []   # empty list to append all names to

for line in f:  # for loop to repeat for each line in the text file
    strip_lines = line.strip()  # strips the line
    listed = converttolist(strip_lines) # converts the stripped lines into a list
    name = listed[0]  # takes the name from the list by indexing the first element
    yeargroup = (int(listed[1])) # takes the priority by using the year group as a value and converting to a integer
    topic = listed[3]  # uses index 3 to find the topic
    allTopics.append(topic) # appends all the topics to the empty list 'allTopics'
    allYeargroups.append(yeargroup)  # appends all the yeargroups to the empty list 'allYearGroups'
    allNames.append(name)  # appends all the names to the empty list 'allNames'
    queue.push(Person(name), yeargroup)  # pushes each person to the queue

f.close()  # closes the file


def count(tobefound, list): # RECURSION
    if not list: # if list is empty
        return 0 # returns 0
    elif tobefound == list[0]: # if the item to be found is the first element
        return 1 + count(tobefound, list[1:]) # returns 1 plus the value of the next recursion
    else: # if the first element is not the element to be found
        return 0 + count(tobefound, list[1:]) # returns 0 plus the value of next recursion



def findMaxYearGroup(): # function to find the maximum frequency
    # finds the count for all the year groups using the count function and the year groups list as a parameter
    yr7 = count(7, allYeargroups)
    yr8 = count(8, allYeargroups)
    yr9 = count(9, allYeargroups)
    yr10 = count(10, allYeargroups)
    yr11 = count(11, allYeargroups)
    yr12 = count(12, allYeargroups)
    yr13 = count(13, allYeargroups)

    YrGroupCounts = {yr7: "Year 7", yr8: "Year 8", yr9: "Year 9", yr10: "Year 10", yr11: "Year 11", yr12: "Year 12", yr13: "Year 13"} # creates the dictionary for the count of each yeargroup
    return("The most used year group is", YrGroupCounts.get(max(YrGroupCounts))) # returns the variable name holding the maximum count


def FrequentString(list): # function to find the most frequently occuring string in a list
    return max(set(list), key=list.count) # returns the maximum of the set of list - key is the count of the list set


def responseStat(): # function to return the answer for the chosen statistic
    if variable.get() == "Most used year groups": # if the chosen option from the drop down menu is "Most used year groups"
        try: # exception handling
            messagebox.showinfo("Most Used year groups", findMaxYearGroup()) # message box outputted with the return from findMaxYearGroup function
        except:
            messagebox.showinfo("Error", "Try again") # error message is outputted
    elif variable.get() == "Most viewed topics":  # if the chosen option from the drop down menu is "Most viewed topics"
        try: # exception handling
            messagebox.showinfo("Most used viewed topics", FrequentString(allTopics)) # message box outputted with the return from FrequentString function and allTopics list as parameter
        except:
            messagebox.showinfo("Error", "Try again")  # error message is outputted

    elif variable.get() == "Most frequently used user":  # if the chosen option from the drop down menu is "Most frequently used user"
        try: # exception handling
            messagebox.showinfo("Most Frequently used student", FrequentString(allNames))
        except:
            messagebox.showinfo("Error", "Try again")  # error message is outputted

    elif variable.get() == "Highest priority student":  # if the chosen option from the drop down menu is "Highest priority student"
        try: # exception handling
            messagebox.showinfo("Highest Priority Member", (queue.pop())) # message box outputted with the forst priority member of the queue
        except:
            messagebox.showinfo("Error", "Try again")  # error message is outputted
    elif variable.get() == " - Select option - ": # if the chosen option from the drop down menu is "Select option"
        messagebox.showinfo("", "Please select an option") # error message is outputted to choose an option

button = Button(master, text="Compute", command=responseStat) # button to provide the appropriate output using the function responseStat
button.grid(column = 4, row=35) # grids the button with column 4 and row 35

mainloop() # runs the page