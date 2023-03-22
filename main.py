import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
import time
import cv2
import pyautogui
import numpy as np


def get_img():
    """
    截取全屏幕
    :return: 保存全屏幕图片
    """
    # 将屏幕截图保存
    pyautogui.screenshot().save("./pic/screenshot.png")

def get_xy(img_model_path):
    """
    用来判定游戏画面的点击坐标
    :param img_model_path:用来检测的模板图片的路径
    :return: 以元组形式返回检测到的区域的中心坐标
    """
    #获取屏幕截图
    get_img()
    # 载入截图
    img = cv2.imread("./pic/screenshot.png")
    # 图像模板
    img_terminal = cv2.imread(img_model_path)
    #读取模板的宽度、高度和通道数
    h , w , c =img_terminal.shape
    #进行模板匹配
    result = cv2.matchTemplate(img , img_terminal,cv2.TM_SQDIFF_NORMED)  #result的type是 <class 'numpy.ndarray'>
    #解析出匹配区域的左上角坐标
    upper_left = cv2.minMaxLoc(result)[2]
    #计算匹配区域的右下角坐标
    lower_right = (upper_left[0]+w,upper_left[1]+h)
    #计算中心区域的坐标并返回
    avg = (int((upper_left[0]+lower_right[0])/2),int((upper_left[1]+lower_right[1])/2))
    return avg

def is_img(img_model_path, value):
    """
    检测有没有目标图片
    :param img_model_path: 目标图片 类型:filename
    :param value: 相似度阈值 类型:float
    :return: True or False
    """
    #获取屏幕截图
    get_img()
    img_rgb = cv2.imread("./pic/screenshot.png")
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(img_model_path, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        # 找到目标图片返回真
        return True
    else:
        return False

def auto_click(var_avg):
    """
    接收一个元组参数，自动点击
    :param var_avg: 坐标（元组形式）
    :return: None
    """
    pyautogui.click(var_avg[0],var_avg[1],button='left')
    time.sleep(1)



def routine(img_model_path,name):
    avg = get_xy(img_model_path)
    print(f'正在点击{name}')
    auto_click(avg)


#理智不足会话框
def notenough():
    print('理智不足，进程结束')
    showwarning("警告","理智不足，进程结束")


#判断代理指挥是否勾选
def is_dlzhyes():
    # 获取屏幕截图
    get_img()
    # 载入截图
    img = cv2.imread("./pic/screenshot.png")
    # 图像模板
    img_terminal = cv2.imread("./pic/terminal_dlzhyes.png")
    # 读取模板的宽度、高度和通道数
    h, w, c = img_terminal.shape
    # 进行模板匹配
    result = cv2.matchTemplate(img, img_terminal, cv2.TM_SQDIFF_NORMED)  # result的type是 <class 'numpy.ndarray'>
    # 解析出匹配区域的左上角坐标
    upper_left = cv2.minMaxLoc(result)[2]
    # 计算匹配区域的右下角坐标
    lower_right = (upper_left[0] + w, upper_left[1] + h)
    # ROI始末点坐标
    startX = upper_left[0]
    startY = upper_left[1]
    endX = lower_right[0]
    endY = lower_right[1]
    # 切片获取ROI
    roi = img[startY:endY, startX:endX]
    # 将ROI和模板匹配，检验找到的是否为模板
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("./pic/terminal_dlzhyes.png", 0)
    res = cv2.matchTemplate(roi_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        # 找到目标图片返回真,说明代理指挥已勾选
        return True
    else:
        return False



def operation_LS_4():
    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_zy.png', '资源')
    routine('./pic/terminal_zsyx.png', '战术演习')
    routine('./pic/terminal_LS_4.png', 'LS-4')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)

def operation_2_1():
    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_ztq.png', '主题曲')
    routine('./pic/terminal_ylts.png', '异卵同生')
    time.sleep(1)
    t=0
    while(t<8):
        '''向左滑8次，滑到最左边的关卡'''
        pyautogui.dragRel(150, 0, duration=0.2)# 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
        pyautogui.moveRel(-150, 0, duration=0.2)# 从当前位置右移150像素
        time.sleep(0.5)
        t += 1
    time.sleep(2)
    routine('./pic/terminal_2_1.png', '2-1')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)

def operation_2_2():
    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_ztq.png', '主题曲')
    routine('./pic/terminal_ylts.png', '异卵同生')
    time.sleep(1)
    t=0
    while(t<8):
        '''向左滑8次，滑到最左边的关卡'''
        pyautogui.dragRel(150, 0, duration=0.2)# 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
        pyautogui.moveRel(-150, 0, duration=0.2)# 从当前位置右移150像素
        time.sleep(0.5)
        t += 1
    time.sleep(2)
    routine('./pic/terminal_2_2.png', '2-2')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)


def operation_1_7():
    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_ztq.png', '主题曲')
    routine('./pic/terminal_huanmie.png', '幻灭')
    routine('./pic/terminal_juexing.png', '觉醒')
    pyautogui.moveRel(100, 300, duration=0.2)  # 鼠标按照当前点向右移动100px，向下移动500px这个方向移动
    pyautogui.dragRel(400, 0, duration=0.5)  # 按住鼠标左键，用0.5秒钟把鼠标向右拖拽
    pyautogui.moveRel(-400, 0, duration=0.2)  # 鼠标按照当前点向右移动-400px，向下移动0px这个方向移动
    pyautogui.dragRel(400, 0, duration=0.5)  # 按住鼠标左键，用0.5秒钟把鼠标向右拖拽
    time.sleep(1)
    routine('./pic/terminal_part2.png', '黑暗时代2')
    time.sleep(1)
    t=0
    while(t<6):
        pyautogui.dragRel(100, 0, duration=0.2)# 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
        pyautogui.moveRel(-100, 0, duration=0.2)# 从当前位置右移100像素
        t += 1
    time.sleep(2)
    pyautogui.dragRel(-400, 0, duration=0.2)# 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
    pyautogui.moveRel(400, 0, duration=0.2)# 从当前位置右移100像素
    time.sleep(2)
    routine('./pic/terminal_1_7.png', '1-7')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行',i,'次')
        time.sleep(2)


