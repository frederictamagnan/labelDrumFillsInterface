import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None,width=300, height=100, **kwarg):
        super().__init__(master)
        self.master.geometry("1000x1000")  # You want the size of the app to be 500x500
        self.master.resizable(0, 0)
        self.create_widgets()
        self.pack(side="left")


    def create_widgets(self):
        self.hi_there = tk.Button(self,width=300)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="bottom")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
myapp = App(master=root)

# create the application


#
# here are method calls to the window manager class
#


# start the program
myapp.mainloop()
