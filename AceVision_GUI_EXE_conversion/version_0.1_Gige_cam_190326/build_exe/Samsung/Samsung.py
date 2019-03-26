# -*- coding: utf-8 -*-

from tkinter import *



def nothing():
    pass

def test():
    global root

    root.destroy()


antenna_list = ["reserved", "reserved", "reserved", "reserved"]
antenna_cmd = [test, nothing, nothing, nothing]
filter_list =["reserved", "reserved", "reserved", "reserved"]
filter_cmd = [test, nothing, nothing, nothing]

def select_antenna():
    global antenna_B, filter_B

    antenna_B.destroy()
    filter_B.destroy()

    antenna_B = Button(root, text="ANTENNA", font="Helvetica 10", relief="raised", overrelief="solid", bg="#dfffbf", \
                       width=12, height=2, bd=3, padx=2, pady=2, command=select_antenna)
    antenna_B.place(x=10, y=250)

    filter_B = Button(root, text="FILTER", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                      width=12, height=2, bd=3, padx=2, pady=2, command=select_filter)
    filter_B.place(x=10, y=300)

    for i in range(4):
        Button(root, text=antenna_list[i], font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", highlightcolor="yellow", \
               width=10, height=5, bd=3, padx=2, pady=2, command=antenna_cmd[i]).place(relx=0.21 + (i * 0.2), rely=0.625)

def select_filter():
    global antenna_B, filter_B

    antenna_B.destroy()
    filter_B.destroy()

    antenna_B = Button(root, text="ANTENNA", font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", \
                       width=12, height=2, bd=3, padx=2, pady=2, command=select_antenna)
    antenna_B.place(x=10, y=250)

    filter_B = Button(root, text="FILTER", font="Helvetica 10", relief="raised", overrelief="solid", bg="#dfffbf", \
                      width=12, height=2, bd=3, padx=2, pady=2, command=select_filter)
    filter_B.place(x=10, y=300)

    for i in range(4):
        Button(root, text=filter_list[i], font="Helvetica 10", relief="raised", overrelief="solid", bg="#ebebeb", highlightcolor="yellow", \
               width=10, height=5, bd=3, padx=2, pady=2, command=filter_cmd[i]).place(relx=0.21 + (i * 0.2), rely=0.625)



def main():
    global root, antenna_B, filter_B

    root = Tk()
    root.iconbitmap(default = "aceantenna.ico")
    main_width, main_height = 600, 400

    root.title("ace antennaA")
    root.geometry("{}x{}".format(main_width, main_height))

    # 메인 화면 창
    imageData = PhotoImage(file="C:/AceVision/attached file/image/samsung.png")
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
