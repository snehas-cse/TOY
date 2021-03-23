import tkinter
import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import *
import tkinter.messagebox

class candiate(object):
    def __init__(self, root1):
        self.root1 = root1
        self.root1.title("candiate")
        self.root1.geometry("1199x600+100+50")
        # frame creation
        Frame_login = Frame(self.root1, bg="white")
        Frame_login.place(x=230, y=80, height=500, width=800)
        # connecting database creating table view
        columns = ('job_id', 'job_name', 'location', 'discription', 'skills')
        table_list = ttk.Treeview(Frame_login, columns=columns, show='headings')
        table_list.column("job_id", anchor=CENTER, width=150)
        table_list.column("job_name", anchor=CENTER, width=150)
        table_list.column("location", anchor=CENTER, width=150)
        table_list.column("discription", anchor=CENTER, width=150)
        table_list.column("skills", anchor=CENTER, width=150)
        table_list.heading("job_id", text="job ID", anchor=CENTER)
        table_list.heading("job_name", text="job name", anchor=CENTER)
        table_list.heading("location", text="location", anchor=CENTER)
        table_list.heading("discription", text="discription", anchor=CENTER)
        table_list.heading("skills", text="skills", anchor=CENTER)
        db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha", database="jobdatabase")
        mycursor = db_connection.cursor()
        mycursor.execute("select job_id,job_name,location,discription,skills from job_table")
        records = mycursor.fetchall()
        for i, (job_id, job_name, location, discription, skills) in enumerate(records):
            table_list.insert("", 'end', values=(job_id, job_name, location, discription, skills))
            db_connection.close()
        table_list.pack(pady=20)
        table_list.bind('<Double-Button-1>')
        btn = tk.Button(Frame_login, text="Apply", fg="black", bd=0, font=("times new roman", 18),
                        command=lambda: [add_frame()])
        btn.place(x=300, y=280)
        #adding application frame
        def add_frame():
            Frame_login1 = Frame(self.root1, bg="white")
            Frame_login1.place(x=230, y=50, height=500, width=800)
            # firstname
            firstnamelabel = tk.Label(Frame_login1, text="first name:*", font=("times new roman", 13, "bold"),
                                      fg="black",
                                      bg="white").place(x=50, y=80)
            firstnametext = tk.StringVar()
            self.firstname = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray",
                                   textvariable=firstnametext)
            self.firstname.place(x=50, y=120, width=250, height=35)
            # last name
            lastnamelabel = tk.Label(Frame_login1, text="last name:*", font=("times new roman", 13, "bold"), fg="black",
                                     bg="white").place(x=50, y=170)
            lastnametext = tk.StringVar()
            self.lastname = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray", textvariable=lastnametext)
            self.lastname.place(x=50, y=210, width=250, height=35)
            # jobid
            jobidlabel = tk.Label(Frame_login1, text="job id:*", font=("times new roman", 13, "bold"), fg="black",
                                  bg="white").place(x=50, y=260)
            jobidtext = tk.StringVar()
            self.jobid = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray", textvariable=jobidtext)
            self.jobid.place(x=50, y=300, width=250, height=35)
            # email id
            emailidlabel = tk.Label(Frame_login1, text="Email id:*", font=("times new roman", 13, "bold"), fg="black",
                                    bg="white").place(x=400, y=80)
            emailidtext = tk.StringVar()
            self.emailid = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray", textvariable=emailidtext)
            self.emailid.place(x=400, y=120, width=250, height=35)
            # it skills
            itskillslabel = tk.Label(Frame_login1, text="IT skills:*", font=("times new roman", 13, "bold"), fg="black",
                                     bg="white").place(x=400, y=170)
            itskillstext = tk.StringVar()
            self.itskill = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray", textvariable=itskillstext)
            self.itskill.place(x=400, y=210, width=250, height=35)
            # year of experience
            yearlabel = tk.Label(Frame_login1, text="year of experience :*", font=("times new roman", 13, "bold"),
                                 fg="black",
                                 bg="white").place(x=400, y=260)
            yeartext = tk.StringVar()
            self.year = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray", textvariable=yeartext)
            self.year.place(x=400, y=300, width=250, height=35)
            # jobname
            jobnamelabel = tk.Label(Frame_login1, text="job name:*", font=("times new roman", 13, "bold"), fg="black",
                                    bg="white").place(x=50, y=360)
            jobnametext = tk.StringVar()
            self.jobname = Entry(Frame_login1, font=("times new roman", 12), bg="lightgray", textvariable=jobnametext)
            self.jobname.place(x=50, y=390, width=250, height=35)

            # submit button
            btn = tk.Button(Frame_login1, text="Submit", fg="black", bd=0, font=("times new roman", 18),
                            command=lambda: [insert_value(), removethis()])
            btn.place(x=420, y=450)
            btn = tk.Button(Frame_login1, text="Back", fg="black", bd=0, font=("times new roman", 18),
                            command=lambda: [candiate(root1)])
            btn.place(x=220, y=450)
            def insert_value():
                db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha",
                                                        database="jobdatabase")
                mycursor = db_connection.cursor()
                firstna = firstnametext.get()
                lastna = lastnametext.get()
                jobi = jobidtext.get()
                jobn = jobnametext.get()
                emaili = emailidtext.get()
                itskill = itskillstext.get()
                yeart = yeartext.get()
                if firstna != "" and lastna != "" and jobi != "" and jobn !="" and emaili !="" and itskill !="" and yeart !="":

                    try:
                        mycursor1 = "select count(1) from job_table where job_id= %s"
                        val = (jobi,)
                        mycursor.execute(mycursor1, val)

                        if mycursor.fetchone()[0]:

                            sql = (
                                "insert  into application_table (first_name ,last_name ,job_id,job_name,email_id ,it_skills ,yearofexp )" "values (%s,%s,%s,%s,%s,%s,%s)")
                            val = (firstna, lastna, jobi, jobn, emaili, itskill, yeart)
                            mycursor.execute(sql, val)
                            db_connection.commit()
                            tkinter.messagebox.showinfo("message", "Applied Sucessfully... ")
                        else:
                            tkinter.messagebox.showinfo("message", "Job Id not found... ")

                    except Exception as e:
                        print(e)
                else:
                    tkinter.messagebox.showinfo("message", "Mandatory field missing... ")
                    add_frame()

            def removethis():
                Frame_login1.destroy()