def operation_PR_B_1():

    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_zy.png', '资源')
    pyautogui.moveRel(0, -500, duration=0.2)  # 鼠标按照当前点向右移动0px，向下移动-500px这个方向移动
    pyautogui.dragRel(-200, 0, duration=0.5)  # 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
    time.sleep(2)
    routine('./pic/terminal_cklx.png', '摧枯拉朽')
    routine('./pic/terminal_PR_B_1.png', 'PR-B-1')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)

def operation_PR_C_1():

    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_zy.png', '资源')
    pyautogui.moveRel(0, -500, duration=0.2)  # 鼠标按照当前点向右移动0px，向下移动-500px这个方向移动
    pyautogui.dragRel(-150, 0, duration=0.5)  # 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
    time.sleep(2)
    routine('./pic/terminal_sbkd.png', '势不可挡')
    routine('./pic/terminal_PR_C_1.png', 'PR-C-1')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)

def operation_PR_D_1():
    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_zy.png', '资源')
    pyautogui.moveRel(0, -500, duration=0.2)  # 鼠标按照当前点向右移动0px，向下移动-500px这个方向移动
    pyautogui.dragRel(-150, 0, duration=0.5)  # 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
    time.sleep(2)
    routine('./pic/terminal_sxsz.png', '身先士卒')
    routine('./pic/terminal_PR_D_1.png', 'PR-D-1')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.9):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)

def operation_CE_3():

    cs = int(spcs.get())
    i = 0
    routine('./pic/terminal_zd.png', '终端')
    routine('./pic/terminal_zy.png', '资源')
    pyautogui.moveRel(0, -500, duration=0.2)  # 鼠标按照当前点向右移动0px，向下移动-500px这个方向移动
    pyautogui.dragRel(150, 0, duration=0.5)  # 按住鼠标左键，用0.2秒钟把鼠标向左拖拽
    time.sleep(2)
    routine('./pic/terminal_hwys.png', '货物运送')
    routine('./pic/terminal_CE_3.png', 'CE-3')
    if is_dlzhyes()==False:
        routine('./pic/terminal_dlzh.png', '代理指挥')
    while( i < cs ):
        routine('./pic/terminal_start.png', '开始行动')
        time.sleep(0.3)
        if is_img('./pic/terminal_lznotenough.png', 0.8):
            notenough()
            break
        routine('./pic/terminal_start_again.png', '开始战斗')
        while(1):
            if is_img('./pic/terminal_over.png', 0.8):
                time.sleep(3)
                routine('./pic/terminal_over.png', '行动结束')
                break
            time.sleep(1)
        i += 1
        print('已执行', i, '次')
        time.sleep(2)

def start():
    if v.get() == 'LS-4  作战记录':
        operation_LS_4()
    elif v.get() == '2-1  异铁':
        operation_2_1()
    elif v.get() == '2-2  糖':
        operation_2_2()
    elif v.get() == '1-7  固源岩':
        operation_1_7()
    elif v.get() == 'PR-B-1  狙击/术师芯片':
        operation_PR_B_1()
    elif v.get() == 'PR-C-1  先锋/辅助芯片':
        operation_PR_C_1()
    elif v.get() == 'PR-D-1  近卫/特种芯片':
        operation_PR_D_1()
    elif v.get() == 'CE - 3  龙门币':
        operation_CE_3()
    else:
        print('未选择关卡')






#界面
root = tk.Tk()
# 标题
root.title("明日方舟自动刷关")
#默认大小和位置
w=300
h=60
root.geometry("%dx%d"%(w,h))
#背景颜色设置
root['background']="#ffffff"

#label"关卡："
label1 = tk.Label(root,text="关卡：", width=1, height=1,font=("arial",12,"bold"), padx=1,pady=1,bg='#FFFACD', anchor='se')
label1.place(relwidth=0.2,relheight=0.5,relx=0,rely=0)

#下拉列表
list = ('LS-4  作战记录','2-1  异铁','2-2  糖','1-7  固源岩','PR-B-1  狙击/术师芯片','PR-C-1  先锋/辅助芯片','PR-D-1  近卫/特种芯片','CE - 3  龙门币')
v = tk.StringVar(root)
om = OptionMenu(root,v,*list).place(relwidth=0.6,relheight=0.5,relx=0.2,rely=0)



#label执行次数
label_cs = tk.Label(root,text="次数：", width=1, height=1,font=("arial",12,"bold"), padx=1,pady=1,bg='#ffffff', anchor='se')
label_cs.place(relwidth=0.2,relheight=0.5,relx=0,rely=0.5)

#执行次数
spcs = Spinbox(root,from_=1,to=20)
spcs.place(relwidth=0.2,relheight=0.5,relx=0.2,rely=0.5)


#开始按钮
button_start = tk.Button(text='开始', command=lambda: start())
button_start.place(relwidth=0.2,relheight=0.5,relx=0.8,rely=0)


#消息循环
root.mainloop()


