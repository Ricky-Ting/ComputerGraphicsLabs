import gui
import sys, os
import math
import cg_algorithms as alg
import sip
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QMenu,
    QMessageBox,
    QInputDialog,
    QColorDialog,
    QFileDialog,
    QVBoxLayout,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QIcon, QImage, QPixmap
from PyQt5.QtCore import QRectF, Qt, QSize


def getAngle(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    cos_angle = (x1*x2 + y1*y2) / (math.sqrt(x1*x1 + y1*y1) * math.sqrt(x2*x2 + y2*y2))
    if cos_angle > 1.0:
        cos_angle = 1.0
    elif cos_angle < -1.0:
        cos_angle = -1.0
    angle = math.acos(cos_angle) / math.pi *180
    cross_product = x1*y2 - x2*y1
    if cross_product >= 0:
        return angle
    else:
        return -angle




class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_items = []

        self.paintColor = QColor(0, 0, 0)

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

    def updateStatusMsg(self):
        if self.status == '':
            self.main_window.statusBar().showMessage("空闲")
        elif self.status == 'line':
            self.main_window.statusBar().showMessage(self.temp_algorithm + "算法绘制线段")
        elif self.status == 'rect':
            self.main_window.statusBar().showMessage("绘制矩形")
        elif self.status == 'polygon':
            self.main_window.statusBar().showMessage(self.temp_algorithm + "算法绘制多边形")
        elif self.status == 'ellipse':
            self.main_window.statusBar().showMessage("中点法绘制椭圆")
        elif self.status == 'curve':
            self.main_window.statusBar().showMessage(self.temp_algorithm + "算法绘制曲线")
        elif self.status == 'select':
            self.main_window.statusBar().showMessage("选择图元")
        elif self.status == 'move':
            self.main_window.statusBar().showMessage("平移图元")
        elif self.status == 'rotate':
            self.main_window.statusBar().showMessage("旋转图元")
        elif self.status == 'scale':
            self.main_window.statusBar().showMessage("缩放图元")
        elif self.status == 'clip':
            self.main_window.statusBar().showMessage("裁剪线段")
        return




    def cursor_mode(self):
        self.status = ''
        self.temp_algorithm = ''
        self.temp_item = None
        self.temp_id = ''
        self.updateStatusMsg()

    def start_draw(self, item_type, item_id, algorithm):
        self.status = item_type
        self.temp_id = item_id
        self.temp_algorithm = algorithm
        self.temp_item = None
        self.updateStatusMsg()

    def finish_draw(self):
        self.temp_id = self.main_window.get_id(self.status)
        self.temp_item = None
        self.updateStatusMsg()

    def start_select(self):
        self.status = 'select'
        self.clear_selection()
        self.selected_items = []
        self.temp_item = None
        self.updateStatusMsg()

    def finish_select(self):
        self.status = ''
        self.temp_item = None
        self.updateStatusMsg()

    def start_move(self):
        self.status = 'move'
        self.temp_id = ''
        self.temp_item = None
        self.updateStatusMsg()

    def finish_move(self):
        self.status = ''
        self.temp_item = None
        self.updateStatusMsg()

    def start_rotate(self):
        self.status = 'rotate'
        self.temp_id = ''
        self.temp_item = None
        for item in self.selected_items:
            item.rotate_angle = 0
            item.rotate_center = []
        self.updateStatusMsg()

    def finish_rotate(self):
        self.status = ''
        self.temp_item = None
        for item in self.selected_items:
            item.rotate_angle = 0
            item.rotate_center = []
        self.updateStatusMsg()

    def start_scale(self):
        self.status = 'scale'
        self.temp_id = ''
        self.temp_item = None
        for item in self.selected_items:
            item.scale_ratio = 0
            item.scale_center = []
        self.updateStatusMsg()

    def finish_scale(self):
        self.status = ''
        self.temp_item = None
        for item in self.selected_items:
            item.scale_ratio = 0
            item.scale_center = []
        self.updateStatusMsg()

    def start_clip(self, algorithm):
        self.status = 'clip'
        self.temp_id = ''
        self.temp_item = None
        self.temp_algorithm = algorithm
        self.updateStatusMsg()

    def finish_clip(self):
        self.status = ''
        self.temp_item = None
        self.updateStatusMsg()



    def clear_selection(self):
        for item in self.selected_items:
            item.selected = False
            item.update()
        return

    def selection_changed(self, x, y, w, h):
        for item in self.selected_items:
            item.selected = False
            item.update()

        self.selected_items = QGraphicsView.items(self, x, y, w, h)

        for item in self.selected_items:
            item.selected = True
            item.update()

        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())

        if event.buttons() == Qt.LeftButton:
            if self.status == 'line':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                self.scene().addItem(self.temp_item)

            elif self.status == 'polygon':
                if self.temp_item is None:
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                    self.scene().addItem(self.temp_item)
                else:
                    self.temp_item.p_list.append([x, y])
                    self.temp_item.p_list.append([x, y])
            elif self.status == 'ellipse':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                self.scene().addItem(self.temp_item)
            elif self.status == 'curve':
                if self.temp_item is None:
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                    self.scene().addItem(self.temp_item)
                else:
                    length = len(self.temp_item.p_list)
                    self.temp_item.p_list[length-1] = [x, y]
                    self.temp_item.p_list.append([x, y])
            elif self.status == 'select':
                self.temp_item = MyItem("select_rect", self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                self.scene().addItem(self.temp_item)
            elif self.status == 'rect':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                self.scene().addItem(self.temp_item)
            elif self.status == 'move':
                self.temp_item = MyItem(self.temp_id, self.status, [[x,y]], self.temp_algorithm, self.paintColor)
            elif self.status == 'rotate':
                if self.temp_item is None:
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.paintColor)
                    self.scene().addItem(self.temp_item)
                    for item in self.selected_items:
                        item.rotate_center = [x, y]
                else:
                    self.temp_item.p_list.append([x, y])
            elif self.status == 'scale':
                if self.temp_item is None:
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.paintColor)
                    self.scene().addItem(self.temp_item)
                    for item in self.selected_items:
                        item.scale_center = [x, y]
                else:
                    self.temp_item.p_list.append([x, y])
            elif self.status == 'clip':
                self.temp_item = MyItem("clip_rect", self.status, [[x, y], [x, y]], self.temp_algorithm, self.paintColor)
                self.scene().addItem(self.temp_item)
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.temp_item is not None:
            if self.status == 'polygon':
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
            elif self.status == 'curve':
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
        self.updateScene([self.sceneRect()])
        super().mouseDoubleClickEvent(event)


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.temp_item is not None:
            if self.status == 'line':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'polygon':
                length = len(self.temp_item.p_list)
                self.temp_item.p_list[length-1] = [x, y]
            elif self.status == 'ellipse':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'curve':
                length = len(self.temp_item.p_list)
                self.temp_item.p_list[length-1] = [x, y]
            elif self.status == 'select':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'rect':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'move':
                dx = x - self.temp_item.p_list[0][0]
                dy = y - self.temp_item.p_list[0][1]
                self.temp_item.p_list[0] = [x, y]
                for item in self.selected_items:
                    item.p_list = alg.translate(item.p_list, dx, dy)
            elif self.status == 'rotate':
                if self.temp_item is not None and len(self.temp_item.p_list) == 2:
                    x0, y0 = self.temp_item.p_list[0]
                    x1, y1 = self.temp_item.p_list[1]
                    v1 = [x1-x0, y1-y0]
                    v2 = [x-x0, y-y0]
                    angle = getAngle(v1, v2)
                    for item in self.selected_items:
                        item.rotate_angle = angle
            elif self.status == 'scale':
                if self.temp_item is not None and len(self.temp_item.p_list) == 2:
                    x0, y0 = self.temp_item.p_list[0]
                    x1, y1 = self.temp_item.p_list[1]
                    ratio = (x-x0) / (x1-x0)
                    for item in self.selected_items:
                        item.scale_ratio = ratio
            elif self.status == 'clip':
                self.temp_item.p_list[1] = [x, y]

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon':
            pass
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'curve':
            pass
        elif self.status == 'select':
            x0, y0 = self.temp_item.p_list[0]
            x1, y1 = self.temp_item.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            self.selection_changed(x, y, w, h)
            self.scene().removeItem(self.temp_item)
            self.finish_select()
        elif self.status == 'rect':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'move':
            self.finish_move()
        elif self.status == 'rotate':
            if len(self.temp_item.p_list) == 2:
                self.scene().removeItem(self.temp_item)
                x0, y0 = self.temp_item.p_list[0]
                for item in self.selected_items:
                    item.p_list = alg.rotate(item.p_list, x0, y0, item.rotate_angle)
                self.finish_rotate()
        elif self.status == 'scale':
            if len(self.temp_item.p_list) == 2:
                self.scene().removeItem(self.temp_item)
                x0, y0 = self.temp_item.p_list[0]
                for item in self.selected_items:
                    item.p_list = alg.scale(item.p_list, x0, y0, item.scale_ratio)
                self.finish_scale()
        elif self.status == 'clip':
            x0, y0 = self.temp_item.p_list[0]
            x1, y1 = self.temp_item.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            for item in self.selected_items:
                if item.item_type == 'line':
                    item.p_list = alg.clip(item.p_list, x, y, x+w, y+h, self.temp_algorithm)
                    if len(item.p_list) < 2:
                        self.scene().removeItem(item)
                        # need to remove from Item List
            self.scene().removeItem(self.temp_item)
            self.finish_clip()

        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)



