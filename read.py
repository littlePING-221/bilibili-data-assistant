import pandas as pd
import time
import matplotlib.pyplot as plt

def draw(kinds='all', start_time='default', end_time='default'):
    s = pd.read_pickle('time_series.pkl')
    #处理kinds参数
    if kinds == 'all':
        kinds = ['view', 'like', 'coin', 'favourite', 'danmu', 'share', 'reply']
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
    else:
        print('error')
    #处理start_time参数
    if start_time == 'default':
        start_timestamp = s.index[0]
    else :
        try:
            start_timestamp = time.mktime(time.strptime(start_time ,"%Y-%m-%d %H:%M"))
        except ValueError:
            print('！！起始日期格式错误！！，应为 \'YYYY-mm-dd MM:HH\' 如 \'2020-05-05 15:05\'\n**已默认从第一条数据开始**\n')
            start_timestamp = s.index[0]
    #处理start_time参数
    if end_time == 'default':
        end_timestamp = s.index[-1]
    else :
        try:
            end_timestamp = time.mktime(time.strptime(end_time ,"%Y-%m-%d %H:%M"))
        except ValueError:
            print('！！截止日期格式错误！！，应为 \'YYYY-mm-dd MM:HH\' 如\'2020-05-05 15:05\'\n**已默认最后一条数据截止**\n')
            end_timestamp = s.index[-1]
    #对series进行切片（选定的时间段）
    s = s[(s.index >= start_timestamp) & (s.index <= end_timestamp)]
    #为画图准备数据
    title = list(s[s.index[-1]]['title'])
    av = list(s[s.index[-1]]['AV'])
    for k in range(kinds_len):
        ls = []
        for i in s.index:
            row = [i]
            for j in range(len(s[i])):
                row.append(s[i][kinds[k]][j])
            ls.append(row)
        df = pd.DataFrame(ls)
        #df[0] = df[0].map(lambda x : time.strftime("%m/%d %H",time.localtime(x)))
        df.set_index([0], inplace=True)
        df.set_axis(av, axis='columns', inplace=True)
        #display(df)
        ax = fig.add_subplot(sub_row, sub_col, k+1)
        ax.plot(df)
        ax.grid()
        strtime = []
        for i in ax.get_xticks():
            strtime.append(time.strftime("%m/%d\n%H:%M",time.localtime(i)))
        ax.set_xticklabels(strtime)
        #plt.xticks(rotation=-90)
        ax.set_title(kinds[k])
    plt.legend(av)
    fig.show()
    print('av号与标题对照如下：')
    for i in range(len(av)):
        print(str(av[i]) + '\t' + str(title[i]))

draw(kinds = ['view','coin'], start_time = '2020-5-1 01:00', end_time = '2020-5-5 18:00')