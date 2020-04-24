from tkinter import *
from keras.models import load_model
import win32gui
from PIL import ImageGrab, Image
import numpy as np
from math import trunc
import pickle
import cv2
canvas_width =300
canvas_height = 300

pickle_in=open("gui_digits.p","rb")
model=pickle.load(pickle_in)


def invimg(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j]=abs(img[i,j]-255)
    return img

def predict(img):

    img=np.array(img)
    print(img.shape)
    cv2.imshow("orig frame",img)

    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=invimg(img)

    cv2.imshow("inverted and gray",img)

    img = cv2.resize(img, (28, 28))
    #cv2.imshow("resize",img)

    img=img.reshape(1,28,28,1)


    num=model.predict(img).argmax()
    prob = np.max(model.predict(img))

    return int(num),prob




def clr():
    w.delete('all')
    cav2.delete('all')
def paint(event):
    my = "#FFFFFF"
    x1, y1 = (event.x - 8), (event.y - 8)
    x2, y2 = (event.x + 8), (event.y + 8)
    w.create_oval(x1, y1, x2, y2, fill=my)
def classify_handwriting():
    HWND = Canvas.winfo_id(master)  # get the handle of the canvas
    rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
    a, b, c, d = rect
    #print(rect)
    rect = (a + 18, b + 3, c - 310, d - 53)
    im = ImageGrab.grab(rect)
    res,prob=predict(im)

    cav2.delete('all')
    cav2.create_text(canvas_width * 0.5, canvas_height * 0.5,
                     text=str(res),
                     font=('Arial', 20, 'bold italic'))

    cav2.create_text(canvas_width*0.5,canvas_height*0.6,text=" probability:-",font=('Arial',20,'bold italic'))
    cav2.create_text(canvas_width*0.6,canvas_height*0.8,text=str(trunc(float(prob*100)))+'%',font=('Arial',20,'bold italic'))

master = Tk()
master.title("Painting using Ovals")
w = Canvas(master,
           width=canvas_width,
           height=canvas_height,bg='black')
w.grid(row=0,column=0)
w.bind("<B1-Motion>", paint)
buttid=Button(master,text='Identify',command=classify_handwriting,bg='pink',fg='green')
buttclr=Button(master,text='Clear',command=clr,bg='pink',fg='green')
buttclr.grid(row=1,column=0)


buttid.grid(row=1,column=1)
cav2=Canvas(master,width=canvas_width,height=canvas_height)
mess2=Label(cav2,text='Draw')
cav2.grid(row=0,column=1)
mess = Label(master,text="Press and Drag the mouse to draw")
mess.grid(row=2,column=0)




mainloop()