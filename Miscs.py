import time
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon

class EngMode(QLabel):
    text = ''
    def __init__(self, widget):
        super().__init__('', widget)
        self.setStyleSheet('background-color: #F2A408; font-size: 20px; border: 3px outset #9C9C9C;')
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.blink)
        self.setLanguage(0)
        self.blinked = False

    #Engineering Mode
    def setLanguage(self, idx):
        if idx == 0:
            EngMode.text = 'Инженерен Режим'
        elif idx == 1:
            EngMode.text = 'Engineering Mode'

    def blink(self):
        self.setText('') if self.blinked else self.setText(EngMode.text)
        self.blinked = not self.blinked

    def setOn(self):
        self.show()
        self.timer.start(1000)

    def setOff(self):
        self.hide()
        self.timer.stop()

class PLCState(QLabel):
    def __init__(self, widget):
        super().__init__(widget)
        self.setStyleSheet('background-color: #BFCDDB; font-size: 20px; border: 3px outset #9C9C9C;')
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def setState(self, state, lang):
        if lang == 0:
            if state == 0:
                self.setText('Машината не Работи')
            elif state == 1:
                self.setText('Машината се Инциализира')
            elif state == 2:
                self.setText('Машината е в Готовност')
            elif state == 3:
                self.setText('Машината е в Работен Режим')
            elif state == 4:
                self.setText('Машината е в Пауза')
            elif state == 5:
                self.setText('Машината е Спряла')
        elif lang == 1:
            if state == 0:
                self.setText('The Machine is Idle')
            elif state == 1:
                self.setText('The Machine is Initializing')
            elif state == 2:
                self.setText('The Machine is Ready')
            elif state == 3:
                self.setText('The Machine Works')
            elif state == 4:
                self.setText('The Machine is Paused')
            elif state == 5:
                self.setText('The Machine is Halted')

