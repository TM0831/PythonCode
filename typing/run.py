"""
Version: Python3.7
Author: OniOn
Site: http://www.cnblogs.com/TM0831/
Time: 2019/9/13 21:46
"""
import os
import sys
import time
import random
from PyQt5 import QtWidgets
from typing.ui import Ui_Form
from typing.crawl import crawl_main


class MyForm(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)

        with open("text.txt", "r", encoding="utf-8") as f:
            self.text_list = f.readlines()
        self.text_list = [i.strip() for i in self.text_list]
        self.text = self.text_list[random.randint(0, len(self.text_list))]  # 随机选取一个句子
        self.used_list = [self.text]  # 已经使用过的句子
        self.textBrowser.setText(self.text)  # 设置内容
        self.hide_label()
        self.start_time = time.time()
        # 设置槽函数
        self.submit_btn.clicked.connect(self.click)
        self.next_btn.clicked.connect(self.next)
        # 设置快捷键
        self.submit_btn.setShortcut('ctrl+e')
        self.next_btn.setShortcut('ctrl+n')

    def get_time(self):
        # 计算时间
        end_time = time.time()
        cost_time = "%.2f"%(end_time - self.start_time)
        self.time_label.setText("本次打字花费：{}s".format(cost_time))

    def click(self):
        """
        点击按钮时调用
        :return:
        """
        self.get_time()
        the_input = self.textEdit.toPlainText()
        # 计算准确率
        count = 0
        for i in range(len(the_input)):
            if the_input[i] == self.text[i]:
                count += 1
        accuracy = count / len(self.text) * 100
        # print(accuracy)
        self.show_label()
        # 设置提示信息
        info = "有点可惜，你的正确率是:  %.2f%%  " % accuracy if accuracy != 100 else "恭喜你全对了呢！继续加油哦！"
        self.info_lable.setText(info)

    def next(self):
        while 1:
            text = self.text_list[random.randint(0, len(self.text_list))]
            if text not in self.used_list:
                self.used_list.append(text)
                self.text = text
                self.textBrowser.setText(text)
                self.textEdit.clear()
                self.hide_label()
                self.start_time = time.time()
                break

    def hide_label(self):
        # 将透明度设置为0，达到隐藏且保留位置的目的
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.info_lable.setGraphicsEffect(op)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0)
        self.time_label.setGraphicsEffect(op)

    def show_label(self):
        # 将透明度设置为1，即显示出来
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(1)
        self.info_lable.setGraphicsEffect(op)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(1)
        self.time_label.setGraphicsEffect(op)


if __name__ == '__main__':
    if os.path.exists("text.txt") and os.stat("text.txt").st_size > 0:
        pass
    else:
        crawl_main()
    app = QtWidgets.QApplication(sys.argv)
    my_form = MyForm()
    my_form.show()
    sys.exit(app.exec_())
