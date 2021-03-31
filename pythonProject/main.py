"""
made by HyungJin Bang
"""

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, QTime
from win32api import GetSystemMetrics
from PIL import ImageGrab
import configparser


class ScreenshotCapture(QWidget):

    def config_generator(self):
        # 설정파일 만들기
        config_parser = configparser.ConfigParser()
        self.datetime = QDateTime.currentDateTime()

        # 설정파일 오브젝트 만들기
        config_parser['system'] = {}
        config_parser['system']['title'] = 'ScreenshotCapture'
        config_parser['system']['author'] = 'HyungJin Bang'
        config_parser['system']['version'] = '0.0.1'
        config_parser['system']['update'] = self.datetime.toString('yyyy-MM-dd')

        config_parser['directory'] = {}
        config_parser['directory']['directory'] = 'screenshots'

        config_parser['shortcuts'] = {}
        config_parser['shortcuts']['take_shot'] = 'Ctrl + 5'

        config_parser['screensize'] = {}
        config_parser['screensize']['axisX1'] = '0'
        config_parser['screensize']['axisY1'] = '0'
        config_parser['screensize']['axisX2'] = str(GetSystemMetrics(0))
        config_parser['screensize']['axisY2'] = str(GetSystemMetrics(1))

        # 설정파일 저장
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.write(configfile)

    def reset_str(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', 'screenshots')
            config_parser.write(configfile)

    def reset_cov(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('screensize', 'axisX1', '0')
            config_parser.set('screensize', 'axisY1', '0')
            config_parser.set('screensize', 'axisX2', str(GetSystemMetrics(0)))
            config_parser.set('screensize', 'axisY2', str(GetSystemMetrics(1)))
            config_parser.write(configfile)

    def select_directory(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', QFileDialog.getExistingDirectory(self, "select Directory"))
            config_parser.write(configfile)

    def open_directory(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        os.startfile(config_parser['directory']['directory'])

    def capture(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        time = QTime.currentTime()
        self.datetime = QDateTime.currentDateTime()
        path = config_parser['directory']['directory'] + '/' + self.datetime.toString('yyyy-MM-dd')
        if not os.path.isdir(path):
            os.mkdir(path)
        x1 = config_parser['screensize']['axisX1']
        y1 = config_parser['screensize']['axisY1']
        x2 = config_parser['screensize']['axisX2']
        y2 = config_parser['screensize']['axisY2']
        im = ImageGrab.grab(bbox=(int(x1), int(y1), int(x2), int(y2)))
        im.save(path + '/' + time.toString('hh시 mm분 ss초 zzz') + '.png')

    def set_screenshot_size(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')

    def mousePressEvent(self, event):
        txt = "Mouse 위치 = {0}, {1}".format(event.x(), event.y())
        self.mouseLabel.setText(txt)


    def __init__(self):
        super().__init__()
        if not os.path.isfile('config.ini'):
            self.config_generator()
        self.datetime = QDateTime.currentDateTime()
        self.init_ui()

    def init_ui(self):
        self.text = "Mouse 위치 = 0, 0"
        self.setMouseTracking(True)
        self.mouseLabel = QLabel(self.text, self)
        reset_str_btn = QPushButton('저장 장소 초기화')
        reset_str_btn.setToolTip('저장 장소를 초기화 합니다.')
        reset_str_btn.clicked.connect(self.reset_str)  # 버튼이 클릭되면 해당 함수 실행

        save_btn = QPushButton('저장 장소 설정')
        save_btn.setToolTip('스크린샷이 저장될 위치를 선택합니다.')
        save_btn.clicked.connect(self.select_directory)  # 버튼이 클릭되면 해당 함수 실행

        open_btn = QPushButton('저장 장소 열기')
        open_btn.setToolTip('스크린샷이 저장된 위치를 엽니다.')
        open_btn.clicked.connect(self.open_directory)  # 버튼이 클릭되면 해당 함수 실행

        set_btn = QPushButton('촬영 범위 설정')
        set_btn.setToolTip('스크린샷 촬영 범위를 설정합니다')
        set_btn.clicked.connect(self.mouseMoveEvent)  # 버튼이 클릭되면 해당 함수 실행

        reset_cov_btn = QPushButton('촬영 범위 초기화')
        reset_cov_btn.setToolTip('스크린샷 촬영 범위를 전체 화면 촬영으로 초기화 합니다.')
        reset_cov_btn.clicked.connect(self.reset_str)  # 버튼이 클릭되면 해당 함수 실행

        capture_btn = QPushButton('스크린샷 촬영 (Ctrl + 키패드 5)')
        capture_btn.setToolTip('스크린샷을 저장합니다.')
        capture_btn.setShortcut("Ctrl+5")
        capture_btn.clicked.connect(self.capture)  # 버튼이 클릭되면 해당 함수 실행

        box_1 = QHBoxLayout()
        box_1.addStretch(1)
        box_1.addWidget(QLabel('오늘 날짜 : ' + self.datetime.toString('yyyy년 MM월 dd일')))
        box_1.addStretch(1)

        box_2 = QHBoxLayout()
        box_2.addStretch(1)
        box_2.addWidget(QLabel('현재 화면 크기(픽셀) : 가로 X 세로 : ' + str(GetSystemMetrics(0)) + ' X ' + str(GetSystemMetrics(1))))  # 현재 화면 크기 출력
        box_2.addStretch(1)

        box_3 = QHBoxLayout()
        box_3.addStretch(1)
        box_3.addWidget(self.mouseLabel)
        box_3.addStretch(1)

        grid = QGridLayout()
        grid.addWidget(save_btn, 0, 0)
        grid.addWidget(open_btn, 0, 1)
        grid.addWidget(reset_str_btn, 0, 2)
        grid.addWidget(set_btn, 1, 0)
        grid.addWidget(capture_btn, 1, 1)
        grid.addWidget(reset_cov_btn, 1, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(box_1)
        vbox.addLayout(box_2)
        vbox.addLayout(box_3)
        vbox.addLayout(grid)

        opacity_effect = QGraphicsOpacityEffect(self.mouseLabel)
        opacity_effect.setOpacity(0.5)
        self.mouseLabel.setGraphicsEffect(opacity_effect)

        self.setLayout(vbox)

        # self.statusBar().showMessage(self.datetime.toString('yyyy.MM.dd, hh:mm:ss'))

        self.setWindowTitle('스크린샷 캡쳐 by BangHyungJin')  # 프로그램 제목 설정
        self.setWindowIcon(QIcon('screenshot_icon.png'))    # 프로그램 아이콘 설정 (아이콘은 프로젝트 폴더에 위치)
        self.setGeometry(300, 300, 720, 405)               # 창 위치, 크기 설정 (X위치, Y위치, X크기, Y크기)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotCapture()
    sys.exit(app.exec_())
