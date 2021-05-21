#!encoding:utf-8
import numpy as np


class GoBangGame(object):
    def __init__(self):
        # 棋盘（15x15范围、初始值全为0的二维nparray数组。）
        # 白方落子后，值变为1
        # 黑方落子后，值变为-1
        self.checkerboard = np.zeros((15, 15), int)
        # 游戏是否结束。胜负
        self.GAME_ENDING = 0

    # 获取输入
    def get_qizi(self):
        try:
            print("    请输入x坐标：")
            x1 = int(input())
            print("    请输入y坐标：")
            y1 = int(input())
            if type(x1) == type(y1) == int:
                return x1, y1
        except Exception as e:
            print(e)
            return -1, -1

    # 落子
    # flag: 用来区别黑白方。0表示白方；1表示黑方。
    # x, y：表示落子的坐标位置。
    def luozi(self, flag, x, y):
        if x < 15 and y < 15:
            if self.checkerboard[x][y] == 0:
                try:
                    if flag == 0:
                        print("白方在坐标为({}, {})的位置落了颗白子\n".format(x, y))
                        self.checkerboard[x][y] = 1
                        return True
                    elif flag == 1:
                        print("黑方在坐标为({}, {})的位置落了颗黑子\n".format(x, y))
                        self.checkerboard[x][y] = -1
                        return True
                    else:
                        return False
                        return {"code": -1, "msg": "黑白方身份验证出错！！"}
                except Exception as e:
                    print("落子失败！报错：{}".format(e))
                    return False
            else:
                print("坐标为({}, {})的格子已有棋子".format(x, y))
                return False
                return {"code": -1, "msg": "此格子已有棋子！"}
        else:
            print("坐标({}, {})超出棋盘范围！".format(x, y))
            return False
            return {"code": -1, "msg": "超出棋盘范围！"}

    # 判断四个方向。（主要是构造以落子点为中心、四个方向上、长度为9 的四个数组）
    def four_list(self, chushi_x, chushi_y):
        fangxiang_list = [(1, chushi_y-chushi_x), (-1, chushi_x+chushi_y), (0, chushi_y)]
        four_list = []
        # 前三个方向(分别是左下->右上，左上->右下，左->右)
        for k, b in fangxiang_list:
            list_tmp = []
            for x in range(chushi_x - 4, chushi_x + 5):
                y = k * x + b
                list_tmp.append((x, y))
            four_list.append(list_tmp)
            # print(list_tmp)
        # # 纵向方向的坐标轴，为横向方向坐标轴的x与y互调得到。
        # a = [(y, x) for x, y in list_tmp]
        # 纵向方向应该是这样。（纵向也就是从从下->上）
        list_tmp = []
        for y in range(chushi_y - 4, chushi_y + 5):
            list_tmp.append((chushi_x, y))
        four_list.append(list_tmp)
        # print(a)
        return four_list

    # 判断是否有五子成线。分别对长度为9的列表（也就是每个方向），进行如下5次判断
    # 00000
    #  00000
    #   00000
    #    00000
    #     00000
    def panduan(self, list1):
        for i in range(5):
            count = 0
            for j in range(5):
                x0 = list1[i + j][0]
                y0 = list1[i + j][1]
                # print("x={}, y={}".format(x, y))
                if 0 <= x0 <= 14 and 0 <= y0 <= 14:
                    # print(x, y)
                    count += self.checkerboard[x0][y0]
                else:
                    break
            # print("count=", count)
            # print()
            # if count == 5:
            #     self.GAME_ENDING = 1
            #     print("白方胜利！")
            #     # 后续可以改成return 1 和return 2，来区别白黑方胜利
            #     return 1
            # elif count == -5:
            #     self.GAME_ENDING = 1
            #     print("黑方胜利！")
            #     return 2
            if count == 5 or count == -5:
                self.GAME_ENDING = count
                return True

    def zuizhong(self, flag, x, y):
        # 因为ui传过来的x y范围为[1, 15]，而逻辑层这里的x, y 范围为[0, 14]
        # 所以要-1
        x, y = x-1, y-1
        try:
            if x < 15 and y < 15:
                if self.luozi(flag, x, y):
                    for list_tmp in self.four_list(x, y):
                        # print(list_tmp)
                        if self.panduan(list_tmp):
                            # print(self.checkerboard)
                            print(np.transpose(self.checkerboard))
                            return self.GAME_ENDING
                    return True
                else:
                    print("落子失败，请重新输入！")
            else:
                print("超出棋盘范围，请重新输入！")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 黑方先手。所以flag初始为1
    flag = 1
    w = GoBangGame()
    while w.GAME_ENDING == 0:
        if flag == 1:
            print("黑方落子：")
        elif flag == 0:
            print("白方落子：")
        x, y = w.get_qizi()
        if x > 0 and y > 0:
            w.zuizhong(flag, x, y)
            # flag 1、0交替变换，直到游戏结束
            flag = (flag + 1) % 2
        else:
            print("输入不为数字，请重新输入！")




