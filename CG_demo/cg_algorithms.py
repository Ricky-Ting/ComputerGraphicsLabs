#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if x0 == x1 and y0 == y1:
        result.append((x0, y0));
        return result
    
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        delta_x = x1 - x0
        delta_y = y1 - y0
        steps = max(abs(delta_x), abs(delta_y))
        dx = delta_x/steps
        dy = delta_y/steps
        cur_x = x0
        cur_y = y0
        for i in range(steps):
            result.append([int(cur_x+0.5), int(cur_y+0.5)])
            cur_x += dx
            cur_y += dy

        result.append([x1, y1])

    elif algorithm == 'Bresenham':
        steep = abs(y1-y0) > abs(x1-x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        delta_x = x1 - x0
        delta_y = abs(y1 - y0)
        error = delta_x // 2
        y = y0
        if y0 > y1:
            ystep = -1
        else:
            ystep = 1
        for x in range(x0, x1+1):
            if steep:
                result.append([y, x])
            else:
                result.append([x, y])
            error = error - delta_y
            if error < 0:
                y = y + ystep
                error = error + delta_x

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    result += draw_line([p_list[0], p_list[len(p_list)-1]], algorithm)
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    [x0, y0], [x1, y1] = p_list
    x_mid, y_mid = round((x0+x1)/2), round((y0+y1)/2)
    a, b = round(abs(x1-x0)/2), round(abs(y1-y0)/2)

    x, y = 0, b

    # decision boundary 1
    d1 = ((b * b) - (a * a * b) + (0.25 * a * a))

    # region 1
    while (b*b*x < a*a*y):  
        result.append([x+x_mid, y+y_mid])
        result.append([x+x_mid, -y+y_mid])
        result.append([-x+x_mid, y+y_mid])
        result.append([-x+x_mid, -y+y_mid])

        if (d1 < 0):  
            d1 = d1 + b*b*(2*x + 3)
            x += 1
        else: 
            d1 = d1 + b*b*(2*x + 3) + 2*a*a*(1-y)
            x += 1  
            y -= 1  


    # decision boundary 2
    d2 = (((b * b) * ((x + 0.5) * (x + 0.5))) + ((a * a) * ((y - 1) * (y - 1))) - (a * a * b * b)) 
  
    # region 2  
    while (y >= 0): 
        result.append([x+x_mid, y+y_mid])
        result.append([x+x_mid, -y+y_mid])
        result.append([-x+x_mid, y+y_mid])
        result.append([-x+x_mid, -y+y_mid])
  
        if (d2 > 0): 
            d2 = d2 + (a * a) * (3 - 2 *y)
            y -= 1  
        else: 
            d2 = d2 + (a * a) * (3 - 2 *y) + 2 * b * b * (x+1)
            y -= 1  
            x += 1 
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        n = len(p_list)
        if n<2:
            return result
        t = 0.001
        result.append(p_list[0])
        for i in range(1, 1000):
            result.append(draw_Bezier(p_list, t))
            t = t + 0.001
        result.append(p_list[n-1])
    elif algorithm == 'B-spline':
        k = 3 # 3阶
        n = len(p_list) - 1
        #T = []
        #for i in range(n+k+1 + 1):
        #    T.append(i)
        step = 0.001

        for T in range(k, n+1):
            t = float(T)
            while(t < T+1):
                result.append(getBsplinePoint(p_list, T, t, k+1))
                t = t + 0.001
    return result



def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x, y in p_list:
        result.append([x+dx, y+dy])
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    cosTheta = math.cos(r/180 * math.pi)
    sinTheta = math.sin(r/180 * math.pi)
    for x1,y1 in p_list:
        dx = x1 - x
        dy = y1 - y
        result.append([round(x + dx*cosTheta - dy*sinTheta), round(y + dx*sinTheta + dy*cosTheta)])
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x1, y1 in p_list:
        dx = x1 - x
        dy = y1 - y 
        result.append([round(x + dx*s), round(y + dy*s)])
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """

    if algorithm == 'Cohen-Sutherland':
        A = p_list[0]
        B = p_list[1]
        result = []
        # 从右到左 为 左边界 右边界 上边界 下边界

        if A[0] == B[0]:
            if A[0] < x_min or A[0] > x_max:
                result.append([0, 0])
                result.append([0, 0])
                return result
            else:
                if A[1] > y_max:
                    A[1] = y_max
                elif A[1] < y_min:
                    A[1] = y_min
                if B[1] > y_max:
                    B[1] = y_max
                elif B[1] < y_min:
                    B[1] = y_min
                result.append(A)
                result.append(B)
                return result
        elif A[1] == B[1]:
            if A[1] < y_min or A[1] > y_max:
                result.append([0, 0])
                result.append([0, 0])
                return result
            else:
                if A[0] > x_max:
                    A[0] = x_max
                elif A[0] < x_min:
                    A[0] = x_min
                if B[0] > x_max:
                    B[0] = x_max
                elif B[0] < x_min:
                    B[0] = x_min
                result.append(A)
                result.append(B)
                return result

        while True:
            A_bits = 0
            B_bits = 0

            if A[0] < x_min:
                A_bits = A_bits + 0x1
            if A[0] > x_max:
                A_bits = A_bits + 0x2
            if A[1] < y_min:
                A_bits = A_bits + 0x4
            if A[1] > y_max:
                A_bits = A_bits + 0x8

            if B[0] < x_min:
                B_bits = B_bits + 0x1
            if B[0] > x_max:
                B_bits = B_bits + 0x2
            if B[1] < y_min:
                B_bits = B_bits + 0x4
            if B[1] > y_max:
                B_bits = B_bits + 0x8

            if A_bits == 0 and B_bits == 0: # 均在区域内
                result.append( [round(A[0]), round(A[1]) ] )
                result.append( [round(B[0]), round(B[1]) ] )
                return result
            if A_bits&B_bits != 0:
                result.append([0,0])
                result.append([0,0])
                return result
            k = (B[1] - A[1]) / (B[0] - A[0])
            if A_bits&0x1 != 0 or B_bits&0x1 != 0:
                if A_bits&0x1 == 0:
                    A_bits, B_bits = B_bits, A_bits
                    A, B = B, A
                A = [x_min, A[1] + k*(x_min - A[0])]
                continue
    
            if A_bits&0x2 != 0 or B_bits&0x2 != 0:
                if A_bits&0x2 == 0:
                    A_bits, B_bits = B_bits, A_bits
                    A, B = B, A
                A = [x_max, A[1] + k*(x_max - A[0])]
                continue
            if A_bits&0x4 != 0 or B_bits&0x4 != 0:
                if A_bits&0x4 == 0:
                    A_bits, B_bits = B_bits, A_bits
                    A, B = B, A
                A = [(y_min - A[1])/k + A[0], y_min]
                continue
            if A_bits&0x8 != 0 or B_bits&0x8 != 0:
                if A_bits&0x8 == 0:
                    A_bits, B_bits = B_bits, A_bits
                    A, B = B, A
                A = [(y_max - A[1])/k + A[0], y_max]
                continue
        
        










def draw_Bezier(p_list, t):
    n = len(p_list)
    P = []
    for point in p_list:
        P.append(point)
    i = n
    while(i>1):
        for j in range(0, i-1):
            x = P[j][0]*t + P[j+1][0]*(1-t)
            y = P[j][1]*t + P[j+1][1]*(1-t)
            P[j] = [x, y]
        i = i - 1

    return [round(P[0][0]), round(P[0][1])]

    '''
    for i = n; i>1; i--:
        for j = 0; j<i-1; j++:
            P[j] = P[j]*t + P[j+1]*(1-t)
    return P[0]
    '''


def getBsplinePoint(p_list, T, t, k):
    x = 0.0 
    y = 0.0
    for i in range(len(p_list)):
        p = p_list[i]
        alpha = getN(i, k, t, T)
        x = x + alpha * p[0]
        y = y + alpha * p[1]
    return [round(x), round(y)]

def getN(i, k, t, T):
    if k == 1:
        if i == T:
            return 1
        else:
            return 0
    return (t-i)/(k-1)*getN(i, k-1, t, T) + (i+k-t)/(k-1)*getN(i+1, k-1, t, T)
