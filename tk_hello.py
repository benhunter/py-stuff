# from Python Help


import tkinter
import tkinter.ttk as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.config(font=("Courier", 44))
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", command=root.destroy) # fg="red" not supported in ttk, use Style instead
        self.quit.pack(side="bottom")
        self.entrythingy = tk.Entry()
        self.entrythingy.pack()
        self.contents = tkinter.StringVar()
        self.contents.set("this is a variable")
        self.entrythingy["textvariable"] = self.contents
        self.entrythingy.bind('<Key-Return>', self.print_contents)

    def say_hi(self):
        print("hi there, everyone")

    def print_contents(self, event):
        print("contents: ", self.contents.get())

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
