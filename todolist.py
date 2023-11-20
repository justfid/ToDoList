import tkinter as tk
from tkinter import messagebox, simpledialog

class Window():
    def __init__(self):
        self.root = tk.Tk()

        #dimensions of screen
        screenWidth = 600
        screenHeight = 400
        #how many pixels from left side is padded
        xpad = 75
        defaultFont = ("Calibri", 12)

        self.root.geometry(f"{screenWidth}x{screenHeight}")
        self.root.title("To-Do List")
        #ensures screen size cant be changed
        self.root.resizable(False, False)
        
        title = tk.Label(self.root, text = "To-Do List", font = ("Calibri", 18))
        title.place(x=xpad, y=15)

        subtitle = tk.Label(self.root, text = "Enter Task Title:", font = ("Calibri", 14))
        subtitle.place(x=xpad, y=100)

        #box to type tasks in
        self.entry = tk.Entry(self.root, width = 20, font=("Calibri", 14))
        self.entry.place(x=xpad, y=140)

        #button to add a task - calls custom function
        add = tk.Button(self.root, text = "Add Task", width = 20, height=1, font = defaultFont, bg = "light grey", command = self.addTask)
        add.place(x=xpad, y=180)

        #binds enter key to the add task function
        self.root.bind("<Return>", self.addTask)

        #delete task button
        delete = tk.Button(self.root, text = "Delete Task", width = 20, height=1, font = defaultFont, bg = "light grey", command = self.deleteTask)
        delete.place(x=xpad, y=220)

        #delete all tasks button - calls a custom delete all function
        delete_all = tk.Button(self.root, text = "Delete All Tasks", width = 20, height=1, font = defaultFont, bg = "light grey", command = self.deleteAllTasks)
        delete_all.place(x=xpad, y=260)

        #exit button - calls custom save text function
        quit = tk.Button(self.root, text = "Exit", command = self.saveText, width = 20, height = 1, font = defaultFont, bg = "light grey")
        quit.place(x=xpad, y=300)

        #text box to keep track of index in list (starting from 1)
        self.indexBox = tk.Text(self.root, height = 14, width=3, font= ("Calibri", 12, "bold"))
        for counter in range(1,15):
            self.indexBox.insert("end",f"{counter})\n")
        self.indexBox.configure(state="disabled")
        self.indexBox.place(x= 315, y= 100)

        #text box
        self.outputText = tk.Text(self.root, height=14, width =20, font = defaultFont)
        #ensures text box cant be changed
        self.outputText.configure(state="disabled")
        self.outputText.place(x= 350, y= 100)

        self.loadText()
        #if x button pressed, causes a save
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()


    def addTask(self, event = None):
        #adds a task and ensures no duplicated - event parameter needed, idk why
        self.outputText.configure(state="normal")
        task = self.entry.get()
        #strips task to get rid of white space
        strippedTask = task.lstrip().rstrip()
        #checks if box is empty
        if not len(strippedTask):
            pass
        #checks if stripped task is in the list already. The \n's stop boundary case errors.
        elif f"\n{strippedTask}\n" in f"\n{self.outputText.get('1.0', 'end')}":
            messagebox.showerror("To-Do List", "Task already exists")
        else:
            self.entry.delete(0,len(task))
            self.outputText.insert("end", f"{strippedTask}\n")

        self.outputText.configure(state="disabled")


    def deleteTask(self):
        #deletes a specific task based off its position
        self.outputText.configure(state="normal")
        valid = False

        while not valid:
            userPrompt = "What Task Do You Want To Delete \n(Enter a number that corresponds to the task's position in list)"
            userInput = simpledialog.askstring(title="Delete", prompt=userPrompt)
            try:
                userInput = int(userInput)
            except ValueError:
                pass
            else:
                valid = True

        self.outputText.delete(f"{userInput}.0", f"{userInput + 1}.0")
        self.outputText.configure(state="disabled")


    def deleteAllTasks(self):
        #deletes all tasks
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0",tk.END)
        self.outputText.configure(state="disabled")


    def saveText(self):
        #saves the tasks to a txt file, and closes window
        textFile = open("Todo.txt", "w")
        textFile.write(self.outputText.get("1.0", "end"))
        textFile.close()
        self.root.destroy()

    def loadText(self):
        #loads text from txt file, and gets rid of a \n
        textFile = open("Todo.txt", "r")
        content = textFile.read()
        self.outputText.configure(state="normal")
        self.outputText.insert("end",content)
        self.outputText.delete("end-1c", "end")
        self.outputText.configure(state="disabled")
        textFile.close()

    
    def on_close(self):
        #function overriding the x button mechanism
        close = messagebox.askokcancel("Close", "Do you want to quit?")
        if close:
            self.saveText()
    
def main():
    Window()

if __name__ == "__main__":
    main()

    #further improvement later: 
    #change text box to list box to make tasks clickable to delete
