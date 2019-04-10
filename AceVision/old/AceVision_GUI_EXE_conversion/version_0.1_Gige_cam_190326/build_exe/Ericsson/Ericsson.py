# -*- coding: utf-8 -*-

from tkinter import *
'''
from Air3239 import *
'''

import Air3239

def nothing():
    pass

def Air_3239():
    global root

    root.destroy()
    Air3239.main()

def template():
    global root

    root.destroy()
    pass

antenna_list = ["Air3239", "reserved", "reserved", "reserved"]
antenna_cmd = [Air_3239, nothing, nothing, nothing]
filter_list =["reserved", "reserved", "reserved", "reserved"]
filter_cmd = [nothing, nothing, nothing, nothing]
check_select = 0

def select_antenna():
    global antenna_B, filter_B, check_select
    global antenna_B0, antenna_B1, antenna_B2, antenna_B3
    global filter_B1, filter_B2, filter_B3, filter_B4

    antenna_B.destroy()
    filter_B.destroy()

    if check_select == 2:
        cnt = len(filter_list)
        if cnt == 1:
            filter_B0.destroy()
        elif cnt == 2:
            filter_B0.destroy()
            filter_B1.destroy()
        elif cnt == 3:
            filter_B0.destroy()
            filter_B1.destroy()
            filter_B2.destroy()
        else:
            filter_B0.destroy()
            filter_B1.destroy()
            filter_B2.destroy()
            filter_B3.destroy()

    antenna_B = Button(root, text="ANTENNA", font="Helvetica 10", relief="raised", overrelief="solid", bg="#dfffbf", \
                       width=12, height=2, bd=3, padx=2, pady=2, command=select_antenna)
    antenna_B.place(x=10, y=250)

    filter_B = Button(root, text="FILTER", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                      width=12, height=2, bd=3, padx=2, pady=2, command=select_filter)
    filter_B.place(x=10, y=300)


    for i in range(len(antenna_list)):
        globals()['antenna_B{}'.format(i)] = Button(root, text=antenna_list[i], font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb",\
               width=10, height=5, bd=3, padx=2, pady=2, command=antenna_cmd[i])
        globals()['antenna_B{}'.format(i)].place(relx=0.21 + (i * 0.2), rely=0.625)

    check_select = 1

def select_filter():
    global antenna_B, filter_B, check_select
    global antenna_B0, antenna_B1, antenna_B2, antenna_B3
    global filter_B1, filter_B2, filter_B3, filter_B4

    antenna_B.destroy()
    filter_B.destroy()

    if check_select == 1:
        cnt = len(antenna_list)
        if cnt == 1:
            antenna_B0.destroy()
        elif cnt == 2:
            antenna_B0.destroy()
            antenna_B1.destroy()
        elif cnt == 3:
            antenna_B0.destroy()
            antenna_B1.destroy()
            antenna_B2.destroy()
        else:
            antenna_B0.destroy()
            antenna_B1.destroy()
            antenna_B2.destroy()
            antenna_B3.destroy()

    antenna_B = Button(root, text="ANTENNA", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                       width=12, height=2, bd=3, padx=2, pady=2, command=select_antenna)
    antenna_B.place(x=10, y=250)

    filter_B = Button(root, text="FILTER", font="Helvetica 10", relief="raised", overrelief="solid", bg="#dfffbf", \
                      width=12, height=2, bd=3, padx=2, pady=2, command=select_filter)
    filter_B.place(x=10, y=300)


    for i in range(len(filter_list)):
        globals()['filter_B{}'.format(i)] = Button(root, text=filter_list[i], font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb",\
               width=10, height=5, bd=3, padx=2, pady=2, command=filter_cmd[i])
        globals()['filter_B{}'.format(i)].place(relx=0.21 + (i * 0.2), rely=0.625)

    check_select = 2

def main():
    global root, antenna_B, filter_B

    root = Tk()
    root.iconbitmap(default = "aceantenna.ico")
    main_width, main_height = 600, 400

    root.title("ace antennaA")
    root.geometry("{}x{}".format(main_width, main_height))

    # 메인 화면 창
    imageData = PhotoImage(file="./ericsson.png")
    label_main = Label(root, image = imageData)
    label_main.place(relx=0.5, rely=0.3, anchor=CENTER)


    antenna_B = Button(root, text="ANTENNA", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                       width=12, height=2, bd=3, padx=2, pady=2, command=select_antenna)
    antenna_B.place(x=10, y=250)

    filter_B = Button(root, text="FILTER", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                      width=12, height=2, bd=3, padx=2, pady=2, command=select_filter)
    filter_B.place(x=10, y=300)

    bottom = Label(root, text="ace antennaA ver1.0.0", font="Helvetica 10 bold", bg="#ebebeb", bd=2, height=2, relief="raised", anchor=CENTER)
    bottom.pack(side=BOTTOM, fill=X)

    root.mainloop()


if __name__=="__main__":
    main()
