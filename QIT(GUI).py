"""
第一个基础的完全由自己编写的项目(带GUI)
一个非常简单的某个大学的宿舍电费获取文件
基于Python 3 编写
使用了request,tkinter等库
本人也是Python的小白,自学了一段时间的Python,
总觉得写CMD界面不太合适,因此也是自学爬虫和GUI制作
作为我的第一个简单项目,写完那刻也是颇有感触
不断的构思结构,布局,以及不断的debug.
Created By Apkdio
"""
import ctypes
import os
import tkinter as tk
from datetime import *
from tkinter import ttk, messagebox

import requests

# 检查所选校区并调用对应方法
def check_school():
    if school_entry.get() == "济南校区":
        get_ji(school_entry.get(),
               building_entry.get(),
               room_entry.get(),
               selected_value.get())

    elif school_entry.get() == "曲阜校区":
        get_qu(school_entry.get(),
               building_entry.get(),
               room_entry.get(),
               selected_value.get())
    else:
        messagebox.showinfo("fatal", "校区设置出现问题,请重试 !")

# 保存设置功能
def save_option():
    try:
        # 同目录下创建config.txt文件,并自动处理可能的异常
        f = open("config.txt", "w", encoding="utf-8")
        if school_entry.get() and building_entry.get() and room_entry.get() and selected_value.get():
            f.write("School:" + school_entry.get() + "\n" +
                    "Building:" + building_entry.get() + "\n" +
                    "Room:" + room_entry.get() + "\n" + "Mode:" + str(selected_value.get()))
            messagebox.showinfo("Success", "保存成功 !")
            f.close()
        else:
            messagebox.showinfo("Waring", "信息不完整,保存失败 !")
            f.close()
    except:
        messagebox.showinfo("Error", "保存失败 !")

# 打开结果文件 功能
def open_f():
    try:
        os.startfile("result.txt")
    except:
        messagebox.showinfo("Error", "没有找到存储文件 !")

# 清楚 信息展示框里的所有信息,以展示最新信息
def clear_text():
    t1.delete('1.0', tk.END)

# 读取配置文件(config.txt),并将设置信息展示到GUI界面
def read_config():
    try:
        f = open("config.txt", "r", encoding="utf-8")
        lines = f.read()
        f.close()
        school = lines.split("\n")[0].split(":")[1]
        building = lines.split("\n")[1].split(":")[1]
        room = lines.split("\n")[2].split(":")[1]
        mode = lines.split("\n")[3].split(":")[1]
        return school, building, room, mode  # (str,str,str,str)
    except:
        return "济南校区", 0, 0, 1

# 处理选项 曲阜校区 的请求
def get_qu(school, building, room, mode):
    if int(building_entry.get()) < 1 or int(building_entry.get()) > 9:
        clear_text()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        t1.insert(1.0, current_time + "\n")
        t1.insert(2.0, "楼栋有误 !")
        return 0
    if int(room_entry.get()) < 100:
        clear_text()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        t1.insert(1.0, current_time + "\n")
        t1.insert(2.0, "房间号有误 !")
        return 0

    # 设置POST参数
    url = 'http://dkdj.qlit.edu.cn:9901/api/getSydl'
    room = room
    payload_qu = {
        'xiaoqu': f'{school}',
        'loudong': f'{building}号学生公寓',
        'room': f'{building}-{room}照明'
    }
    # 处理潜在的网络问题
    try:
        response = requests.post(url, data=payload_qu)
        data = response.text
        if mode == 1:
            clear_text()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t1.insert(1.0, current_time + "\n")
            t1.insert(2.0, f"{room}宿舍剩余电费:\n{data}")
        elif mode == 2:
            clear_text()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t1.insert(1.0, current_time + "\n")
            t1.insert(2.0, f"{room}宿舍剩余电费:\n{data}\n")
            with open("result.txt", "a") as f:
                f.write(room + "\t" + current_time + "\t" + data + "\n")
                f.close()
            t1.insert(4.0, "结果已保存 !")
        else:
            messagebox.showwarning("???", "未知的查询模式 !")
    except requests.exceptions.ConnectionError:
        clear_text()
        t1.insert(1.0, "获取数据失败,请重试 !")

