import tkinter as tk
from tkinter import *
import tkinter.messagebox
from project.candiate import candiate
from project.recruiter import Recruiter

class login(object):
    def __init__(self, root):
        self.root = root
        self.root.title("login page")
        self.root.geometry("1199x600+100+50")
        #Frame_login = Frame(self.root, bg="white")
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=350, y=150, height=340, width=500)
        title = Label(Frame_login, text="login here", font=("impact", 35, "bold"), fg="black", bg="white").place(x=90,
                                                                                                                  y=30)
        unamelabel = tk.Label(Frame_login, text="enter your username:", font=("Goudy old style", 14, "bold"), fg="gray",
                              bg="white").place(x=90, y=140)
        unnametext = tk.StringVar()
        self.txt_user = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", textvariable=unnametext)
        self.txt_user.place(x=90, y=170, width=350, height=35)
        btn = tk.Button(Frame_login, text="login", fg="black",  bd=0, font=("times new roman", 18),
                        command=lambda: [retrieve_input()])
        btn.place(x=150, y=280)
        #getting input from the user

        def retrieve_input():
            inputvalue = unnametext.get()
            if (inputvalue == ("recruiter@screel.in")):
                root.destroy()
                root1 = Tk()
                obj = Recruiter(root1)
                root1.mainloop()
            elif (inputvalue == ("candidate@screel.in")):
                root.destroy()
                root1 = Tk()
                obj = candiate(root1)
                root1.mainloop()
            else:
                tkinter.messagebox.showinfo("error", "Invalid user name ")
                login(root)
root = Tk()
ob = login(root)
root.mainloop()