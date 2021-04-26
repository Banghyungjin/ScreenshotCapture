import configparser
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CsvConverter(QWidget):

    def config_generator(self):
        # 설정파일 만들기
        config_parser = configparser.ConfigParser()
        self.datetime = QDateTime.currentDateTime()

        # 설정파일 오브젝트 만들기
        config_parser['system'] = {}
        config_parser['system']['title'] = 'csv_converter'
        config_parser['system']['author'] = 'HyungJin Bang'
        config_parser['system']['version'] = '0.0.1'
        config_parser['system']['update'] = self.datetime.toString('yyyy-MM-dd')

        config_parser['directory'] = {}
        config_parser['directory']['directory'] = 'converted_files'


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
            config_parser.set('directory', 'directory', 'converted_files')
            config_parser.write(configfile)
        configfile.close()
        self.storage_label.setText("현재 저장 장소 = " + config_parser['directory']['directory'])
        self.storage_label.repaint()

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

    def convert(self):  # 변환
        converting_directory = QFileDialog.getOpenFileNames(self, "select Directory")
        for file in converting_directory[0]:
            open_file = open(file, 'r')
            out_name = file + '_converted.csv'
            config_parser = configparser.ConfigParser()
            config_parser.read('config.ini', encoding='utf-8')
            path = config_parser['directory']['directory']
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(file, 'rb') as fin:
                first_one = fin.readline()
                print(first_one)
                mark = ','.encode()
                columns = first_one.count(mark) + 1
                readData = fin.readlines()
                for line in readData:
                    print(line)




    def dialog_open(self, column):
        # 버튼 추가
        btnDialog = QPushButton("OK", self.dialog)
        btnDialog.clicked.connect(self.dialog_close)
        dialog_vbox = QVBoxLayout()
        dialog_vbox.addWidget(btnDialog)


        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.setLayout(dialog_vbox)
        self.dialog.show()

    def dialog_close(self):
        self.dialog.close()

    def __init__(self):
        super().__init__()
        if not os.path.isfile('config.ini'):
            self.config_generator()
        self.datetime = QDateTime.currentDateTime()
        self.dialog = QDialog()
        self.init_ui()

    def init_ui(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini', encoding='utf-8')

        self.storage_text = "현재 저장 장소 = " + config_parser['directory']['directory']
        self.storage_label = QLabel(self.storage_text, self)
        # 버튼 생성
        reset_str_btn = QPushButton('저장 장소 초기화')
        reset_str_btn.setToolTip('저장 장소를 초기화 합니다.')
        reset_str_btn.clicked.connect(self.reset_str)  # 버튼이 클릭되면 해당 함수 실행

        save_btn = QPushButton('저장 장소 설정')
        save_btn.setToolTip('csv파일이 저장될 위치를 선택합니다.')
        save_btn.clicked.connect(self.select_directory)  # 버튼이 클릭되면 해당 함수 실행

        open_btn = QPushButton('저장 장소 열기')
        open_btn.setToolTip('csv파일이 저장된 위치를 엽니다.')
        open_btn.clicked.connect(self.open_directory)  # 버튼이 클릭되면 해당 함수 실행

        convert_btn = QPushButton('변환 시작')
        convert_btn.setToolTip('스크린샷 촬영을 시작합니다.')
        convert_btn.clicked.connect(self.convert)  # 버튼이 클릭되면 해당 함수 실행
        # 박스 레이아웃 생성
        box_1 = QHBoxLayout()
        box_1.addStretch(1)
        box_1.addWidget(QLabel('오늘 날짜 : ' + self.datetime.toString('yyyy년 MM월 dd일')))
        box_1.addStretch(1)

        box_4 = QHBoxLayout()
        box_4.addStretch(1)
        box_4.addWidget(self.storage_label)
        box_4.addStretch(1)

        box_5 = QHBoxLayout()
        box_5.addStretch(1)
        box_5.addWidget(QLabel("사용법 = 변환 버튼을 누르면 변환할 파일을 선택하는 창이 열립니다."))
        box_5.addStretch(1)
        # 그리드 레이아웃 생성
        grid = QGridLayout()
        grid.addWidget(save_btn, 0, 0)
        grid.addWidget(open_btn, 0, 1)
        grid.addWidget(reset_str_btn, 0, 2)
        grid.addWidget(convert_btn, 1, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(box_1)
        vbox.addLayout(box_4)
        vbox.addLayout(box_5)
        vbox.addLayout(grid)

        self.setLayout(vbox)
        self.setWindowTitle('Csv_Converter')  # 프로그램 제목 설정
        self.setGeometry(300, 300, 720, 400)  # 창 위치, 크기 설정 (X위치, Y위치, X크기, Y크기)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CsvConverter()
    sys.exit(app.exec_())