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
        error = delta_x / 2
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
    dx = 2 * b * b * x  
    dy = 2 * a * a * y

    # region 1
    while (dx < dy):  
        result.append([x+x_mid, y+y_mid])
        result.append([x+x_mid, -y+y_mid])
        result.append([-x+x_mid, y+y_mid])
        result.append([-x+x_mid, -y+y_mid])

        if (d1 < 0):  
            x += 1;  
            dx = dx + (2 * b * b)  
            d1 = d1 + dx + (b * b)
        else: 
            x += 1;  
            y -= 1;  
            dx = dx + (2 * b * b)  
            dy = dy - (2 * a * a)
            d1 = d1 + dx - dy + (b * b)


    # decision boundary 2
    d2 = (((b * b) * ((x + 0.5) * (x + 0.5))) + ((a * a) * ((y - 1) * (y - 1))) - (a * a * b * b)) 
  
    # region 2  
    while (y >= 0): 
        result.append([x+x_mid, y+y_mid])
        result.append([x+x_mid, -y+y_mid])
        result.append([-x+x_mid, y+y_mid])
        result.append([-x+x_mid, -y+y_mid])
  
        if (d2 > 0): 
            y -= 1;  
            dy = dy - (2 * a * a);  
            d2 = d2 + (a * a) - dy;  
        else: 
            y -= 1;  
            x += 1;  
            dx = dx + (2 * b * b);  
            dy = dy - (2 * a * a);  
            d2 = d2 + dx - dy + (a * a);
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    pass


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
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


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
    pass
