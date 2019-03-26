# -*- coding: utf-8 -*-

from tkinter import *

'''
# Build 가 없을 때
from Samsung import *
from Ericsson import *
'''

# Build 를 할 때
import Samsung
import Ericsson

def nothing():
    pass

def samsung():
    root.destroy()
    Samsung.main()

def ericsson():
    root.destroy()
    Ericsson.main()


root = Tk()
root.iconbitmap(default = "aceantenna.ico")
main_width, main_height = 600, 400

root.title("ace antennaA")
root.geometry("{}x{}".format(main_width, main_height))

# 메인 화면 창
imageData = PhotoImage(file="C:/AceVision/attached file/image/aceantenna.png")
label_main = Label(root, image = imageData)
label_main.place(relx=0.5, rely=0.3, anchor=CENTER)

customer_list = ['SAMSUNG','Ericsson','reserved','reserved','reserved']
command_list = [samsung, ericsson, nothing, nothing, nothing]

for i in range(5):
    Button(root, text=customer_list[i], font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb",highlightcolor="yellow", \
           width=10, height=5, bd=3, padx=2, pady=2, command=command_list[i]).place(relx=0.025 + (i * 0.2),rely=0.625)

bottom = Label(root, text="ace antennaA ver1.0.0", font="Helvetica 10 bold", bg="#ebebeb", bd=2, height=2, relief="raised", anchor=CENTER)
bottom.pack(side=BOTTOM, fill=X)

root.mainloop()

