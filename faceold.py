import os
import tkinter as tk
import sqlite3
from PIL import Image,ImageTk
from tkinter import messagebox as tm
import numpy as np
import cv2
import pickle
import smtplib
from pynput.keyboard import Key , Controller


keyboard= Controller()
V_LARGE_F = ("Verdana" ,24)
VV_LARGE_F = ("Verdana" ,33)
Large_F = ("Verdana" , 21)
Nor_F = ("Verdana" , 16)
Sm_F = ("Verdana", 12)
V_S_F = ("Verdana", 10)

'''conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Admin(a_id INTEGER primary key AUTOINCREMENT ,af_name varchar(10),al_name varchar(10),mob_no char(10),email varchar(10),password varchar(10) )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute("INSERT INTO Admin(af_name,al_name,mob_no,email,password) values('xyz','abc',4567894,'kdgdfgdh','123')" )
conn.commit()        

conn=sqlite3.connect('face.db')
c=conn.cursor()
00c.execute('CREATE TABLE IF NOT EXISTS Faculty(f_id INTEGER primary key AUTOINCREMENT ,ff_name varchar(10),fl_name varchar(10),mob_no char(10),email varchar(10),password varchar(10) )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute("INSERT INTO Faculty(ff_name,fl_name,mob_no,email,password) values('abc','abc',4567894,'kdgdfgdh','123')" )
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Student(s_id INTEGER primary key AUTOINCREMENT ,sf_name varchar(10),sl_name varchar(10),mob_no char(10),email varchar(10),course varchar(10) ,year INTEGER )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute("INSERT INTO Student(sf_name,sl_name,mob_no,email,course,year) values('abcs','abc',4567894,'kdgdfgdh','bca',3)" )
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS s1Attendence(s_id INTEGER primary key AUTOINCREMENT ,classes INTEGER )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS s2Attendence(s_id INTEGER primary key AUTOINCREMENT ,classes INTEGER )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS s3Attendence(s_id INTEGER primary key AUTOINCREMENT ,classes INTEGER )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS s4Attendence(s_id INTEGER primary key AUTOINCREMENT ,classes INTEGER )')
conn.commit()


conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS s5Attendence(s_id INTEGER primary key AUTOINCREMENT ,classes INTEGER )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS s6Attendence(s_id INTEGER primary key AUTOINCREMENT ,classes INTEGER )')
conn.commit()

conn=sqlite3.connect('face.db')
c=conn.cursor()
c.execute("INSERT INTO s1attendence(classes) values(0)" )
c.execute("INSERT INTO s2attendence(classes) values(0)" )
c.execute("INSERT INTO s3attendence(classes) values(0)" )

c.execute("INSERT INTO s4attendence(classes) values(0)" )

c.execute("INSERT INTO s5attendence(classes) values(0)" )

c.execute("INSERT INTO s6attendence(classes) values(0)" )

conn.commit()'''




class collegeapp(tk.Tk):         
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"sample")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        b1=tk.Button(self,text="Quit",fg="black",bg="orange",relief="raised",width=5,font=Sm_F,command=lambda:self.destroy())
        b1.place(x=1260,y=10)
        
        self.frames = {}
        
        for F in (LoginPage,AdminPage,FacultyPage,TakeAttendencePage,ViewStatusPage,AddStudentPage,SendEmailPage): 
            frame = F(container,self)
            self.frames[F]= frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)     

   
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

    def get_page(self,page_class):
        return self.frames[page_class]

