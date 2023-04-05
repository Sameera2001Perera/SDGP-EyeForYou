#importing packages
import tkinter
import customtkinter
import cv2
from PIL import Image, ImageTk

from camara import Camara
from multiprocessing import Process

import mongodb as db
import customtkinter as ctk
import tkinter as tk
import distanceAndBlinkDetectionModel
import os
from winotify import Notification, audio
import json




class SetRefImageFrame(ctk.CTkFrame):
    def __init__(self, master, userName, **kwargs):
        self.userName = userName
        self.master = master
        super().__init__(master, **kwargs)
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
        ref_faceWidth,_ = distanceAndBlinkDetectionModel.face_data(frame)
        if check and ref_faceWidth != 0:
            image = self.userName + ".png"

            cv2.imwrite("imageRes/" + image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            self.canvas.create_image(0, 0, image=ImageTk.PhotoImage(image=Image.fromarray(frame)))

            mainFrame = MainApplicationFrame(master=self.master, userName=self.userName, width=720, height=550,
                                         corner_radius=15)
            self.master.placeFrame(mainFrame)
            self.camara.release()
            db.postRefImage(self.userName)
            self.destroy()
        else:
            toast = Notification(app_id="EyeForYou", title="face not recognized", msg="the system failed to recognize your face",
                                 duration="short")
            toast.set_audio(audio.SMS, loop=False)
            print("face not recognized")
            toast.show()


    def update(self):
        isTrue, frame = self.camara.getFrame()

        if isTrue:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=ctk.NW)

        self.master.after(6, self.update)
