from pandas import Series, DataFrame, read_pickle
import time
import matplotlib.pyplot as plt
from types import MethodType

def select_time(s, start_time, end_time):
    if start_time == 'default':
        start_timestamp = s.index[0]
    else :
        try:
            start_timestamp = time.mktime(time.strptime(start_time ,"%Y-%m-%d %H:%M"))
        except ValueError:
            messagebox.showinfo(title='', message='！！起始日期格式错误！！，应为 \'YYYY-mm-dd MM:HH\' 如 \'2020-05-05 15:05\'\n**已默认从第一条数据开始**\n')
            start_timestamp = s.index[0]
    #处理start_time参数
    if end_time == 'default':
        end_timestamp = s.index[-1]
    else :
        try:
            end_timestamp = time.mktime(time.strptime(end_time ,"%Y-%m-%d %H:%M"))
        except ValueError:
            messagebox.showinfo(title='', message='！！截止日期格式错误！！，应为 \'YYYY-mm-dd MM:HH\' 如\'2020-05-05 15:05\'\n**已默认最后一条数据截止**\n')
            end_timestamp = s.index[-1]
    #对series进行切片（选定的时间段）
    return s[(s.index >= start_timestamp) & (s.index <= end_timestamp)]

def prep_plt(kinds):
    kinds_len = len(kinds)
    if kinds_len == 1:
        sub_row = 1
        sub_col = 1
        fig = plt.figure(figsize=(12,6),facecolor='w')
    elif kinds_len == 2:
        sub_row = 1
        sub_col = 2
        fig = plt.figure(figsize=(18,6),facecolor='w')
    elif (kinds_len == 3 or kinds_len == 4):
        sub_row = 2
        sub_col = 2
        fig = plt.figure(figsize=(18,12),facecolor='w')
    elif (kinds_len == 5 or kinds_len == 6):
        sub_row = 2
        sub_col = 3
        fig = plt.figure(figsize=(24,16),facecolor='w')
    elif kinds_len == 7:
        sub_row = 3
        sub_col = 3
        fig = plt.figure(figsize=(24,24),facecolor='w')
    else :
        print('error')
        
    return sub_row, sub_col, fig

def sort_by(s, k, av):
    ls = []
    for i in s.index:
        d = dict(time = i)
        for j in range(len(s[i])):
            #display(s[i])
            row_av = s[i].iloc[j,0]
            row_data = int(s[i].iloc[j][k])
            d.update({row_av:row_data})
        #print(d)
        ls.append(d)
    #print(ls)
    df = DataFrame(ls)
    df.set_index(['time'], inplace=True)
    if av != 'all':
        df = df[av]
    return df

def plt_line(df, title, fig, sub_row, sub_col, t):
    ax = fig.add_subplot(sub_row, sub_col, t)
    df.plot(ax=ax)
    ax.grid()
    strtime = []
    for i in ax.get_xticks():
        strtime.append(time.strftime("%m/%d\n%H:%M",time.localtime(i)))
    ax.set_xticklabels(strtime)
    ax.set_title(title)

def plt_bar(df, title, fig, sub_row, sub_col, t):
    ax = fig.add_subplot(sub_row, sub_col, t)
    df.plot(kind='bar', ax=ax)
    ax.grid()
    #strtime = []
    #for i in ax.get_xticks():
    #    strtime.append(time.strftime("%m/%d\n%H:%M",time.localtime(i)))
    #ax.set_xticklabels(strtime)
    ax.set_title(title)

def get_interval(df, interval):
    interval_df = DataFrame()
    first = df.index[0]
    last = df.index[-1]
    start = first
    end = start
    while(end <= last):
        end = start + interval
        if df[(df.index >= start) & (df.index <= end)].empty : #循环的最后一次有可能切片为空
            break
        t_df = df[(df.index >= start) & (df.index <= end)]
        #print(t_df.index)
        time_str = time.strftime("%m/%d\n%H:%M",time.localtime(t_df.index[-1]))
        interval_df[time_str] = t_df.iloc[-1]-t_df.iloc[0]
        start = end
    return interval_df.T
    #return t_df.iloc[-1]-t_df.iloc[0]
    #return t_df