class  LoginPage(tk.Frame) :
    
    def __init__(self,parent,controller):
        self.controller=controller
        tk.Frame.__init__(self,parent)
        
        c1 = tk.Canvas(self)       
        c1.pack(fill="both", expand=True)
        
        '''load = Image.open("m.jpg")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(0,0,image = img.image,anchor = "nw")  
        load = Image.open("UI__26-512.png")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(160,380,image = img.image,anchor = "nw")'''
        c1.create_text(200,480, text="Admin ID",font = 12) 
        c1.create_text(200,560, text="Password",font = Sm_F)
        E1 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3) 
        E2 = tk.Entry(self, state="normal",font=Sm_F, width=20, bd=3, show="**")
        E1.focus_set() 
        E1.place(x=250, y=470)  
        E2.place(x=250, y=550)

        B1=tk.Button(self, text="Submit",font=Sm_F,fg="black",bg="lightblue",relief="raised",width=10,command=lambda:check(E1,E2))
        B1.place(x=250, y=650)
        
        def check(E1,E2):
            conn=sqlite3.connect('face.db')
            c=conn.cursor()
            f=E1.get()
            g=E2.get()
            find=("select * from Admin WHERE a_id=? AND password=?")
            c.execute(find,[(f),(g)])
            result=c.fetchall()
            if result:
                controller.show_frame(AdminPage)
            else:
                tm.showerror('login','username or password is incorrect')
                c.close()
                conn.close()
        '''load = Image.open("UI__26-512.png")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(660,380,image = img.image,anchor = "nw")'''    
        c1.create_text(700,480, text="Faculty ID",font = 12) 
        c1.create_text(700,560, text="Password",font = Sm_F)
        E3 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3) 
        E4 = tk.Entry(self, state="normal",font=Sm_F, width=20, bd=3, show="**")
        E3.focus_set() 
        E3.place(x=750, y=470)  
        E4.place(x=750, y=550)

        B1=tk.Button(self, text="Submit",font=Sm_F,fg="black",bg="lightblue",relief="raised",width=10,command=lambda:check1(E3,E4))
        B1.place(x=750, y=650)
        
        
        
        def check1(E1,E2):
            conn=sqlite3.connect('face.db')
            c=conn.cursor()
            f=E1.get()
            g=E2.get()
            find=("select * from Faculty WHERE f_id=? AND password=?")
            c.execute(find,[(f),(g)])
            result=c.fetchall()
            if result:
                controller.show_frame(FacultyPage)
            else:
                tm.showerror('login','username or password is incorrect')
                c.close()
                conn.close()    







       
class AdminPage(tk.Frame):
    def __init__(self,parent,controller):
        self.controller=controller
        tk.Frame.__init__(self,parent)
        
        c1 = tk.Canvas(self)       
        c1.pack(fill="both", expand=True)

        '''load = Image.open("Attendance.jpg")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(0,0,image = img.image,anchor = "nw")  
        load = Image.open("UI__26-512.png")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(160,380,image = img.image,anchor = "nw")'''
       
        b1=tk.Button(self,text="Back",fg="black",bg="orange",relief="raised",width=5,font=Sm_F,command=lambda:controller.show_frame(LoginPage))
        b1.place(x=20,y=10)
        
        B1=tk.Button(self, text="Add a student ",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25,command=lambda:controller.show_frame(AddStudentPage))
        B1.place(x=500, y=300)
        B2=tk.Button(self, text="Send an alert",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25,command=lambda:controller.show_frame(SendEmailPage))
        B2.place(x=500, y=370)

class AddStudentPage(tk.Frame):
    def __init__(self,parent,controller):
            self.controller=controller
            tk.Frame.__init__(self,parent)
        
            c1 = tk.Canvas(self)       
            c1.pack(fill="both", expand=True)
            '''load = Image.open("aaa.jpg")
            render = ImageTk.PhotoImage(load)   
            img = tk.Label(image=render)        
            img.image = render
            c1.create_image(0,0,image = img.image,anchor = "nw")'''
            
            c1.create_text(520,200, text="Add the student details",font = Sm_F ,fill="black")
            c1.create_text(520,250, text="First Name",font = Sm_F ,fill="black",justify="left")
            E1 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E1.focus_set() 
            E1.place(x=640, y=240)

            c1.create_text(520,300, text="Last Name",font = Sm_F ,fill="black",justify="left")
            E2 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E2.focus_set() 
            E2.place(x=640, y=290)

            c1.create_text(520,350, text="mobile",font = Sm_F ,fill="black",justify="left")
            E3 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E3.focus_set() 
            E3.place(x=640, y=340)

            c1.create_text(520,400, text="email id",font = Sm_F ,fill="black",justify="left")
            E4 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E4.focus_set() 
            E4.place(x=640, y=390)

            c1.create_text(520,450, text="course",font = Sm_F ,fill="black",justify="left")
            E5 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E5.focus_set() 
            E5.place(x=640, y=440)

            
            c1.create_text(520,500, text="year",font = Sm_F ,fill="black",justify="left")
            E6 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E6.focus_set() 
            E6.place(x=640, y=490)

           

           

            but1=tk.Button(self,text="Submit",width=12,height=1,font=Sm_F,fg="black",bg="gray72",relief="raised",command=lambda:Register(E1,E2,E3,E4,E5,E6))
            but1.place(x=640,y=630)
            

            def Register(E1,E2,E3,E4,E5,E6):
                p1=E1.get()
                p2=E2.get()
                p3=E3.get()
                p4=E4.get()
                p5=E5.get()
                p6=E6.get()
                
                
                conn = sqlite3.connect('face.db')
                c = conn.cursor()
                c.execute("INSERT INTO Student(sf_name,sl_name,mob_no,email,course,year) values(?,?,?,?,?,?)",(p1,p2,p3,p4,p5,p6))
                find=("select s_id from Student where sf_name=?")
                c.execute(find,[(p1),])
                res=c.fetchone()
                v8 = tk.StringVar()
                v8.set(res)
                l5=tk.Label(c1, text="Yourstudent id is:",font = Sm_F,bg="white")
                l6=tk.Label(c1, textvariable=v8,font = Sm_F,bg="white")
                l5.place(x=650,y=680)
                l6.place(x=780,y=680)
                conn.commit()
                c.close()
                conn.close()

