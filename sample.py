import tkinter
import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import *
import tkinter.messagebox
import sqlite3
from fastapi import FastAPI
import json
app=FastAPI()
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

        @app.get("/select")
        async def get_all():
            conn = sqlite3.connect("jobdatabases.db")
            cursor = conn.execute("select job_id,job_name,location,discription,skills from job_table;")
            object_list = cursor.fetchall()
            print((object_list))
            #y = json.dumps(object_list)
            for i, (job_id, job_name, location, discription, skills) in enumerate(object_list):

                #table_list.insert("", 'end', values=(job_id, job_name, location, discription, skills))

                print(object_list)
                print("values")

            return object_list

        table_list.pack(pady=20)


root1 = Tk()
obj = candiate(root1)
root1.mainloop()
