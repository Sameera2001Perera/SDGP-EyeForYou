#importing packages
import tkinter
import customtkinter
import cv2
from PIL import Image, ImageTk
from SDGP.camara import Camara
import time
from multiprocessing import Process


import customtkinter as ctk
import tkinter as tk
from SDGP import distanceDetectionModel
import os


class SetRefImageFrame(ctk.CTkFrame):
    def __init__(self, master, userName, db, **kwargs):
        self.userName = userName
        self.master = master
        super().__init__(master, **kwargs)
        self.db = db
        self.master = master
        self.label = ctk.CTkLabel(master=self, text="Set ref image", font=('Century Gothic', 30))
        self.label.place(relx=0.5, y=30, anchor=tk.CENTER)

        self.camara = Camara()

        self.label = ctk.CTkLabel(master=master, text="", text_color="#fff", bg_color="green", width=250, anchor="w")
        self.canvas = tk.Canvas(self, width=self.camara.width, height=self.camara.height, bg='black')
        self.canvas.pack()

        self.snapshot_btn = ctk.CTkButton(self, text="Capture", width=30, command=self.snapshot)
        self.snapshot_btn.pack(anchor=ctk.CENTER, expand=True)
        self.update()

    def snapshot(self):
        check, frame = self.camara.getFrame()
        if check:
            image = self.userName + ".png"
            cv2.imwrite("imageRes/" + image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.canvas.create_image(0, 0, image=ImageTk.PhotoImage(image=Image.fromarray(frame)))
        self.label.configure(text="Username or password incorrect")
        mainFrame = MainApplicationFrame(master=self.master, userName=self.userName, db=self.db, width=720, height=550,
                                         corner_radius=15)
        self.master.placeFrame(mainFrame)
        self.camara.release()
        self.db.postRefImage(self.userName)
        self.destroy()

    def update(self):
        isTrue, frame = self.camara.getFrame()

        if isTrue:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=ctk.NW)

        self.master.after(6, self.update)
class MainApplicationFrame(ctk.CTkFrame):
    def __init__(self, master, userName, db, **kwargs):
        super().__init__(master, **kwargs)
        self.userName = userName

        self.db = db
        self.master = master

        self.label = ctk.CTkLabel(master=self, text=self.userName, font=('Century Gothic', 30))
        self.label.place(relx=5, y=80, anchor=tk.CENTER)

        self.distanceLabel = ctk.CTkLabel(master=self, text="",font=('Century Gothic', 30))
        self.distanceLabel.place(relx=5, y=10, anchor=tk.CENTER)

        self.distaceDetectionProcess = Process(target=distanceDetectionModel.measureDistance)

        self.snapshot_btn = ctk.CTkButton(self, text="log out", width=40, command=self.logOut)
        self.snapshot_btn.pack(anchor=tk.CENTER, expand=True)

        self.snapshot_btn=ctk.CTkButton(self, text = "Start", width = 30, command = self.start)
        self.snapshot_btn.pack(anchor=tk.CENTER, expand=True)

        self.snapshot_btn=ctk.CTkButton(self, text = "Stop", width = 30, command = self.stop)
        self.snapshot_btn.pack(anchor=tk.CENTER, expand=True)
    def start(self):
        self.distaceDetectionProcess.start()
        time.sleep(3)

    def stop(self):
        self.distaceDetectionProcess.terminate()
        self.distaceDetectionProcess = Process(target=distanceDetectionModel.measureDistance)


    def logOut(self):
        os.remove("imageRes/"+self.userName+".png")
        self.master.placeFrame(AccountFrame(master=self.master, db=self.db, width=320, height=350, corner_radius=25))
        self.destroy()
    def setDis(self, distance):
        self.distanceLabel.configure(text=distance)