class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str , paintColor , parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.rotate_angle = 0
        self.rotate_center = []
        self.scale_ratio = 0
        self.scale_center = []
        self.paintColor = paintColor

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            p_list = self.p_list
            if self.rotate_angle != 0:
                p_list = alg.rotate(self.p_list, self.rotate_center[0], self.rotate_center[1], self.rotate_angle)
            if self.scale_ratio != 0:
                p_list = alg.scale(self.p_list, self.scale_center[0], self.scale_center[1], self.scale_ratio)
            item_pixels = alg.draw_line(p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.paintColor)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            p_list = self.p_list
            if self.rotate_angle != 0:
                p_list = alg.rotate(self.p_list, self.rotate_center[0], self.rotate_center[1], self.rotate_angle)
            if self.scale_ratio != 0:
                p_list = alg.scale(self.p_list, self.scale_center[0], self.scale_center[1], self.scale_ratio)
            item_pixels = alg.draw_polygon(p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.paintColor)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            p_list = self.p_list
            if self.scale_ratio != 0:
                p_list = alg.scale(self.p_list, self.scale_center[0], self.scale_center[1], self.scale_ratio)
            item_pixels = alg.draw_ellipse(p_list)
            for p in item_pixels:
                painter.setPen(self.paintColor)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            p_list = self.p_list
            if self.rotate_angle != 0:
                p_list = alg.rotate(self.p_list, self.rotate_center[0], self.rotate_center[1], self.rotate_angle)
            if self.scale_ratio != 0:
                p_list = alg.scale(self.p_list, self.scale_center[0], self.scale_center[1], self.scale_ratio)
            item_pixels = alg.draw_curve(p_list, self.algorithm)
            for p in p_list:
                painter.setPen(self.paintColor)
                painter.drawPoint(*p)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'select':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            painter.setPen(QColor(0, 0, 255))
            painter.drawRects(QRectF(x, y, w, h))
        elif self.item_type == 'rect':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            painter.setPen(self.paintColor)
            painter.drawRects(QRectF(x, y, w, h))
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'rotate':
            painter.drawPoint(*(self.p_list[0]))
        elif self.item_type == 'scale':
            painter.drawPoint(*(self.p_list[0]))
        elif self.item_type == 'clip':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            painter.setPen(QColor(0, 0, 255))
            painter.drawRects(QRectF(x, y, w, h))

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            x = self.p_list[0][0]
            y = self.p_list[0][1]
            w = h = 0
            for p in self.p_list:
                x = min(x, p[0])
                y = min(y, p[1])
            for p in self.p_list:
                w = max(w, p[0] - x)
                h = max(h, p[1] - y)
            return QRectF(x - 1, y - 1, w + 2, h + 2)

        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            x = self.p_list[0][0]
            y = self.p_list[0][1]
            w = h = 0
            for p in self.p_list:
                x = min(x, p[0])
                y = min(y, p[1])
            for p in self.p_list:
                w = max(w, p[0] - x)
                h = max(h, p[1] - y)
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'select':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'rect':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'rotate':
            return QRectF(0, 0, 1, 1)
        elif self.item_type == 'scale':
            return QRectF(0, 0, 1, 1)
        elif self.item_type == 'clip':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)