def av_title():
    out = str('av号与标题对照如下：\n')
    for i in range(len(dat.av_ls)):
        out = str(str(out) + str(dat.av_ls[i]) + '\t' + str(dat.title[i]) + '\n')
    return out

class data():
    title_ls = list()
    av_ls = list()
    def __init__(self):
        s = read_pickle('time_series.pkl')
        self.title = list(s[s.index[-1]]['title'])
        self.av_ls = list(s[s.index[-1]]['AV'])
        #self.av_ls = list(s[s.index[-1]]['id'])



def accumulate(kinds='all', start_time='default', end_time='default', av = 'all'):
    # 处理默认kinds参数
    if kinds == 'all':
        kinds = ['view', 'like', 'coin', 'favourite', 'danmu', 'share', 'reply'] 
    # 读取爬虫所保存的数据
    s = read_pickle('time_series.pkl')
    # 在series的时候对时间进行选取更为方便
    s = select_time(s, start_time, end_time)
    # 为fig做准备
    sub_row, sub_col, fig = prep_plt(kinds)
    #循环画多个子图
    for i in range(len(kinds)) :
        # 将series转换为dataframe
        df = sort_by(s, kinds[i], av)
        # 画子图
        plt_line(df, kinds[i], fig, sub_row, sub_col, i+1)
    fig.show()


def increase(kinds='all', start_time='default', end_time='default', av = 'all', interval=86400):
    # 处理默认kinds参数
    if kinds == 'all':
        kinds = ['view', 'like', 'coin', 'favourite', 'danmu', 'share', 'reply'] 
    # 读取爬虫所保存的数据
    s = read_pickle('time_series.pkl')
    # 在series的时候对时间进行选取更为方便
    s = select_time(s, start_time, end_time)
    # 为fig做准备
    sub_row, sub_col, fig = prep_plt(kinds)
    #循环画多个kinds子图
    for i in range(len(kinds)) :
        # 将series转换为dataframe
        df = sort_by(s, kinds[i], av)
        df_increase = get_interval(df, interval)
        # 画子图
        plt_bar(df_increase, kinds[i], fig, sub_row, sub_col, i+1)
    fig.show()


dat = data()

#####
import tkinter as tk
from tkinter import messagebox
import ctypes
from tkinter import scrolledtext

# 第1步，实例化object，建立窗口window
window = tk.Tk()
#window.geometry('1000x1000')
# 高分屏
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#调用api获得当前的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
#设置缩放因子
window.tk.call('tk', 'scaling', ScaleFactor/75)

# 第2步，给窗口的可视化起名字
window.title('My Window')

main_frame = tk.Frame(window)
main_frame.pack()



#布置下边

bottom_frame = tk.Frame(main_frame)
bottom_frame.pack(side='bottom')

###滚动条---
bottom_scroll = tk.Scrollbar(bottom_frame)
bottom_canvas = tk.Canvas(bottom_frame, yscrollcommand=bottom_scroll.set, width=1000)
bottom_scroll.config(command=bottom_canvas.yview)
bottom_scroll.pack(side=tk.RIGHT, fill=tk.Y) 
bottom_subframe=tk.Frame(bottom_canvas) #Create the frame which will hold the widgets
bottom_canvas.pack(side="bottom", fill="both", expand=True)
#Updated the window creation
bottom_canvas.create_window(0,0,window=bottom_subframe, anchor='nw')
tk.Label(bottom_subframe,text=av_title(), justify='left').pack()
#Updated the screen before calculating the scrollregion
bottom_frame.update()
bottom_canvas.config(scrollregion=bottom_canvas.bbox("all"))
###---

###滚轮
def _on_mousewheel(event): 
    bottom_canvas.yview_scroll(int(-1*(event.delta/120)), "units") 
bottom_canvas.bind("<MouseWheel>", _on_mousewheel)
###---

#布置上边
top_frame = tk.Frame(main_frame)
top_frame.pack(side='top')

kinds_frame = tk.Frame(top_frame)
kinds_frame.pack(side='left')

