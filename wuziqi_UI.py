#!encoding:utf-8
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QBrush, QPen
from PyQt5.QtWidgets import QPlainTextEdit, QToolTip, QMessageBox, QApplication
from wuziqi import GoBangGame


class GoBangUI(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self._pos = []  # 存放棋子坐标的列表
        self.flag = 1  # 表示落子时的棋手身份(黑方白方)
        self._flag = []  # 存放棋手身份的列表
        self.initUI()  # 调用initUI绘制界面
        self.game = GoBangGame()  # 初始化游戏

    # 绘制界面(窗口)
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setObjectName("MainWindow")  # 设置对象名称
        # # 设置窗口的位置和大小
        # self.setGeometry(300, 300, 300, 220)
        self.resize(800, 800)
        self.setWindowTitle('五子棋')  # 设置窗口的标题
        self.setStyleSheet("#MainWindow{background-color:green}")  # 设置背景颜色
        self.show()  # 显示窗口

    # 点击鼠标事件
    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)  # 重写父类
        if e.buttons() == QtCore.Qt.LeftButton:
            # print("点击鼠标左键")
            # 判断点击位置是否在棋盘内
            if 50 <= e.x() <= 750 and 50 <= e.y() <= 750:
                rem_x, rem_y = e.x() % 50, e.y() % 50  # x，y坐标对50取余
                # 判断点击位置是否在落子点的范围内（）
                if 20 < rem_x < 30 or 20 < rem_y < 30:
                    print("此位置不在落子点范围内！")
                else:
                    # xy坐标对50的整除
                    div_x, div_y = e.x() // 50, e.y() // 50
                    # 寻找棋盘上，坐标对应的落子点
                    div_x = div_x+1 if rem_x > 30 else div_x
                    div_y = div_y+1 if rem_y > 30 else div_y
                    # print("坐标为:({}, {})".format(e.x(), e.y()))
                    # print("中心点坐标为:({}, {})".format(div_x*50, div_y*50))
                    # print("落子点为：({}, {})".format(div_x, div_y))
                    # 调用逻辑层代码
                    if self.game.zuizhong(self.flag, div_x, div_y):
                        # 更新身份
                        self._flag.append(self.flag)  # 将flag添加到数组中
                        self._pos.append((div_x, div_y))  # 将落子点(x,y)添加到数组中
                        self.flag = (self.flag+1) % 2  # 更新flag
                        self.viewport().update()  # 更新界面
                        if self.game.GAME_ENDING:
                            # 游戏结束之后的弹窗
                            self.GameOver()
                            return
            else:
                print("此位置在棋盘范围外！")

    # 绘图
    def paintEvent(self, e, radius=30) -> None:
        super().paintEvent(e)  # 重写父类
        qp = QPainter(self.viewport())
        brush_list = [QBrush(Qt.white, Qt.SolidPattern), QBrush(Qt.black, Qt.SolidPattern)]
        pen_list = [QPen(Qt.white, 2, Qt.SolidLine), QPen(Qt.black, 2, Qt.SolidLine)]
        # 绘制棋盘
        self.draw_checkbox(qp)
        # 绘制棋子
        for i in range(len(self._pos)):
            # print(self._pos[i])
            # print(self._flag[i])
            qp.setBrush(brush_list[self._flag[i]])  # 设置棋子的背景色（brush）
            qp.setPen(pen_list[self._flag[i]])  # 设置画笔的颜色
            qp.drawEllipse(self._pos[i][0] * 50 - radius / 2, self._pos[i][1] * 50 - radius / 2, radius, radius)

    # 绘制棋盘
    def draw_checkbox(self, qp):
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for i in range(1, 16):
            x = y = i * 50
            qp.drawLine(x, 50, x, 750)  # 竖线
            qp.drawLine(50, y, 750, y)  # 横线

    # # 游戏结局弹窗信息
    # def GameOver(self, text, parent="游戏结束"):
    #     text = "{}是否再来一局？".format(text)
    #     # QMessageBox.about(self, parent, text)
    #     QMessageBox.information(self, parent, text, QMessageBox.Yes | QMessageBox.No)

    # 游戏结局弹窗信息
    def GameOver(self, title="游戏结束", content="游戏结束,是否再来一局"):
        if self.game.GAME_ENDING == 5:
            title = "白方胜利！"
        elif self.game.GAME_ENDING == -5:
            title = "黑方胜利！"
        print(title)
        choice = QMessageBox.information(self, title, content, QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("==================重新开始游戏!==================\n")
            self.__init__()  # 重新初始化棋盘和数组
        elif choice == QMessageBox.No:
            print("退出游戏。")
            self.close()  # 关闭窗体
            pass


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("图形绘制")
    test = GoBangUI()
    sys.exit(app.exec_())  # 退出pyqt窗口
    # # app.exec_()  # 结束程序，但是窗口还在