class cgUI(QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        super(cgUI, self).__init__()
        self.setupUi(self)  # 设置基本UI
        self.update_ui()    # 添加控件
        self.item_cnt = 0

    def update_ui(self) -> None:
        # 更新主界面
        self.set_canvas(600, 600)
        self.setWindowTitle('Painter')

        # 设置菜单

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu('文件')
        file_menu.addAction('设置画笔', self.set_color)

        file_menu.addAction('重置画布', self.reset_canvas)
        file_menu.addAction('保存文件', self.save_file)
        file_menu.addAction('退出', qApp.quit)

        draw_menu = menubar.addMenu('绘制')

        line_menu = draw_menu.addMenu('线段')
        line_menu.addAction('Naive', lambda: self.item_action("line", "Naive"))
        line_menu.addAction('DDA', lambda: self.item_action("line", "DDA"))
        line_menu.addAction("Bresenham", lambda: self.item_action("line", "Bresenham"))
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_menu.addAction('Naive', lambda: self.item_action("polygon", "Naive"))
        polygon_menu.addAction('DDA', lambda: self.item_action("polygon", "DDA"))
        polygon_menu.addAction('Bresenham', lambda: self.item_action("polygon", "Bresenham"))

        ellipse_act = draw_menu.addAction('椭圆')

        curve_menu = draw_menu.addMenu('曲线')
        curve_menu.addAction('Bezier', lambda: self.item_action("curve", "Bezier"))
        curve_menu.addAction('B-spline', lambda: self.item_action("curve", "B-spline"))


        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移', lambda: self.canvas_widget.start_move())
        rotate_act = edit_menu.addAction('旋转', lambda: self.canvas_widget.start_rotate())
        scale_act = edit_menu.addAction('缩放', lambda: self.canvas_widget.start_scale())
        clip_menu = edit_menu.addMenu('裁剪')
        clip_menu.addAction('Cohen-Sutherland', lambda: self.canvas_widget.start_clip("Cohen-Sutherland"))
        clip_menu.addAction("Liang-Barsky", lambda: self.canvas_widget.start_clip("Liang-Barsky"))

        help_menu = menubar.addMenu('帮助')
        help_menu.addAction('关于', self.about)



        # 设置button


        self.line_button.clicked.connect(lambda: self.item_action("line", "DDA"))
        self.polygon_button.clicked.connect(lambda: self.item_action('polygon', "DDA"))
        self.ellipse_button.clicked.connect(lambda: self.item_action("ellipse", "N/A"))
        self.curve_button.clicked.connect(lambda: self.item_action('curve', 'Bezier'))
        self.select_button.clicked.connect(lambda: self.canvas_widget.start_select())
        self.rect_button.clicked.connect(lambda: self.item_action("rect", "N/A"))
        self.cursor_button.clicked.connect(lambda:  self.canvas_widget.cursor_mode())
        self.move_button.clicked.connect(lambda: self.canvas_widget.start_move())
        self.rotate_button.clicked.connect(lambda: self.canvas_widget.start_rotate())
        self.scale_button.clicked.connect(lambda: self.canvas_widget.start_scale())
        self.clip_button.clicked.connect(lambda: self.canvas_widget.start_clip("Cohen-Sutherland"))
        self.color_button.clicked.connect(self.set_color)


        self.cursor_button.setIcon(self.get_icon("./resource/icon/cursor.png"))
        self.line_button.setIcon(self.get_icon("./resource/icon/line.png"))
        self.rect_button.setIcon(self.get_icon("./resource/icon/rect.png"))
        self.polygon_button.setIcon(self.get_icon("./resource/icon/polygon.png"))
        self.ellipse_button.setIcon(self.get_icon("./resource/icon/ellipse.png"))
        self.curve_button.setIcon(self.get_icon("./resource/icon/curve.png"))

        self.select_button.setIcon(self.get_icon("./resource/icon/select.png"))
        self.move_button.setIcon(self.get_icon("./resource/icon/move.png"))
        self.rotate_button.setIcon(self.get_icon("./resource/icon/rotate.png"))
        self.scale_button.setIcon(self.get_icon("./resource/icon/scale.png"))
        self.clip_button.setIcon(self.get_icon("./resource/icon/clip.png"))
        self.color_button.setIcon(self.get_icon("./resource/icon/color.png"))


        return

    def get_id(self, item_type):
        _id = item_type + " " + str(self.item_cnt)
        self.item_cnt += 1
        return _id


    def item_action(self, item_type, algorithm):
        self.canvas_widget.start_draw(item_type, self.get_id((item_type)), algorithm)
        #self.statusBar().showMessage(algorithm + '算法绘制'+ item_type)
        return

    def get_icon(self, path):
        img = QImage(os.path.join(bundle_dir, path))
        pixmap = QPixmap(img)
        fitPixmap = pixmap.scaled(64, 64, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        icon = QIcon(fitPixmap)
        return icon

    def reset_canvas(self):
        text, ok = QInputDialog.getText(self, "重置画布", "设置画布大小(宽，高)", text = '600, 600')
        if ok:
            strs = text.split(',')
            if len(strs) != 2 or not strs[0].strip().isdigit() or not strs[1].strip().isdigit():
                QMessageBox.warning(self, "警告", "格式不正确", QMessageBox.Yes, QMessageBox.Yes)
                return
            w = int(strs[0].strip())
            h = int(strs[1].strip())
            self.horizontalLayout.removeWidget(self.list_widget)
            #self.horizontalLayout.removeWidget(self.canvas_widget)
            sip.delete(self.list_widget)
            sip.delete(self.canvas_widget)
            self.set_canvas(w, h)

    def save_file(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "/", "Images (*.png *.jpg *.bmp)")
        if fileName != '':
            #pixMap = self.canvas_widget.grab(self.canvas_widget.scene().sceneRect().toRect())
            pixMap = self.canvas_widget.grab()
            pixMap.save(fileName)

            #image = self.canvas_widget.scene().toImage()
            #image.save(fileName)

            #image = QImage(QSize(self.canvas_widget.scene().width(), self.canvas_widget.scene().height()), QImage.Format_RGB32)
            #painter = QPainter(image)
            #self.canvas_widget.scene().render(painter);
            #image.save(fileName)


        #print(fileName)

    def set_canvas(self, w, h):
        # 使用QListWidget来记录已有的图元，并用于选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 设置画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, w, h)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(w, h)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget
        self.canvas_widget.setMouseTracking(True)

        #self.horizontalLayout.addWidget(self.canvas_widget)
        #self.Tab.removeTab(1)
        #self.Tab.removeTab(0)
        #self.Tab.addTab(self.canvas_widget, "canvas")

        self.scrollArea.setWidget(self.canvas_widget)

        self.horizontalLayout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')

    def set_color(self):
        col = QColorDialog().getColor(self.canvas_widget.paintColor)
        if col.isValid():
            self.canvas_widget.paintColor = col
        return

    def about(self):
        QMessageBox.about(self, "Painter V1.0", "CopyRight @ 2020 Ricky Ting。")
        return


        

if __name__ == '__main__':

    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))


    app = QApplication(sys.argv)
    ui = cgUI()
    ui.show()
    sys.exit(app.exec_())