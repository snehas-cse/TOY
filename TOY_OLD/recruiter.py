import tkinter
import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import ttk
import tkinter.messagebox
class Recruiter(object):
    def __init__(self, root1):
        self.root1 = root1
        self.root1.title("recruiter")
        self.root1.geometry("1199x600+100+50")
        # creating frame
        Frame_login = Frame(self.root1, bg="white")
        Frame_login.place(x=230, y=80, height=500, width=800)
        create_btn = tk.Button(Frame_login, text="Create Table", font=("times new roman", 18), width=20,
                               command=lambda: create_table())
        create_btn.place(x=80, y=100)
        upset_btn = Button(Frame_login, text="Insert/Update Record", font=("times new roman", 18), width=20,
                           command=lambda: upset_table())
        upset_btn.place(x=80, y=200)
        delete_btn = Button(Frame_login, text="Delete Records", font=("times new roman", 18), width=20,command=lambda:delete())
        delete_btn.place(x=400, y=100)
        list_btn = Button(Frame_login, text=" Job Table List", font=("times new roman", 18), width=20,command=lambda:job_list_table())
        list_btn.place(x=400, y=200)
        applicant_list_btn = Button(Frame_login, text=" Applicant Table list", font=("times new roman", 18), width=20,
                            command=lambda: applicant_list())
        applicant_list_btn.place(x=230, y=310)

        db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha", database="jobdatabase")
        self.my_query = db_connection.cursor()

        #creating table in database if not exist
        def create_table():
            db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha",
                                                    database="jobdatabase")
            self.mycreate_query=db_connection.cursor()
            try:
                sql = "create table job_table (job_id varchar(8) primary key not null,job_name varchar(20),location varchar(15),discription varchar(25),skills varchar(25));"
                self.mycreate_query.execute(sql)
                tkinter.messagebox.showinfo("message", "Table created")
                Recruiter(root1)
            except Exception as e:
                tkinter.messagebox.showinfo("message", "Table already exist.")
                Recruiter(root1)

        #update or insert record into table
        def upset_table():
            upset_frame = Frame(self.root1, bg="white")
            upset_frame.place(x=230, y=80, height=500, width=800)
            # job id
            job_id_label1 = tk.Label(upset_frame, text="job id:", font=("times new roman", 13, "bold"), fg="black",
                                     bg="white").place(x=50, y=80)
            job_id_text = tk.StringVar()
            self.txt_user1 = Entry(upset_frame, font=("times new roman", 12), bg="lightgray", textvariable=job_id_text)
            self.txt_user1.place(x=50, y=120, width=250, height=35)
            # job name
            job_name_label1 = tk.Label(upset_frame, text="job name:", font=("times new roman", 13, "bold"), fg="black",
                                       bg="white").place(x=50, y=170)
            job_name_text = tk.StringVar()
            self.txt_user2 = Entry(upset_frame, font=("times new roman", 12), bg="lightgray",
                                   textvariable=job_name_text)
            self.txt_user2.place(x=50, y=210, width=250, height=35)
            # location
            job_location_label1 = tk.Label(upset_frame, text="location:", font=("times new roman", 13, "bold"),
                                           fg="black",
                                           bg="white").place(x=50, y=260)
            job_location_text = tk.StringVar()
            self.txt_user3 = Entry(upset_frame, font=("times new roman", 12), bg="lightgray",
                                   textvariable=job_location_text)
            self.txt_user3.place(x=50, y=300, width=250, height=35)
            # description
            job_desc_label1 = tk.Label(upset_frame, text="description:", font=("times new roman", 13, "bold"),
                                       fg="black",
                                       bg="white").place(x=400, y=80)
            job_desc_text = tk.StringVar()
            self.txt_user4 = Entry(upset_frame, font=("times new roman", 12), bg="lightgray",
                                   textvariable=job_desc_text)
            self.txt_user4.place(x=400, y=120, width=250, height=35)
            # skills
            job_skills_label1 = tk.Label(upset_frame, text="skills:", font=("times new roman", 13, "bold"),
                                         fg="black",
                                         bg="white").place(x=400, y=170)
            job_skill_text = tk.StringVar()
            self.txt_user5 = Entry(upset_frame, font=("times new roman", 12), bg="lightgray",
                                   textvariable=job_skill_text)
            self.txt_user5.place(x=400, y=210, width=250, height=35)
            # submit button
            btn = tk.Button(upset_frame, text="  Submit ", fg="black", bd=0, font=("times new roman", 18),command=lambda:[inserting()])
            btn.place(x=440, y=380)
            #back button
            def removethis():
                root1.destroy()
            btn2 = tk.Button(upset_frame, text="  Back   ", fg="black", bd=0, font=("times new roman", 18),command=lambda:[back_frame()])
            btn2.place(x=220, y=380)
            def back_frame():
                Recruiter(root1)
            #getting input from user and insert into dadabase
            def inserting():
                db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha",
                                                        database="jobdatabase")
                mycursor = db_connection.cursor()
                job_id = job_id_text.get()
                job_name =job_name_text.get()
                location = job_location_text.get()
                discription = job_desc_text.get()
                skills = job_skill_text.get()
                if job_id!="" and job_name != "" and location != "" and discription != "" and skills !="" :
                    sql = "replace into job_table ( job_id ,job_name ,location ,discription,skills  )" "values (%s,%s,%s,%s,%s)"
                    val = (job_id, job_name, location, discription, skills)
                    mycursor.execute(sql, val)
                    db_connection.commit()
                    tkinter.messagebox.showinfo("message", "recored inserted sucessfully....")
                    upset_table()
                else:
                    tkinter.messagebox.showinfo("message", "Mandratory field missing....")
                    upset_table()

        # Deleting records from the table
        def delete():
            delete_frame = Frame(self.root1, bg="white")
            delete_frame.place(x=230, y=80, height=500, width=700)
            job_id_label1 = tk.Label(delete_frame, text="enter job id for delete record:", font=("times new roman", 13, "bold"), fg="black",
                                     bg="white").place(x=250, y=180)
            delete_text = tk.StringVar()
            self.txt_user1 = Entry(delete_frame, font=("times new roman", 12), bg="lightgray", textvariable=delete_text)
            self.txt_user1.place(x=250, y=240, width=250, height=35)
            btn = tk.Button(delete_frame, text="  Submit  ", fg="black", bd=0, font=("times new roman", 18),
                            command=lambda: [deleting()])
            btn.place(x=410, y=380)
            btn = tk.Button(delete_frame, text="  Back  ", fg="black", bd=0, font=("times new roman", 18),
                            command=lambda:[back_button()])
            btn.place(x=250, y=380)
            def back_button():
                Recruiter(root1)
            def deleting():
                deletevalue = delete_text.get()
                db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha",
                                                        database="jobdatabase")
                mycursor = db_connection.cursor()
                mycursor1 = "select count(1) from job_table where job_id= %s"
                val = (deletevalue,)
                mycursor.execute(mycursor1, val)
                if mycursor.fetchone()[0]:
                    sql = "delete from job_table where job_id = %s"
                    val = (deletevalue,)
                    mycursor.execute(sql, val)
                    db_connection.commit()
                    tkinter.messagebox.showinfo("message", "Sucessfully deleted.. ")
                    Recruiter(root1)
                else:
                    tkinter.messagebox.showwarning("error","Job Id Not Found..")
                    delete()
            #closing frame
            def removethis(self):
                root1.destroy()

        #listing job_table
        def job_list_table():
            list_frame = Frame(self.root1, bg="white")
            list_frame.place(x=230, y=80, height=500, width=800)
            btn = tk.Button(list_frame, text="  Back  ", fg="black", bd=0, font=("times new roman", 18),
                            command=lambda:[back_button()])
            btn.place(x=280, y=380)
            def back_button():
                Recruiter(root1)
            columns = ('job_id', 'job_name', 'location', 'discription', 'skills')
            table_list1 = ttk.Treeview(list_frame, columns=columns, show='headings')
            table_list1.column("job_id", anchor=CENTER, width=120)
            table_list1.column("job_name", anchor=CENTER, width=150)
            table_list1.column("location", anchor=CENTER, width=150)
            table_list1.column("discription", anchor=CENTER, width=150)
            table_list1.column("skills", anchor=CENTER, width=150)
            table_list1.heading("job_id", text="job ID", anchor=CENTER)
            table_list1.heading("job_name", text="job name", anchor=CENTER)
            table_list1.heading("location", text="location", anchor=CENTER)
            table_list1.heading("discription", text="discription", anchor=CENTER)
            table_list1.heading("skills", text="skills", anchor=CENTER)
            table_list1.pack(pady=10)
            db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha",
                                                    database="jobdatabase")
            mycursor = db_connection.cursor()
            mycursor.execute("select job_id,job_name,location,discription,skills from job_table")
            records = mycursor.fetchall()
            for i, (job_id, job_name, location, discription, skills) in enumerate(records):
                table_list1.insert("", 'end', values=(job_id, job_name, location, discription, skills))
                db_connection.close()
            table_list1.pack(pady=20)

        # listing application table
        def applicant_list():
            applicant_login = Frame(self.root1, bg="white")
            applicant_login.place(x=230, y=80, height=500, width=800)
            btn = tk.Button(applicant_login, text="  Back  ", fg="black", bd=0, font=("times new roman", 18),
                            command=lambda:[back_button()])
            btn.place(x=250, y=380)
            def back_button():
                Recruiter(root1)
            columns = ('first_name', 'last_name', 'job_id', 'job_name', 'email_id','it_skills','yearofexp')
            table_list = ttk.Treeview(applicant_login, columns=columns, show='headings')
            table_list.column("job_id", anchor=CENTER, width=100)
            table_list.column("first_name", anchor=CENTER, width=100)
            table_list.column("last_name", anchor=CENTER, width=100)
            table_list.column("job_name", anchor=CENTER, width=100)
            table_list.column("email_id", anchor=CENTER, width=100)
            table_list.column("it_skills", anchor=CENTER, width=100)
            table_list.column("yearofexp", anchor=CENTER, width=100)
            table_list.heading("first_name", text="first_name", anchor=CENTER)
            table_list.heading("last_name", text="last name", anchor=CENTER)
            table_list.heading("job_id", text="job id", anchor=CENTER)
            table_list.heading("job_name", text="job name", anchor=CENTER)
            table_list.heading("email_id", text="email id", anchor=CENTER)
            table_list.heading("it_skills", text="It skills", anchor=CENTER)
            table_list.heading("yearofexp", text="year of exp", anchor=CENTER)
            table_list.pack(pady=10)
            db_connection = mysql.connector.connect(host="localhost", user="root", password="Sneha",
                                                    database="jobdatabase")
            mycursor = db_connection.cursor()
            mycursor.execute("select * from application_table")
            records = mycursor.fetchall()
            for i, (first_name,last_name,job_id, job_name, email_id, it_skills, yearofexp) in enumerate(records):
                table_list.insert("", 'end', values=(first_name, last_name, job_id, job_name, email_id,it_skills,yearofexp))
                db_connection.close()
            table_list.pack(pady=20)

