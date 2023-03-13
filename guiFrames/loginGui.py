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
