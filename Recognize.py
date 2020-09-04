import os
import cv2
import numpy as np
import sys
import socket
import time

piece_template = cv2.imread('/Users/xunuo/PycharmProjects/tioayitiao/template.png',0)
piece_w, piece_h = piece_template.shape[::-1]

meth = eval('cv2.TM_CCORR_NORMED')
piece_base_height_1_2 = 25
#img = cv2.imread('2.png',0)
coef_time = 1.25

whitePoint = cv2.imread('/Users/xunuo/PycharmProjects/tioayitiao/img_canny的副本.jpg',0)
whitePoint_x, whitePoint_y = whitePoint.shape[::-1]

def getScreen():
    os.system("screencapture -R 5,200,570,1080 -o 2.png")

def control(time):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.50.171', 9999))
    s.send(str(time).encode('utf-8'))
    s.close()


def find_piece(img):
    res = cv2.matchTemplate(img, piece_template, meth)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    piece_x, piece_y = max_loc

    goal_x, goal_y = find_goal(img, piece_x, piece_y) #将棋子的左上角坐标传到find_goal函数中，求出

    if (goal_x==0 or goal_y==0):  #进行检查，如果goal_x或者goal_y有一个为0，则说明检测失败了。
        print("goal_x或者goal_y检测失败！！")
        sys.exit(0)
    piece_x = int(piece_x + piece_w / 2)#将piece_x改为棋子的底座中央的x坐标
    piece_y = piece_y + piece_h - piece_base_height_1_2#将piece_y改为棋子的底座中央的y坐标

    print(piece_x,piece_y,goal_x,goal_y)
    time = calcuTime(piece_x,piece_y,goal_x,goal_y)
    return time

def find_goal(img,piece_begin_x,piece_begin_y):  #求目标
    img2 = img.copy()
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)
    img_canny = cv2.Canny(img2, 1, 10)  #以上三行是将img转为canny，寻找边界
    goal_x = 0
    goal_y = 0
    for i in range(piece_begin_x, piece_begin_x + piece_w):   #这个循环的目的是把棋子覆盖的部分都去掉，防止干扰
        for j in range(piece_begin_y, piece_begin_y + piece_h):
            img_canny[j][i] = 0
    cv2.imwrite('resultOfCanny.png', img_canny)

    #尝试匹配whitePoint：
    res2 = cv2.matchTemplate(img_canny, whitePoint, meth)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
    if max_val2 > 0.54:
        print('found a white point!!')
        goal_x = max_loc2[0] + whitePoint_x//2
        goal_y = max_loc2[1] + whitePoint_y//2
    else:
        board_y_top = 0
        for i in img_canny[0:]:
            # print(i)
            if max(i):  # i是一整行像素的list，max(i)返回最大值，一旦最大值存在，则找到了board_y_top
                break
            board_y_top += 1
        print('test')
        # board_y_top的像素可能有多个 对它们的坐标取平均值
        goal_x = int(np.mean(np.nonzero(img_canny[board_y_top])))
        #从找到的落点方块的最高点开始扫描，找出x坐标和最高点相同的不为0的点，
        for row in img_canny[board_y_top:]:
            print(row[goal_x])
            if row[goal_x] == 255:
                break
            goal_y += 1
        goal_y = goal_y + board_y_top
    return goal_x, goal_y

def calcuTime(piece_x,piece_y,goal_x,goal_y):
    distance = np.sqrt(np.square(goal_y-piece_y) + np.square(goal_x-piece_x))
    time = int(coef_time * distance)
    return time

if __name__ == "__main__":
    while True:
        getScreen()            #截屏
        img = cv2.imread('2.png', 0)
        t = find_piece(img)  #返回的是需要按压时间
        print(t)
        control(t)
        time.sleep(3)