# 处理选项 济南校区 请求
def get_ji(school, building, room, mode):
    if int(building_entry.get()) < 1 or int(building_entry.get()) > 12:
        clear_text()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        t1.insert(1.0, current_time + "\n")
        t1.insert(2.0, "楼栋有误 !")
        return 0
    if int(room_entry.get()) < 1100 or int(room_entry.get()) > 12670:
        clear_text()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        t1.insert(1.0, current_time + "\n")
        t1.insert(2.0, "房间号有误 !")
        return 0
    # 设置POST参数
    url = 'http://dkdj.qlit.edu.cn:9901/api/getSydl'
    room = room
    payload_ji = {
        'xiaoqu': f'{school}',
        'loudong': f'{building}号公寓照明',
        'room': f'{room}照明'
    }
    # 处理潜在的网络异常
    try:
        response = requests.post(url, data=payload_ji)
        data = response.text
        if mode == 1:
            clear_text()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t1.insert(1.0, current_time + "\n")
            t1.insert(2.0, f"{room}宿舍剩余电费:\n{data}")
        elif mode == 2:
            clear_text()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t1.insert(1.0, current_time + "\n")
            t1.insert(2.0, f"{room}宿舍剩余电费:\n{data}\n")
            with open("result.txt", "a") as f:
                f.write(room + "\t" + current_time + "\t" + data + "\n")
                f.close()
            t1.insert(4.0, "结果已保存 !")
        else:
            messagebox.showwarning("???", "未知的查询模式 !")
    except requests.exceptions.ConnectionError:
        clear_text()
        t1.insert(1.0, "获取数据失败,请重试 !")


# 设置GUI界面
option1, option2, option3, option4 = read_config()
root = tk.Tk()
root.title("电费查询")
root.geometry("500x300")

selected_value = tk.IntVar()
selected_value.set(option4)
# 规矩 模式 布局
mode_label = tk.Label(root, text="选择查询模式:", font=("黑体", 15))
mode_label.grid(row=0, column=1)
mode1 = tk.Radiobutton(root, text="仅查询", variable=selected_value, value=1, font=("黑体", 15))
mode1.grid(row=0, column=2, sticky=tk.W)
mode2 = tk.Radiobutton(root, text="查询并保存结果", variable=selected_value, value=2, font=("黑体", 15))
mode2.grid(row=0, column=2, sticky=tk.E, padx=(100, 0))
# 规划 校区选择 布局
school = tk.Label(root, text="校区:", font=("黑体", 15))
school.grid(row=1, column=1, padx=50)
school_entry = ttk.Combobox(root, values=["济南校区", "曲阜校区"], width=20, font=("黑体", 15))
school_entry.set(option1)
school_entry.grid(row=1, column=2, sticky=tk.W)
# 规划 楼栋及房间号 布局
building = tk.Label(root, text="楼栋:", font=("黑体", 15), width=20)
building.grid(row=2, column=1, pady=(5, 0))
building_entry = tk.Entry(root, font=("黑体", 15), width=20)
building_entry.insert(0, string=option2)
building_entry.grid(row=2, column=2, sticky=tk.W)
room = tk.Label(root, text="房间号:", font=("黑体", 15))
room.grid(row=3, column=1)
room_entry = tk.Entry(root, font=("黑体", 15))
room_entry.insert(0, string=option3)
room_entry.grid(row=3, column=2, sticky=tk.W)
# 规划 杂项 布局
save_op = tk.Button(root, text="保存当前设置", command=save_option, width=12, height=1, font=("黑体", 15))
open_re = tk.Button(root, text="打开结果文件", command=open_f, width=12, height=1, font=("黑体", 15))
open_re.grid(row=4, column=2, sticky=tk.W)
save_op.grid(row=4, column=2, sticky=tk.E, padx=(15, 0))
# 规划 查询按钮 布局
send = tk.Button(root, text="查询", command=lambda: check_school()
                 , width=10, height=2, bg="PaleTurquoise1", font=("黑体", 15))
send.grid(row=4, column=1, pady=10)
# 规划 信息展示框 布局
t1 = tk.Text(root, height=4, width=25, font=("黑体", 15))
t1.grid(row=5, column=2, sticky=tk.W)
# 设置字体缩放以及DPI问题
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor / 75)
root.mainloop()