class MainApplicationFrame(ctk.CTkFrame):
    def __init__(self, master, userName, **kwargs):
        super().__init__(master, **kwargs)
        self.userName = userName

        self.master = master

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        #hell user label
        self.label = ctk.CTkLabel(master=self, text="Hello "+self.userName+" ...", font=('Century Gothic', 30), height=50)
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="nsew")

        self.distaceDetectionProcesses = []
        self.distaceDetectionProcesses.append(Process(target=distanceAndBlinkDetectionModel.measureDistance, args=(self.userName,)))

        # align buttons to the left
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, padx=20, pady=(20, 20), sticky="nsew")

        self.logout_btn = ctk.CTkButton(button_frame, text="log out", fg_color='red',hover_color='#9F3630',width=100, command=self.logOut)
        self.logout_btn.pack(anchor=tk.CENTER, expand=True)

        self.camara = ctk.CTkButton(button_frame, text="Camara View", width=100, command=self.showCam)
        self.camara.pack(anchor=tk.CENTER, expand=True)

        self.start_btn=ctk.CTkButton(button_frame, text = "Start",fg_color='#4F8422',hover_color='#276422',width = 100, command = self.start)
        self.start_btn.pack(anchor=tk.CENTER, expand=True)

        self.stop_button=ctk.CTkButton(button_frame, text = "Stop", fg_color='#6D544D',hover_color='#9E544D', width = 100, command = self.stop)
        self.stop_button.pack(anchor=tk.CENTER, expand=True)

        # Usage History label
        self.label = ctk.CTkLabel(master=self, text="History", font=('Century Gothic', 20))
        self.label.grid(row=2, column=1, padx=20, pady=(10, 5), sticky="nsew")

        #frame for the table
        self.hFrame = customtkinter.CTkFrame(master=self, width=200, height=150)
        self.hFrame.grid(row=3, column=1, sticky="nswe", padx=15, pady=15)


        sessions = db.getSessions(username=userName)

        #tabel
        columns = ("date and time", "eye blink warnings", "distance warnings")
        self.table = tk.ttk.Treeview(master=self.hFrame,
                                  columns=columns,
                                  height=10,
                                  selectmode='browse',
                                  show='headings')

        self.table["columns"] = columns

        self.table.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)


        # self.sessionsBox = tk.Listbox(master=self, width=67, font=("Helvetica", 15))
        # self.sessionsBox.grid(row=2, column=1, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        self.table.column("date and time", width=150)
        self.table.column("eye blink warnings", width=100, anchor=tk.CENTER)
        self.table.column("distance warnings", width=100, anchor=tk.CENTER)

        self.table.heading('date and time', text='Date\Time')
        self.table.heading('eye blink warnings', text='Eye Blink Warnings')
        self.table.heading('distance warnings', text='Distance Warnings')



        rc = 0
        for item in sessions:
            dictionary = json.loads(json.dumps(item))
            time = dictionary["start_time"]
            blinkWarnings = dictionary["blinkWarnings"]
            distanceWarnings = dictionary["distanceWarnings"]

            self.table.insert("", index=0, iid=rc, values=(time,blinkWarnings,distanceWarnings))


            # self.sessionsBox.insert(rc, "   start time : "+str(time)+"  ,  blink warnings : "+str(blinkWarnings)+"  ,  distance warnings : "+str(distanceWarnings))

            rc+=1

        self.table.bind('<Motion>', 'break')


        # resize the canvas when the frame size changes
    def showCam(self):
        if(os.path.exists("camaraFlag.flag")):
            os.remove("camaraFlag.flag")
        else:
            with open('camaraFlag.flag', 'w') as fp:
                pass
            fp.close()


    def start(self):
        self.distaceDetectionProcesses[-1].start()
        self.start_btn.configure(state="disabled")
        self.stop_button.configure(state="enable")
        self.logout_btn.configure(state="disabled")


    def stop(self):
        self.distaceDetectionProcesses[-1].terminate()
        self.distaceDetectionProcesses.append(Process(target=distanceAndBlinkDetectionModel.measureDistance, args=(self.userName,)))
        self.start_btn.configure(state="enable")
        self.stop_button.configure(state="disabled")
        self.logout_btn.configure(state="enable")
        #creating new process since the previous process cannot be started again
        # self.distaceDetectionProcess = Process(distanceDetectionModel.measureDistance, args=(self.userName,))


    def logOut(self):
        os.remove("imageRes/"+self.userName+".png")
        for widgets in self.winfo_children():
            widgets.destroy()
        self.master.placeFrame(AccountFrame(master=self.master, width=320, height=350, corner_radius=25))
    def setDis(self, distance):
        self.distanceLabel.configure(text=distance)


class AccountFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
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
        elif (db.isAvailable(self.usernameEntry.get()) and db.getPassword(self.usernameEntry.get()) == self.passwordEntry.get()):
            if (db.hasRefImage(self.usernameEntry.get())):
                db.getImage(self.usernameEntry.get())
                self.master.placeFrame(MainApplicationFrame(master=self.master, userName=self.usernameEntry.get(), width=620, height=450, corner_radius=15))
            else:
                self.master.placeFrame(SetRefImageFrame(master=self.master, userName=self.usernameEntry.get(),  width=620, height=550, corner_radius=15))
            self.destroy()


        else:
            self.errorLog.configure(text="Username or password incorrect")



    def createAccount_function(self):
        if (self.usernameEntry.get()=="" or self.passwordEntry.get()==""):
            self.errorLog.configure(text="Username or Password is empty")
        elif (db.isAvailable(self.usernameEntry.get())):
            self.errorLog.configure(text="This username already exist")
        elif (str(self.passwordEntry.get()) != (str(self.confirmPasswordEntry.get()))):
            self.errorLog.configure(text="Password mismatch")
        else:
            self.errorLog.configure(text="Creating Account...")
            db.postAccount(self.usernameEntry.get(), self.passwordEntry.get())
            self.setLoginView()

class LoginApp(customtkinter.CTk):
    def __init__(self):
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

        self.accountFrame = AccountFrame(master=self, width=320, height=350, corner_radius=25)
        self.placeFrame(self.accountFrame)

    def placeFrame(self, frame):
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)