kinds_label = tk.Label(kinds_frame, text='选择kind')
kinds_label.pack(anchor='w')
#布置kinds多选栏
kinds_ls = ['view', 'like', 'coin', 'favourite', 'danmu', 'share', 'reply']
kinds_var_ls = list()
for i in range(len(kinds_ls)):
    kinds_var_ls.append(tk.BooleanVar())
    tk.Checkbutton(kinds_frame, text=kinds_ls[i], variable=kinds_var_ls[i], onvalue=1, offvalue=0).pack(anchor=tk.W)


# av_frame
av_frame = tk.Frame(top_frame)
av_frame.pack(side='left')
av_label = tk.Label(av_frame, text='选择av号')
av_label.pack(side='top')
# 布置av多选栏
av_var_ls = list()

av_scroll = tk.Scrollbar(av_frame)
av_canvas = tk.Canvas(av_frame, yscrollcommand=av_scroll.set, width=200)
av_scroll.config(command=av_canvas.yview)
av_scroll.pack(side='right', fill='y')
av_subframe = tk.Frame(av_canvas)
av_canvas.pack(side='bottom', fill='both', expand=True)
av_canvas.create_window(0,0,window=av_subframe, anchor='nw')

for i in range(len(dat.av_ls)):
    av_var_ls.append(tk.BooleanVar())
    tk.Checkbutton(av_subframe, text=dat.av_ls[i], variable=av_var_ls[i], onvalue=1, offvalue=0).pack(anchor=tk.W)

av_frame.update()
av_canvas.config(scrollregion=av_canvas.bbox('all'))

# date_frame
date_frame = tk.Frame(top_frame)
date_frame.pack(side='left')
tk.Label(date_frame, text='格式：YYYY-mm-dd MM:HH').pack()
starttime_label = tk.Label(date_frame, text='输入起始时间')
starttime_label.pack()
starttime_entry = tk.Entry(date_frame)
starttime_entry.insert('end', 'default')
starttime_entry.pack()

endtime_label = tk.Label(date_frame, text='输入终止时间')
endtime_label.pack()
endtime_entry = tk.Entry(date_frame)
endtime_entry.insert('end', 'default')
endtime_entry.pack()

# interval_frame
interval_frame = tk.Frame(top_frame)
interval_frame.pack(side='left')
tk.Label(interval_frame,text='设置increase的interval\n(单位:小时)').pack(side='top')
interval_tk = tk.StringVar()
tk.Scale(interval_frame, from_=0.5, to=48, resolution=0.5, length=400, variable=interval_tk).pack()

#画图按钮frame
button_frame = tk.Frame(main_frame)
button_frame.pack(side='bottom')

# def init_increase():
def pre_increase():
    checked_kinds_ls = list()
    for i in range(len(kinds_ls)):
        if kinds_var_ls[i].get():
            checked_kinds_ls.append(kinds_ls[i])
    checked_av_ls = list()
    for i in range(len(dat.av_ls)):
        if av_var_ls[i].get():
            checked_av_ls.append(dat.av_ls[i])
    #messagebox.showinfo(title='Hi', message=str(int(float(interval_tk.get())*3600)))
    increase(kinds=checked_kinds_ls, start_time=str(starttime_entry.get()), end_time=str(endtime_entry.get()), av=checked_av_ls, interval=int(float(interval_tk.get())*3600))

increase_button = tk.Button(button_frame, text='draw increase', command=pre_increase)
increase_button.pack(side='left')

def pre_accumulate():
    checked_kinds_ls = list()
    for i in range(len(kinds_ls)):
        if kinds_var_ls[i].get():
            checked_kinds_ls.append(kinds_ls[i])
    checked_av_ls = list()
    for i in range(len(dat.av_ls)):
        if av_var_ls[i].get():
            checked_av_ls.append(dat.av_ls[i])
    #messagebox.showinfo(title='Hi', message=str(checked_av_ls))
    accumulate(kinds=checked_kinds_ls, start_time=str(starttime_entry.get()), end_time=str(endtime_entry.get()), av=checked_av_ls)

accumulate_button = tk.Button(button_frame, text='draw accumulate', command=pre_accumulate)
accumulate_button.pack(side='right')

# 主窗口循环显示
window.mainloop()
