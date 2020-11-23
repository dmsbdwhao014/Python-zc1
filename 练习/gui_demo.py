import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

def checkNameEntry(nameValue, validOption, fieldName):
    return True

def checkNameEntryInvalid():
    print('nameEntry 不合法时执行')


def selFile():
    path_ = filedialog.askopenfilename()
    fileEntryV.set(path_)



############### 页面 ########################
# 实例化窗口
root = tk.Tk()
# 窗口标题
root.title("window test")
# 窗口分辨率
root.geometry("500x300+100+200")
# 设置窗口不可以调整
root.resizable(0, 0)

win = tk.Frame(root)
win.pack(side=tk.TOP, expand = tk.YES, fill=tk.NONE, anchor='nw')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='new',command=None)
filemenu.add_command(label='open')
filemenu.add_command(label='exit')

fileEntryV = tk.StringVar()
banquanV =  tk.StringVar()
#
nameEntryCMD = win.register(checkNameEntry)

# 考试名称
name_label = tk.Label(win, text="本次考试名称 ")
name_label.grid(row=0, column=0, sticky=tk.E)

name_entry = tk.Entry(win, width=50, validate='focusout', validatecommand=(nameEntryCMD,'%P','%v','%W'), invalidcommand=checkNameEntryInvalid)
name_entry.grid(row=0, column=1, sticky=tk.W)
name_entry.focus()


# 每个考场人数
num_label = tk.Label(win, text="每个考场人数 ")
num_label.grid(row=1, column=0, sticky=tk.E)

num_entry = tk.Entry(win, width=50)
num_entry.insert(0, '30')
num_entry.grid(row=1, column=1, sticky=tk.W)

# 文理科是否分考场
wl_label = tk.Label(win, text="文理科是否分考场 ")
wl_label.grid(row=2, column=0, sticky=tk.E)

wl_cmo = ttk.Combobox(win)
wl_cmo['value'] = ('否','是')
wl_cmo.current(0)
wl_cmo.grid(row=2, column=1, sticky=tk.W)

# 成绩单附件
file_label = tk.Label(win, text="成绩单（excel）")
file_label.grid(row=3, column=0, sticky=tk.W)

file_entry = tk.Entry(win, textvariable=fileEntryV, state="disabled", width=50)
file_entry.grid(row=3, column=1, sticky=tk.E)

file_sel_btn = tk.Button(win, text="选择", command=selFile)
file_sel_btn.grid(row=3, column=2)

filler_label = tk.Label(win, text="")
filler_label.grid()
# 执行
btn = tk.Button(win, text="生成考场", command=None)
btn.grid(row=5, column=1)

root.config(menu=menubar)

win.mainloop()