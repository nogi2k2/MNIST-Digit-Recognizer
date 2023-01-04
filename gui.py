from tensorflow.keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui as wgui
from PIL import ImageGrab, ImageOps, Image
import numpy as np
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
model=load_model('mcp\save_2.h5')
def predict_num(img):
    img=img.resize((28,28))
    img=img.convert('L')
    img=ImageOps.invert(img)
    img=np.array(img)
    img=img.reshape(1,28,28,1)
    img=img.astype('float32')
    img/=255.0
    r=model.predict([img])[0]
    return np.argmax(r),max(r)

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x=self.y=0
        self.canvas=tk.Canvas(self,width=400, height=400,bg='white',cursor='cross')
        self.canvas.grid(row=0,column=0,pady=2,sticky=W)
        self.label=tk.Label(self,text="Draw and click 'Predict' to predict",font=("Times New Roman",14))
        self.label.grid(row=0,column=1,pady=2,padx=2)
        self.predict_btn=tk.Button(self,text="Predict",fg='blue',command=self.pdict)
        self.predict_btn.grid(row=1,column=1,pady=2,padx=2)
        self.clear_btn=tk.Button(self,text="Clear",fg='blue',command=self.clear)
        self.clear_btn.grid(row=1,column=0,pady=2)
        self.canvas.bind("<B1-Motion>",self.draw)

    def clear(self):
        self.canvas.delete("all")
    def pdict(self):
        HWND=self.canvas.winfo_id()
        rect=wgui.GetWindowRect(HWND)
        im=ImageGrab.grab(rect)
        digit,acc=predict_num(im)
        self.label.configure(text=f"{digit} Acc: {acc*100:.2f}%")
    def draw(self,event):
        self.x=event.x
        self.y=event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
gui=GUI()
mainloop()