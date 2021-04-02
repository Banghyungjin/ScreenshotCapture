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
import mouse as MS
import keyboard as KB


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
        config_parser['shortcuts']['take_shot'] = 'Ctrl + Alt'

        config_parser['screensize'] = {}
        config_parser['screensize']['axisX1'] = '0'
        config_parser['screensize']['axisY1'] = '0'
        config_parser['screensize']['axisX2'] = str(GetSystemMetrics(0))
        config_parser['screensize']['axisY2'] = str(GetSystemMetrics(1))

        # 설정파일 저장
        with open('config.ini', 'w', encoding='utf-8') as configfile:   # 스크린샷 저장 폴더가 없을 경우 만듬
            config_parser.write(configfile)
        configfile.close()
        path = config_parser['directory']['directory']
        if not os.path.isdir(path):
            os.mkdir(path)

    def reset_str(self):  # 저장 공간 리셋
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', 'screenshots')
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()

    def reset_cov(self):  # 촬영 범위 리셋
        self.cover_label.setText(
            "현재 촬영할 범위(픽셀) = (0, 0) (" + str(GetSystemMetrics(0)) + ", " + str(GetSystemMetrics(1)) + ")")
        self.cover_label.repaint()
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('screensize', 'axisX1', '0')
            config_parser.set('screensize', 'axisY1', '0')
            config_parser.set('screensize', 'axisX2', str(GetSystemMetrics(0)))
            config_parser.set('screensize', 'axisY2', str(GetSystemMetrics(1)))
            config_parser.write(configfile)
        configfile.close()

    def select_directory(self):  # 저장 공간 설정
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('directory', 'directory', QFileDialog.getExistingDirectory(self, "select Directory"))
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()

    def open_directory(self):   # 저장 공간 열기
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        path = config_parser['directory']['directory']
        if not os.path.isdir(path):
            os.mkdir(path)
        os.startfile(config_parser['directory']['directory'])

    def capture(self):  # 촬영
        counter = 1
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        path = config_parser['directory']['directory'] + '/' + self.datetime.toString('yyyy-MM-dd')
        if not os.path.isdir(path):
            os.mkdir(path)
        while 1:
            if KB.is_pressed(config_parser['shortcuts']['take_shot']) and counter:
                time = QTime.currentTime()
                x1 = config_parser['screensize']['axisX1']
                y1 = config_parser['screensize']['axisY1']
                x2 = config_parser['screensize']['axisX2']
                y2 = config_parser['screensize']['axisY2']
                im = ImageGrab.grab(bbox=(int(x1), int(y1), int(x2), int(y2)))
                im.save(path + '/' + time.toString('hh시 mm분 ss초 zzz') + '.png')
                counter = 0
            if not KB.is_pressed("ctrl") or not KB.is_pressed("alt"):
                counter = 1
            if KB.is_pressed("e"): break

    def get_mouse(self):    # 마우스 위치 받아오기
        self.cover_label.setText("촬영할 범위의 왼쪽 위를 클릭하세요")
        self.cover_label.repaint()
        while 1:
            if MS.is_pressed():
                left_upper = MS.get_position()
                break
        while MS.is_pressed():
            if not MS.is_pressed():
                break
        self.cover_label.setText("촬영할 범위의 오른쪽 아래를 클릭하세요")
        self.cover_label.repaint()
        while 1:
            if MS.is_pressed():
                right_lower = MS.get_position()
                break
        self.cover_label.setText("현재 촬영할 범위(픽셀) = " + str(left_upper) + " " + str(right_lower))
        self.cover_label.repaint()
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config_parser.set('screensize', 'axisX1', str(left_upper[0]))
            config_parser.set('screensize', 'axisY1', str(left_upper[1]))
            config_parser.set('screensize', 'axisX2', str(right_lower[0]))
            config_parser.set('screensize', 'axisY2', str(right_lower[1]))
            config_parser.write(configfile)
        configfile.close()

    def __init__(self):
        super().__init__()
        if not os.path.isfile('config.ini'):
            self.config_generator()
        self.datetime = QDateTime.currentDateTime()
        self.init_ui()

    def init_ui(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')

        self.cover_text = "현재 촬영할 범위(픽셀) = (" + config_parser['screensize']['axisX1'] + ", " \
                          + config_parser['screensize']['axisY1'] + ") (" + config_parser['screensize']['axisX2'] \
                          + ", " + config_parser['screensize']['axisY2'] + ")"
        self.cover_label = QLabel(self.cover_text, self)

        self.storage_text = "현재 저장 장소 = " + config_parser['directory']['directory']
        self.storage_label = QLabel(self.storage_text, self)
        # 버튼 생성
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
        set_btn.clicked.connect(self.get_mouse)  # 버튼이 클릭되면 해당 함수 실행

        reset_cov_btn = QPushButton('촬영 범위 초기화')
        reset_cov_btn.setToolTip('스크린샷 촬영 범위를 전체 화면 촬영으로 초기화 합니다.')
        reset_cov_btn.clicked.connect(self.reset_cov)  # 버튼이 클릭되면 해당 함수 실행

        capture_btn = QPushButton('촬영 시작 = Q,  종료 = E')
        capture_btn.setToolTip('스크린샷 촬영을 시작합니다.')
        capture_btn.setShortcut("q")
        capture_btn.clicked.connect(self.capture)  # 버튼이 클릭되면 해당 함수 실행
        # 박스 레이아웃 생성
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
        box_3.addWidget(self.cover_label)
        box_3.addStretch(1)

        box_4 = QHBoxLayout()
        box_4.addStretch(1)
        box_4.addWidget(self.storage_label)
        box_4.addStretch(1)

        box_5 = QHBoxLayout()
        box_5.addStretch(1)
        box_5.addWidget(QLabel("사용법 = 촬영 시작 버튼을 누른 뒤 Ctrl + Alt를 누를 때 마다 스크린샷이 저장됩니다.\n" \
                               + "스크린샷을 필요한 만큼 촬영한 뒤에는 E를 눌러 촬영을 종료합니다."))
        box_5.addStretch(1)
        # 그리드 레이아웃 생성
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
        vbox.addLayout(box_4)
        vbox.addLayout(box_3)
        vbox.addLayout(box_5)
        vbox.addLayout(grid)

        self.setLayout(vbox)
        self.setWindowTitle('스크린샷 캡쳐 by BangHyungJin')  # 프로그램 제목 설정
        self.setWindowIcon(QIcon('screenshot_icon.png'))  # 프로그램 아이콘 설정 (아이콘은 프로젝트 폴더에 위치)
        self.setGeometry(300, 300, 720, 400)  # 창 위치, 크기 설정 (X위치, Y위치, X크기, Y크기)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotCapture()
    sys.exit(app.exec_())
