import ftplib
import sys

import os

import time
import xlsxwriter
from PyQt5 import QtCore
import glob

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QCheckBox
import threading

from Miscs import ClickableLabel, FolderIcon, FileTransferIcon, FtpIcon, ProceedIcon, OkIcon
from rwIni import RWIni


class Program(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ini = RWIni()

        self.src_txt = QLabel('Source', self)
        self.src_txt.setStyleSheet('color: white; background-color: transparent; font-size: 18px')
        self.src_txt.resize(60, 40)
        self.src_txt.move(80, 50)

        self.src_box = QLineEdit(self)
        self.src_box.setStyleSheet('background-color: white;'
                           'border-width: 2px;'
                           'border-color: #9C9C9C;'
                           'border-style: inset;')
        self.src_box.resize(400, 40)
        self.src_box.move(150, 50)

        self.src_select = FolderIcon(self)
        self.src_select.resize(40, 40)
        self.src_select.move(580, 50)
        self.src_select.clicked.connect(self.get_src)

        # self.ftp_txt = QLabel('FTP', self)
        # self.ftp_txt.setStyleSheet('color: white; background-color: transparent; font-size: 18px')
        # self.ftp_txt.resize(60, 40)
        # self.ftp_txt.move(80, 100)
        #
        # self.ftp_box = QLineEdit(self)
        # self.ftp_box.setStyleSheet('background-color: white;'
        #                            'border-width: 2px;'
        #                            'border-color: #9C9C9C;'
        #                            'border-style: inset;')
        # self.ftp_box.resize(400, 40)
        # self.ftp_box.move(150, 100)
        # self.ftp_box.setText(
        #     self.ini.readIni('FTP', 'Path')
        # )
        # self.ftp_box.editingFinished.connect(self.update_ftp)

        self.dest_txt = QLabel('Destination', self)
        self.dest_txt.setStyleSheet('color: white; background-color: transparent; font-size: 18px')
        self.dest_txt.resize(100, 40)
        self.dest_txt.move(40, 150)

        self.dest_box = QLineEdit(self)
        self.dest_box.setStyleSheet('background-color: white;'
                                   'border-width: 2px;'
                                   'border-color: #9C9C9C;'
                                   'border-style: inset;')
        self.dest_box.resize(400, 40)
        self.dest_box.move(150, 150)

        self.dest_select = FolderIcon(self)
        self.dest_select.resize(40, 40)
        self.dest_select.move(580, 150)
        self.dest_select.clicked.connect(self.get_dest)


        self.file_proceed = FileTransferIcon(self)
        self.file_proceed.resize(80, 80)
        self.file_proceed.move(600, 400)
        self.file_proceed.clicked.connect(self.file_process_pressed)

        self.ftp_proceed = FtpIcon(self)
        self.ftp_proceed.resize(80, 80)
        self.ftp_proceed.move(600, 500)
        self.ftp_proceed.clicked.connect(self.process_ftp)
        # self.ftp_proceed.hide()

        self.delete_box = QCheckBox('Delete source files after processing', self)
        self.delete_box.setStyleSheet('QCheckBox::indicator {width: 20px; height: 20px}'
                                      'QCheckBox{color: white; background-color: transparent; font-size: 20px; spacing: 50px}')
        # self.delete_box.setStyleSheet('QCheckBox::indicator {width: 40px; height: 40px}')
        self.delete_box.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.delete_box.resize(400, 20)
        self.delete_box.move(150, 220)
        self.delete_box.setChecked(True)

        self.proceed = OkIcon(self)
        self.proceed.resize(150, 150)
        self.proceed.move(280, 300)
        self.proceed.hide()

        # self.status = QLabel('', self)
        # self.status.setStyleSheet('color: white; background-color: transparent; font-size: 16px')
        # self.status.resize(500, 30)
        # self.status.move(20, 550)

        self.timer = QTimer(self)



        self.setStyleSheet('QMainWindow {background-color: #012B74}')
        self.setWindowTitle('Curve Extractor')
        self.setWindowIcon(QIcon('img\\Curve.ico'))
        self.show()
        self.resize(700, 600)
        self.move(200, 200)


    def process_ftp(self):
        dest = self.dest_box.text()
        if dest == '':
            QMessageBox.warning(self, 'Warning', 'Select destination path!')
            self.proceed.hide()
            return
        user = self.ini.readIni('FTP', 'User')
        if user == '':
            QMessageBox.warning(self, 'Warning', 'No ftp settings in configuration file!')
            self.proceed.hide()
            return
        pwd = self.ini.readIni('FTP', 'Password')
        if pwd == '':
            QMessageBox.warning(self, 'Warning', 'No ftp settings in configuration file!')
            self.proceed.hide()
            return
        adr = self.ini.readIni('FTP', 'IP')
        if adr == '':
            QMessageBox.warning(self, 'Warning', 'No ftp settings in configuration file!')
            self.proceed.hide()
            return
        src = self.ini.readIni('FTP', 'Path')
        if src == '':
            QMessageBox.warning(self, 'Warning', 'No ftp settings in configuration file!')
            self.proceed.hide()
            return
        try:
            conection = ftplib.FTP(adr)
            conection.login(user, pwd)

            conection.cwd(src)
        except:
            QMessageBox.warning(self, 'Warning', 'Unable to connect to ftp server!')
            self.proceed.hide()
            return
        try:
            data = conection.nlst()
        except:
            QMessageBox.warning(self, 'Warning', 'No such directory on FTP server!')
            self.proceed.hide()
            return
        if len(data) == 0:
            self.proceed.hide()
            return

        for rec in data:
            try:
                conection.retrbinary('RETR ' + rec, open(rec, 'wb').write)
                self.generate_curve(rec, dest)
                os.remove(rec)
            except:
                pass
            # Delete File
            if self.delete_box.isChecked():
                conection.delete(rec)

        self.proceed.setOk(True)

    def update_ftp(self):
        value = self.ftp_box.text()
        self.ini.writeIni('FTP', 'Path', value)

    def get_src(self):
        self.src_box.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))

    def get_dest(self):
        self.dest_box.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))

    def generate_curve(self, f, dest):
        file = open(f)
        content = file.read()
        # Extract Data
        data = content.split('[Point];[Position];[Force]\n', 1)
        if len(data) <= 1:
            return
        data = data[1]
        data = data.split('\n')
        value_x = []
        value_y = []
        # Fill Data
        for rec in data:
            local = rec.split(';')
            if len(local) == 3:
                value_x.append(float(local[1]))
                value_y.append(float(local[2]))

        # Create Excel file
        file_only = f.split('\\')#[1]
        if len(file_only) > 1:
            file_only = file_only[1]
        else:
            file_only = file_only[0]

        fname = dest + '\\' + file_only.split('.log')[0] + '.xlsx'
        workbook = xlsxwriter.Workbook(fname)
        chart_1 = workbook.add_chart({'type': 'line'})
        curve_worksheet = workbook.add_worksheet('Curve')
        data_worksheet = workbook.add_worksheet('Data')

        # Write Data To Excel
        data_worksheet.write_column('A1', value_x)
        data_worksheet.write_column('B1', value_y)

        # Generate Curve
        chart_1.set_x_axis({
            'name': 'Position',
            'name_font': {'size': 18, 'bold': True}
        })

        chart_1.set_y_axis({
            'name': 'Force',
            'name_font': {'size': 18, 'bold': True}
        })
        chart_1.set_legend({
            'none': True
        })

        chart_1.add_series({
            'values': '=Data!$B$1:$B$198',
            'categories': '=Data!$A$1:$A$198'
        })

        curve_worksheet.insert_chart('D2', chart_1, {'x_scale': 2, 'y_scale': 2})

        # Close Excel
        workbook.close()
        # Close File
        file.close()

    def file_process_pressed(self):
        if self.src_box.text() != '' and self.dest_box.text() != '':
            self.proceed.setOk(False)
            self.proceed.show()
        self.timer.singleShot(1000, self.process_files)

    def ftp_process_pressed(self):
        if self.src_box.text() != '':
            self.proceed.setOk(False)
            self.proceed.show()
        self.timer.singleShot(1000, self.process_ftp)

    def process_files(self):
        src = self.src_box.text()
        if src == '':
            QMessageBox.warning(self, 'Warning', 'Select source path!')
            return
        dest = self.dest_box.text()
        if dest == '':
            QMessageBox.warning(self, 'Warning', 'Select destination path!')
            return



        src += '\\*.log'
        files = glob.glob(src)

        for path in files:
            self.generate_curve(path, dest)

            # Delete File
            if self.delete_box.isChecked():
                os.remove(path)

        # Show Ok Icon
        self.proceed.setOk(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    sys.exit(app.exec_())