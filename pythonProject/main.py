import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime
from win32api import GetSystemMetrics


class ScreenshotCapture(QWidget):

    def __init__(self):
        super().__init__()
        self.datetime = QDateTime.currentDateTime()
        self.init_ui()

    def init_ui(self):
        now_version = 0.0                                   # 버전
        var = .1
        #self.statusBar().showMessage('now version = ' + str(now_version) + '' + str(var))
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('현재 화면 크기 : '), 0, 0)
        grid.addWidget(QLabel('가로 - ' + str(GetSystemMetrics(0)) + ' 세로 - ' + str(GetSystemMetrics(1))), 0, 1)
        grid.addWidget(QLabel('Author:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)

        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QTextEdit(), 2, 1)


        # self.statusBar().showMessage(self.datetime.toString('yyyy.MM.dd, hh:mm:ss'))

        self.setWindowTitle('스크린샷 캡쳐 by BangHyungJin')  # 프로그램 제목 설정
        self.setWindowIcon(QIcon('screenshot_icon.png'))    # 프로그램 아이콘 설정 (아이콘은 프로젝트 폴더에 위치)
        self.setGeometry(300, 300, 720, 405)               # 창 위치, 크기 설정 (X위치, Y위치, X크기, Y크기)
        self.setFullscreen = QAction("&Fullscreen", self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotCapture()
    sys.exit(app.exec_())