class SendEmailPage(tk.Frame):
    def __init__(self,parent,controller):
            self.controller=controller
            tk.Frame.__init__(self,parent)
        
            c1 = tk.Canvas(self)       
            c1.pack(fill="both", expand=True)
            c1.create_text(560,200, text="Email Sending Site",font = Large_F ,fill="black")
            c1.create_text(520,250, text="Enter Student id",font = Sm_F ,fill="black",justify="left")
            E1 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E1.focus_set() 
            E1.place(x=640, y=240)
            c1.create_text(520,300, text="Enter email subject",font = Sm_F ,fill="black",justify="left")
            E2 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E2.focus_set() 
            E2.place(x=640, y=290)
            c1.create_text(520,350, text="Enter email content",font = Sm_F ,fill="black",justify="left")
            E3 = tk.Entry(self, state="normal", font=Sm_F,width=20, bd=3)
            E3.focus_set() 
            E3.place(x=640, y=340)
            but1=tk.Button(self,text="Submit",width=12,height=1,font=Sm_F,fg="black",bg="gray72",relief="raised",command=lambda:email(E1,E2,E3))
            but1.place(x=640,y=400)

            def email(E1,E2,E3):
                p=E1.get()
                q=E2.get()
                r=E3.get()
                conn=sqlite3.connect('face.db')
                c1=conn.cursor()
                find=("select email from Student where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                print(result1)
                gmail_user = "prakshitha248@gmail.com"
                gmail_pwd = "iminhome"
                TO = result1[0]
                SUBJECT = q
                TEXT=r
                                    
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                BODY = '\r\n'.join(['To: %s' % TO,
                                        'From: %s' % gmail_user,
                                            'Subject: %s' % SUBJECT,'',TEXT])

                server.sendmail(gmail_user, TO, BODY)
                tm.showinfo('Email','Email sent successfully!!',parent=self)
                                
                conn.commit()
                c1.close()
                conn.close()


            
            
            
            

                


class FacultyPage(tk.Frame):
    def __init__(self,parent,controller):
        self.controller=controller
        tk.Frame.__init__(self,parent)
        
        c1 = tk.Canvas(self)       
        c1.pack(fill="both", expand=True)

        '''load = Image.open("Attendance.jpg")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(0,0,image = img.image,anchor = "nw")  
        load = Image.open("UI__26-512.png")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(160,380,image = img.image,anchor = "nw")'''
        
        s1=tk.Button(self, text="Take attendence",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25,command=lambda:controller.show_frame(TakeAttendencePage))
        s2=tk.Button(self, text="view attendence status",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25,command=lambda:controller.show_frame(ViewStatusPage))
        s3=tk.Button(self, text="view student profile",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25)
        s1.place(x=200,y=150)
        s2.place(x=200,y=200)
        s3.place(x=200,y=250)
        b1=tk.Button(self,text="Back",fg="black",bg="orange",relief="raised",width=5,font=Sm_F,command=lambda:controller.show_frame(LoginPage))
        b1.place(x=20,y=10)
        
        

class ViewStatusPage(tk.Frame):
    def __init__(self,parent,controller):
        self.controller=controller
        tk.Frame.__init__(self,parent)
        
        c1 = tk.Canvas(self)       
        c1.pack(fill="both", expand=True)

        '''load = Image.open("Attendance.jpg")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(0,0,image = img.image,anchor = "nw")  
        load = Image.open("UI__26-512.png")
        render = ImageTk.PhotoImage(load)   
        img = tk.Label(image=render)        
        img.image = render
        c1.create_image(160,380,image = img.image,anchor = "nw")'''
        
        b1=tk.Button(self,text="Back",fg="black",bg="orange",relief="raised",width=5,font=Sm_F,command=lambda:controller.show_frame(FacultyPage))
        b1.place(x=20,y=10)
        
        c1.create_text(550,360, text="Enter student id",font = Sm_F)
        E1 = tk.Entry(self, state="normal",font=Sm_F, width=20, bd=3) 
        E1.place(x=650, y=350)
        
        c1.create_text(550,400, text="Enter subject name",font = Sm_F)
        E2 = tk.Entry(self, state="normal",font=Sm_F, width=20, bd=3) 
        E2.place(x=650, y=400)
        s1=tk.Button(self, text="check status",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25,command=lambda:view(E1,E2))
        s1.place(x=650,y=500)
        def view(E1,E2):
            conn=sqlite3.connect('face.db')
            c1=conn.cursor()
            p=E1.get()
            q=E2.get()
            if(q =='s1'):
                
                find=("select classes from s1Attendence where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
               
                
                per= ((result1[0])/60)*100
                v1=tk.StringVar()
                v1.set(per)
                L1=tk.Label(self, textvariable=v1,font = Sm_F,bg="white")
                L1.place(x=650,y=550)
            if(q=='s2'):
                
                find=("select classes from s2Attendence where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                per= ((result1[0])/60)*100
                v1=tk.StringVar()
                v1.set(per)
                L1=tk.Label(self, textvariable=v1,font = Sm_F,bg="white")
                L1.place(x=650,y=550)
                
            
               
            if(q=='s3'):
                
                find=("select classes from s3Attendence where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                per= ((result1[0])/60)*100
                v1=tk.StringVar()
                v1.set(per)
                L1=tk.Label(self, textvariable=v1,font = Sm_F,bg="white")
                L1.place(x=650,y=550)
            
            if(q=='s4'):
                
                find=("select classes from s4Attendence where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                per= ((result1[0])/60)*100
                v1=tk.StringVar()
                v1.set(per)
                L1=tk.Label(self, textvariable=v1,font = Sm_F,bg="white")
                L1.place(x=650,y=550)
            
            if(q=='s5'):
                
                find=("select classes from s5Attendence where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                per= ((result1[0])/60)*100
                v1=tk.StringVar()
                v1.set(per)
                L1=tk.Label(self, textvariable=v1,font = Sm_F,bg="white")
                L1.place(x=650,y=550)
            
            if(q=='s6'):
                
                find=("select classes from s6Attendence where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                per= ((result1[0])/60)*100
                v1=tk.StringVar()
                v1.set(per)
                L1=tk.Label(self, textvariable=v1,font = Sm_F,bg="white")
                L1.place(x=650,y=550)
            if per<75.0 :
                s1=tk.Button(self, text="send alert mail",font=Sm_F,fg="black",bg="gray78",relief="raised",width=25,command=lambda:email(p))
                s1.place(x=650,y=500)
                
            def email(p):
                conn=sqlite3.connect('face.db')
                c1=conn.cursor()
                find=("select email from Student where s_id=?")
                c1.execute(find,[p,])
                result1=c1.fetchone()
                print(type(result1[0]))
                gmail_user = "prakshitha248@gmail.com"
                gmail_pwd = "iminhome"
                TO = result1[0]
                SUBJECT = "Student Attendence shortage notification"
                TEXT="Dear parent,\n    With reference to above subject we write to state that your child is having shortage in attendence please make sure he attends classes properlu.\n .\n\nTHANK YOU\n"
                                    
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                BODY = '\r\n'.join(['To: %s' % TO,
                                        'From: %s' % gmail_user,
                                            'Subject: %s' % SUBJECT,'',TEXT])

                server.sendmail(gmail_user, TO, BODY)
                tm.showinfo('Email','Email sent successfully!!',parent=self)
                                
                conn.commit()
                c.close()
                conn.close()


                
                
                
                

        
class TakeAttendencePage(tk.Frame):
       def __init__(self,parent,controller):       
            self.controller=controller
            tk.Frame.__init__(self,parent)
            b1=tk.Button(self,text="Back",fg="black",bg="orange",relief="raised",width=5,font=Sm_F,command=lambda:controller.show_frame(FacultyPage))
            b1.place(x=20,y=10)
            c1 = tk.Canvas(self)       
            c1.pack(fill="both", expand=True)
            '''load = Image.open("Attendance.jpg")
            render = ImageTk.PhotoImage(load)   
            img = tk.Label(image=render)        
            img.image = render
            c1.create_image(0,0,image = img.image,anchor = "nw")  
            load = Image.open("UI__26-512.png")
            render = ImageTk.PhotoImage(load)   
            img = tk.Label(image=render)        
            img.image = render
            c1.create_image(160,380,image = img.image,anchor = "nw")'''

            c1.create_text(550,360, text="Enter subject name",font = Sm_F)
            E2 = tk.Entry(self, state="normal",font=Sm_F, width=20, bd=3) 
            E2.place(x=650, y=350)

            B1=tk.Button(self, text="Submit",font=Sm_F,fg="black",bg="lightblue",relief="raised",width=10,command=lambda:TakeAttendence(E2))
            B1.place(x=650, y=450)
            
            def TakeAttendence(E2):  
                conn=sqlite3.connect('face.db')
                c=conn.cursor()
                p=E2.get()


                face_cascade = cv2.CascadeClassifier('cascade/data/haarcascade_frontalface_alt2.xml')
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read("trainer.yml")
                labels={"person name":1}
                with open("labels.pickle" , "rb") as f:
                        labels=pickle.load(f)
                        labels={v:k for k,v in labels.items()}
                        cap=cv2.VideoCapture(0)
                keyboard = Controller()
                while(True):
                    keyboard = Controller()
                    ret,frame = cap.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5 ,minNeighbors=5)
                    for(x,y,w,h) in faces:
                            
                            #print(x,y,w,h)
                            roi_gray = gray[y:y+h , x:x+w]

                            id_,conf = recognizer.predict(roi_gray)
                            
                            if conf>=45 : #and conf<=85:
                                 
                                 print(id_)
                                 id_=id_+1
                                 if(p=='s1'):
                                     print('update')
                                     c.execute("UPDATE s1Attendence set classes=classes+1 where s_id=? ",(id_ ,))
                                     conn.commit()
                                     img_item = "my-img.png"
                                     cv2.imwrite(img_item , roi_gray)

                                     color = (255,0,0)
                                     stroke=2
                                     end_cord_x=x+w
                                     end_cord_y=y+h
                                     cv2.rectangle(frame, (x,y) , (end_cord_x , end_cord_y),color , 2)
                                     break
                                     

                                 if(p=='s2'):
                                     
                                     c.execute("UPDATE s2Attendence set classes=classes+1 where s_id=? ",(id_ ,))
                                     conn.commit()
                                     break

                                 if(p=='s3'):
                                     
                                     c.execute("UPDATE s3Attendence set classes=classes+1 where s_id=? ",(id_ ,))
                                     conn.commit()
                                     break

                                 if(p=='s4'):
                                     
                                     c.execute("UPDATE s4Attendence set classes=classes+1 where s_id=? ",(id_ ,))
                                     conn.commit()
                                     break

                                 if(p=='s5'):
                                     
                                     c.execute("UPDATE s5Attendence set classes=classes+1 where s_id=? ",(id_ ,))
                                     conn.commit()
                                     break

                                 if(p=='s6'):
                                     
                                     c.execute("UPDATE s6Attendence set classes=classes+1 where s_id=? ",(id_ ,))
                                     conn.commit()
                                     break


                            
            

                                    
                    cv2.imshow('frame',frame)
                    
                    if cv2.waitKey(20)& 0xFF == ord('q'):
                           break
                    
                    keyboard.press('q')
                    keyboard.release('q')                

                cap.release()
                cv2.destroyAllWindows()

                





           





pp = collegeapp()   
pp.geometry("1920x1080")
pp.mainloop()

    
