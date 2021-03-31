import os
import sys
from PyQt5.QtWidgets import \
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QMainWindow, QAction, \
    QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt, QTime
from win32api import GetSystemMetrics
from PIL import ImageGrab


class ScreenshotCapture(QWidget):
    working_path = 'screenshots'

    def select_directory(self):
        options = QFileDialog.Options()
        options != QFileDialog.ShowDirsOnly

        working_path = QFileDialog.getExistingDirectory(self, "select Directory")

    def open_directory(self):
        os.startfile(self.working_path)

    def capture(self):
        time = QTime.currentTime()
        self.datetime = QDateTime.currentDateTime()
        self.path = 'screenshots/' + self.datetime.toString('yyyy-MM-dd')
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        im = ImageGrab.grab(bbox=(100, 100, 1000, 1000))
        im.save(self.path + '/' + time.toString('hh시 mm분 ss초 zzz') + '.png')



    def __init__(self):
        super().__init__()
        self.datetime = QDateTime.currentDateTime()
        self.init_ui()

    def init_ui(self):
        now_version = 0.0                                   # 버전
        var = .1

        working_path = 'screenshots'

        save_btn = QPushButton('저장 장소 설정')
        save_btn.setToolTip('스크린샷이 저장될 위치를 선택합니다.\n현재 경로는 ' + os.path.abspath(self.working_path) + '입니다')
        save_btn.clicked.connect(self.select_directory) # 버튼이 클릭되면 해당 함수 실행

        open_btn = QPushButton('저장 장소 열기')
        open_btn.setToolTip('스크린샷이 저장된 위치를 엽니다.\n현재 경로는' + os.path.abspath(self.working_path) + '입니다')
        open_btn.clicked.connect(self.open_directory)  # 버튼이 클릭되면 해당 함수 실행

        set_btn = QPushButton('스크린샷 범위 설정')
        set_btn.setToolTip('스크린샷의 범위를 설정합니다')

        capture_btn = QPushButton('스크린샷 촬영 (Ctrl + 키패드 5)')
        capture_btn.setToolTip('스크린샷을 저장합니다.')
        capture_btn.setShortcut("Ctrl+5")
        capture_btn.clicked.connect(self.capture)  # 버튼이 클릭되면 해당 함수 실행

        box_1 = QHBoxLayout()
        box_1.addStretch(1)
        box_1.addWidget(QLabel('오늘 날짜 : ' + self.datetime.toString('yyyy.MM.dd')))
        box_1.addStretch(1)

        box_2 = QHBoxLayout()
        box_2.addStretch(1)
        box_2.addWidget(QLabel('현재 화면 크기(픽셀) : 가로 X 세로 : ' + str(GetSystemMetrics(0)) + ' X ' + str(GetSystemMetrics(1))))  # 현재 화면 크기 출력
        box_2.addStretch(1)

        grid = QGridLayout()
        grid.addWidget(save_btn, 0, 0)
        grid.addWidget(open_btn, 0, 1)
        grid.addWidget(set_btn, 1, 0)
        grid.addWidget(capture_btn, 1, 1)

#        box_3 = QHBoxLayout()
#        box_3.addStretch(1)
#        box_3.addWidget(set_btn)
#        box_3.addStretch(1)
#        box_3.addWidget(capture_btn)
#        box_3.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(box_1)
        vbox.addLayout(box_2)
        vbox.addLayout(grid)
        self.setLayout(vbox)


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
