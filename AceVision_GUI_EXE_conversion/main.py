# -*- coding: utf-8 -*-

from tkinter import *
import QR_SS_Detect   		# **중요, exe파일을 만들면 디렉터리가 같은곳에 위치하므로 from ~ import가 아니고, 그냥 import 모듈이름.  즉, main과 같은 자리에 있으므로 이렇게 해야한다!!!
import RivetDetect

def nothing():
    pass

def rivet():
    root.destroy()
    RivetDetect.execute()

def qr_ss():
    root.destroy()
    QR_SS_Detect.execute()

root = Tk()
main_width, main_height = 800, 600

root.title("ace antennaA")
root.geometry("{}x{}".format(main_width, main_height))

# 메인 화면 창
imageData = PhotoImage(file="C:\Data_Record_QR/aceantenna.jpg")
label_main = Label(root, image = imageData)
label_main.place(relx=0.5, rely=0.3, anchor=CENTER)

menu_list = ["Check\n\nRivet", "Check\n\nQR && SS", "reserved", "reserved", "reserved"]
command_list = [rivet, qr_ss, nothing, nothing, nothing]
for i in range(5):
    Button(root, text=menu_list[i], font="돋움체", relief="raised", overrelief="solid", bg="#ebebeb", \
           width=10, height=5, bd=3, padx=2, pady=2, command=command_list[i]).place(relx=0.025 + (i * 0.2), rely=0.625)

bottom = Label(root, text="ace antennaA ver1.0.0", font="돋움체", bg="#ebebeb", bd=2, height=2, relief="raised", anchor=CENTER)
bottom.pack(side=BOTTOM, fill=X)

root.mainloop()