class CmdStatus(QLabel):
    def __init__(self, widget):
        super().__init__(widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setStyleSheet('background-color: transparent; font-size: 16px; border: 3px inset #9C9C9C;')

    def setStatus(self, busy):
        if busy:
            self.setText('Busy')
            self.setStyleSheet('background-color: #D40000; font-size: 16px; border: 3px inset #9C9C9C;')
        else:
            self.setText('Done')
            self.setStyleSheet('background-color: #00B200; font-size: 16px; border: 3px inset #9C9C9C;')

class MachineError(QLabel):
    def __init__(self, widget):
        super().__init__(widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setStyleSheet('background-color: #BFCDDB; border: 3px outset #9C9C9C;')

        self.text_area = QLabel('', self)
        self.text_area.setStyleSheet('background-color:transparent; font-size: 14px;border: none')
        self.text_area.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.icon = QLabel('', self)
        self.icon.setStyleSheet('background-color:transparent; font-size: 16px;border: none')
        self.icon.setPixmap(QPixmap('img\\error.png'))
        self.icon.setScaledContents(True)
        self.icon.hide()

    def setText(self, str):
        self.text_area.setText(str)
        if len(str) > 0:
            self.icon.show()
        else:
            self.icon.hide()

    def setResize(self):
        self.text_area.resize(self.width() * 0.72, self.height() * 0.9)
        self.text_area.move(self.width() * 0.01, self.height() * 0.05)

        self.icon.resize(self.width() * 0.25, self.height() * 0.9)
        self.icon.move(self.width() * 0.72, self.height() * 0.05)



class GoldenSample(QLabel):
    def __init__(self, widget):
        super().__init__(widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.setStyleSheet('background-color: #F2A408; font-size: 16px; border: 3px outset #9C9C9C;')

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self,name, widget):
        super().__init__(name, widget)
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

class ClickableIcon(ClickableLabel):
    def __init__(self,path, widget, name = ''):
        super().__init__(name, widget)
        self.setPixmap(QPixmap(path))
        self.setStyleSheet('background-color: transparent')
        self.setScaledContents(True)

class LanguageIcon(ClickableLabel):
    #clicked = pyqtSignal()
    def __init__(self, widget,  name=''):
        super().__init__(name, widget)
        self.bg = QPixmap('img\\bg.png')
        self.gb = QPixmap('img\\gb.png')
        self.setPixmap(self.gb)
        self.lang = 0   # 0 == BG; 1 == EN

    def change(self):
        if self.lang == 0:
            self.setPixmap(self.bg)
            self.lang = 1
        elif self.lang == 1:
            self.setPixmap(self.gb)
            self.lang = 0

class GoodParts(ClickableLabel):
    def __init__(self, name, widget):
        super().__init__(name, widget)
        self.setStyleSheet('background-color: #BFCDDB; font-size: 12px; font-weight:bold; border: 3px outset #9C9C9C;')
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def updatePart(self, qty, lang):
        if lang == 0:
            self.setText('Годни: {}'.format(qty))
        else:
            self.setText('Good Parts: {}'.format(qty))

class BadParts(ClickableLabel):
    def __init__(self,name, widget):
        super().__init__(name, widget)
        self.setStyleSheet('background-color: #BFCDDB; font: 12px; font-weight:bold; border: 3px outset #9C9C9C; color: red')
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def updatePart(self, qty, lang):
        if lang == 0:
            self.setText('Негодни: {}'.format(qty))
        else:
            self.setText('Bad Parts: {}'.format(qty))

class AlertBox(QMessageBox):
    def __init__(self, title, msg):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(msg)
        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(QMessageBox.Warning)
        self.setModal(False)
        self.setWindowIcon(QIcon('img\\logo.png'))
        self.exec_()

class Nest(QLabel):
    def __init__(self, widget, txt):
        super().__init__(txt, widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def setStatus(self, idx):
        if idx == 0:
            self.setStyleSheet('background-color: #FFFFFF; font-size: 20px')
        elif idx == 1:
            self.setStyleSheet('background-color: #4366ff; font-size: 20px')
        elif idx == 2:
            self.setStyleSheet('background-color: #00B200; font-size: 20px')
        elif idx == 3:
            self.setStyleSheet('background-color: #D40000; font-size: 20px')
        elif idx == 4:
            self.setStyleSheet('background-color: #BFCDDB; font-size: 20px')
        elif idx == 5:
            self.setStyleSheet('background-color: #F2A408; font-size: 20px')

class BoxInfo(ClickableLabel):
    def __init__(self, widget):
        super().__init__('', widget)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)


    def set_box(self, bool):
        if bool:
            self.setStyleSheet('background-color: #00CC00;font-size: 20px; border: 3px outset #9C9C9C;')
        else:
            self.setStyleSheet('background-color: #FF0000;font-size: 20px; border: 3px outset #9C9C9C;')

    def setLanguage(self, idx):
        if idx == 0:
            self.setText('Регистриран Кашон')
        elif idx == 1:
            self.setText('Registered Box')

class RotatorIcon(QLabel):
    def __init__(self, widget, name = ''):
        super().__init__(name, widget)
        self.left = 'img\\left_ferrule.png'
        self.load_1 = 'img\\load_1.png'
        self.load_2 = 'img\\load_2.png'
        self.load_tail = 'img\\load_tail.png'
        self.right_1 = 'img\\right_1.png'
        self.right_2 = 'img\\right_2.png'
        self.setPixmap(QPixmap(self.left))
        self.setStyleSheet('background-color: transparent')
        self.setScaledContents(True)
    def setPosition(self, pp, pt, pos, rotator):
        if not pp: #Not part present
            self.hide()
            return
        if rotator == 1: #Rotator left
            self.setPixmap(QPixmap(self.left))
            self.show()
        elif rotator == 2: # Rotator in load position
            if pos == 1: #Pointed down
                if pt == 1: # V type
                    self.setPixmap(QPixmap(self.load_1))
                    self.show()
                    return
                elif pt == 2: # U type
                    self.setPixmap(QPixmap(self.load_2))
                    self.show()
            elif pos == 2: # Pointed Up
                self.setPixmap(QPixmap(self.load_tail))
                self.show()
        elif rotator == 3: # Rotator right
            if pt == 1: # V Type
                self.setPixmap(QPixmap(self.right_1))
                self.show()
            elif pt == 2: # U Type
                self.setPixmap(QPixmap(self.right_2))
                self.show()

class PressIcon(QLabel):
    def __init__(self, widget, name=''):
        super().__init__(name, widget)
        self.setPixmap(QPixmap('img\\pressfit.png'))
        self.setStyleSheet('background-color: transparent')
        self.setScaledContents(True)

class AssemblyIcon(QLabel):
    def __init__(self, widget, name=''):
        super().__init__(name, widget)
        self.setPixmap(QPixmap('img\\assembly.png'))
        self.setStyleSheet('background-color: transparent')
        self.setScaledContents(True)

class OkIcon(QLabel):
    def __init__(self, widget, name=''):
        super().__init__(name, widget)
        self.setPixmap(QPixmap('img\\ok.png'))
        self.setStyleSheet('background-color: transparent')
        self.setScaledContents(True)
    def setOk(self, bool):
        if bool:
            self.setPixmap(QPixmap('img\\ok.png'))
        else:
            self.setPixmap(QPixmap('img\\processing.png'))

class RmNest(QLabel):
    def __init__(self, widget):
        super().__init__('', widget)
        self.setStatus(True)

    def setStatus(self, bool):
        if bool:
            self.setStyleSheet('background-color:#00CC00; border: 3px inset grey;')
        else:
            self.setStyleSheet('background-color:#bfcddb; border: 3px inset grey;')

class FileTransferIcon(ClickableLabel):
    def __init__(self, widget,  name=''):
        super().__init__(name, widget)
        self.icon = QPixmap('img\\fileTransfer.png')
        self.setPixmap(self.icon)
        self.setScaledContents(True)

class FolderIcon(ClickableLabel):
    def __init__(self, widget,  name=''):
        super().__init__(name, widget)
        self.icon = QPixmap('img\\folder.png')
        self.setPixmap(self.icon)
        self.setScaledContents(True)

class FtpIcon(ClickableLabel):
    def __init__(self, widget,  name=''):
        super().__init__(name, widget)
        self.icon = QPixmap('img\\ftp.png')
        self.setPixmap(self.icon)
        self.setScaledContents(True)

class ProceedIcon(QLabel):
    def __init__(self, widget):
        super().__init__(widget)

        self.icons = (
            QPixmap('img\\proceed1.png'),
            QPixmap('img\\Proceed2.png'),
            QPixmap('img\\Proceed3.png'),
            QPixmap('img\\Proceed4.png'),
            QPixmap('img\\Proceed5.png'),
            QPixmap('img\\Proceed6.png'),
            QPixmap('img\\Proceed7.png'),
            QPixmap('img\\Proceed8.png'),
        )
        self.setPixmap(self.icons[0])
        self.setScaledContents(True)
        self.active = False
        self.icon_num = 0
        self.timer = QTimer(self)

    def run(self):

        if self.active:
            self.show()
            self.setPixmap(self.icons[self.icon_num])
            self.icon_num += 1
            if self.icon_num == 8:
                self.icon_num = 0
            self.timer.singleShot(300, self.run)
        else:
            self.hide()