class AccountFrame(customtkinter.CTkFrame):
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        self.master = master
        self.setLoginView()

    def setLoginView(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.label = customtkinter.CTkLabel(master=self, text="Login to your account", font=('Century Gothic', 20))
        self.label.place(relx=0.5, y=30, anchor=tkinter.CENTER)

        self.errorLog = customtkinter.CTkLabel(master=self, text="", font=('Century Gothic', 15))
        self.errorLog.place(x=45, y=50)

        self.usernameEntry = customtkinter.CTkEntry(master=self, width=220, placeholder_text="Username")
        self.usernameEntry.place(x=50, y=80)

        self.passwordEntry = customtkinter.CTkEntry(master=self, width=220, placeholder_text="Password")
        self.passwordEntry.place(x=50, y=130)

        self.login = customtkinter.CTkButton(master=self, width=220, text="Login", corner_radius=6,
                                             command=self.login_function)
        self.login.place(x=50, y=210)

        self.caButton = customtkinter.CTkButton(master=self, width=220, text="create account", corner_radius=6,
                                                command=self.setCreateAccountView)

        self.caButton.configure(fg_color='green', hover_color='dark green')
        self.caButton.place(x=50, y=260)

    def setCreateAccountView(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.label = customtkinter.CTkLabel(master=self, text="Create you account", font=('Century Gothic', 20))
        self.label.place(relx=0.5, y=30, anchor=tkinter.CENTER)

        self.errorLog = customtkinter.CTkLabel(master=self, text="", font=('Century Gothic', 15))
        self.errorLog.place(x=45, y=50)

        self.usernameEntry = customtkinter.CTkEntry(master=self, width=220, placeholder_text="Username")
        self.usernameEntry.place(x=50, y=80)

        self.passwordEntry = customtkinter.CTkEntry(master=self, width=220, placeholder_text="New Password")
        self.passwordEntry.place(x=50, y=130)

        self.confirmPasswordEntry = customtkinter.CTkEntry(master=self, width=220, placeholder_text="Confirm Password")
        self.confirmPasswordEntry.place(x=50, y=180)

        self.caButton = customtkinter.CTkButton(master=self, width=220, text="create account", corner_radius=6,
                                                command=self.createAccount_function)
        self.caButton.configure(fg_color='green', hover_color='dark green')
        self.caButton.place(x=50, y=260)

    def login_function(self):
        self.errorLog.configure(text="Checking your account...")
        if(self.usernameEntry.get()=="" or self.usernameEntry.get()==""):
            self.errorLog.configure(text="Username or password is empty")
        elif (self.db.isAvailable(self.usernameEntry.get()) and self.db.getPassword(self.usernameEntry.get()) == self.passwordEntry.get()):
            if (self.db.hasRefImage(self.usernameEntry.get())):
                self.db.getImage(self.usernameEntry.get())
                self.master.placeFrame(MainApplicationFrame(master=self.master, userName=self.usernameEntry.get(), db=self.db, width=620, height=450, corner_radius=15))
            else:
                self.master.placeFrame(SetRefImageFrame(master=self.master, db=self.db, userName=self.usernameEntry.get(),  width=620, height=550, corner_radius=15))
            self.destroy()


        else:
            self.errorLog.configure(text="Username or password incorrect")



    def createAccount_function(self):
        if (self.usernameEntry.get()=="" or self.passwordEntry.get()==""):
            self.errorLog.configure(text="Username or Password is empty")
        elif self.db.isAvailable(self.usernameEntry.get()):
            self.errorLog.configure(text="This username already exist")
        elif (str(self.passwordEntry.get()) != (str(self.confirmPasswordEntry.get()))):
            self.errorLog.configure(text="Password mismatch")
        else:
            self.errorLog.configure(text="Creating Account...")
            self.db.postAccount(self.usernameEntry.get(), self.passwordEntry.get())
            self.setLoginView()

class LoginApp(customtkinter.CTk):
    def __init__(self, database):
        super().__init__()

        self.geometry("780x550")
        self.title("EyeForYou")
        self.resizable(width=False, height=False)
        backgroundImage = customtkinter.CTkImage(light_image=Image.open(
            "backgroundImages/light_mode_background.png"), dark_image=Image.open(
            "backgroundImages/dark_mode_background.png"), size=(800, 500))

        imlabel = customtkinter.CTkLabel(master=self, image=backgroundImage)
        imlabel.pack()

        self.label = customtkinter.CTkLabel(master=self, text="EyeForYou", font=('Century Gothic italic', 30), corner_radius=30)
        self.label.place(relx=0.5, y=50, anchor=tkinter.CENTER)

        self.database = database

        self.accountFrame = AccountFrame(master=self, db=self.database, width=320, height=350, corner_radius=25)
        self.placeFrame(self.accountFrame)

    def placeFrame(self, frame):
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


