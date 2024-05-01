# -*- coding: utf-8 -*-

"""
Program: Simple Piano
Author: MrCrawL
Created Time: 2024-04-23
Last Modified: 2024-05-01
PS. 2024-04-24 by MrCrawL: Creat file and realize basic functions
    2024-04-25 by MrCrawL: Add display information function and modify sound system
    2024-04-26 by MrCrawL: Fix file not found bug and optimize code
    2024-04-28 by MrCrawL: Fix bug that mouse click doesn't display information
    2024-04-30 by MrCrawL: Add more soundLib and improve keyboard release fluency
    2024-05-01 by MrCrawL: Add check update function and fix some bugs
"""

import os, sys, pygame, logging, requests
from PyQt6.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QThread, pyqtSignal
from xu_ui import Ui_Form
from mr_ico import icon_hex  # fixme: comment this line please, or it might raise Exception
from pynput.keyboard import Listener
from threading import Thread
from time import sleep
from lxml.etree import HTML
import webbrowser

# 版本号
VERSION = '1.2.9'
NEW_VERSION = ''

# 获取文件路径
FILE_PATH = None
if getattr(sys, 'frozen', False):
    FILE_PATH = os.path.join(os.path.dirname(sys.executable), os.path.basename(sys.executable))
else:
    FILE_PATH = os.path.abspath(__file__)
FILE_DIRNAME = os.path.dirname(FILE_PATH)
# print(FILE_DIRNAME)
soundLibDir = os.path.join(FILE_DIRNAME, r'soundLib')
if os.path.exists(soundLibDir):
    soundLibPath = os.path.join(soundLibDir, os.listdir(soundLibDir)[0])
else:
    soundLibPath = None

# Ord 0-48, pick 32 from 49
NOTE_LIST = ['C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
             'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
             'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5',
             'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 'C7']
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
ORD_MAP = {'C': 12, 'C#': 13, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
ORDER = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28,29,31,1,3,6,8,10,13,15,18,20,22,25,27,30]
SCALE_MAP = {
    'Major (Ionian)': [0,2,4,5,7,9,11, 12,14,16,17,19,21,23, 24,26,28,29,31],
    'Major Bebop': [0,2,4,5,7,8,9,11, 12,14,16,17,19,20,21,23, 24,26,28,29,31],
    'Major Bulgarian': [0,2,5,6,8,9,11, 12,14,17,18,20,21,23, 24,26,29,30],
    'Major Hexatonic': [0,2,4,5,7,9, 12,14,16,17,19,21, 24,26,28,29,31],
    'Major Pentatonic': [0,2,4,7,9, 12,14,16,19,21, 24,26,28,31],
    'Major Persian': [0,1,4,5,6,8,11, 12,13,16,17,18,20,23, 24,25,28,29,30],
    'Major Polymode': [0,2,3,5,6,8,10,11, 12,14,15,17,18,20,22,23, 24,26,27,29,30],
    'Minor Harmonic': [0,2,3,5,7,8,11, 12,14,15,17,19,20,23, 24,26,27,29,31],
    'Minor Hungarian': [0,2,3,6,7,8,11, 12,14,15,18,19,20,23, 24,26,27,30,31],
    'Minor Melodic': [0,2,3,5,7,9,11, 12,14,15,17,19,21,23, 24,26,27,29,31],
    'Minor Natural (Aeolian)': [0,2,3,5,7,8,10, 12,14,15,17,19,20,22, 24,26,27,29,31],
    'Minor Neapolitan': [0,1,3,5,7,8,11, 12,13,15,17,19,20,23, 24,25,27,29,31],
    'Minor Pentatonic': [0,3,5,7,10, 12,15,17,19,22, 24,27,29,31],
    'Minor Polymode': [0,1,2,4,5,7,8,10, 12,13,14,16,17,19,20,22, 24,25,26,28,29,31],
    'Minor Romanian': [0,2,3,6,7,9,10, 12,14,15,18,19,21,22, 24,26,27,30,31],
    'Other Arabic': [0,1,4,5,7,8,11, 12,13,16,17,19,20,23, 24,25,28,29,31],
    'Other Bebop Dominant': [0,2,4,5,7,9,10,11, 12,14,16,17,19,21,22,23, 24,26,28,29,31],
    'Other Blues': [0,3,5,6,7,10, 12,15,17,18,19,22, 24,27,29,30,31],
    'Other Blues Nonatonic': [0,2,3,4,5,6,7,9,10, 12,14,15,16,17,18,19,21,22, 24,26,27,28,29,30,31],
    'Other Diminished': [0,2,3,5,6,8,9,11, 12,14,15,17,18,20,21,23, 24,26,27,29,30],
    'Other Dorian': [0,2,3,5,7,9,10, 12,14,15,17,19,21,22, 24,26,27,29,31],
    'Other Eastern': [0,2,3,5,7,8,10,11, 12,14,15,17,19,20,22,23, 24,26,27,29,31],
    'Other Egyptian': [0,2,5,7,10, 12,14,17,19,22, 24,26,29,31],
    'Other Enigmatic': [0,1,4,6,8,10,11, 12,13,16,18,20,22,23, 24,25,28,30],
    'Other Hirajoshi': [0,2,3,7,8, 12,14,15,19,20, 24,26,27,31],
    'Other Iwato': [0,1,5,6,10, 12,13,17,18,22, 24,25,29,30],
    'Other Japanese Insen': [0,1,5,7,10, 12,13,17,19,22, 24,25,29,31],
    'Other Locrian': [0,1,3,5,6,8,10, 12,13,15,17,18,20,22, 24,25,27,29,30],
    'Other Locrian Super': [0,1,3,4,6,8,10, 12,13,15,16,18,20,22, 24,25,27,28,30],
    'Other Lydian': [0,2,4,6,7,9,11, 12,14,16,18,19,21,23, 24,26,28,30,31],
    'Other Mixolydian': [0,2,4,5,7,9,10, 12,14,16,17,19,21,22, 24,26,28,29,31],
    'Other Neapolitan': [0,1,3,5,7,9,11, 12,13,15,17,19,21,23, 24,25,27,29,31],
    'Other Phrygian': [0,1,3,5,7,8,10, 12,13,15,17,19,20,22, 24,25,27,29,31],
    'Other Phrygian Dominant': [0,1,4,5,7,8,10, 12,13,16,17,19,20,22, 24,25,28,29,31],
    'Other Piongio': [0,2,5,7,9,10, 12,14,17,19,21,22, 24,26,29,31],
    'Other Prometheus': [0,2,4,6,9,10, 12,14,16,18,21,22, 24,26,28,30],
    'Other Whole Tone': [0,2,4,6,8,10, 12,14,16,18,20,22, 24,26,28,30],
    'All': list(range(32)),
}
NUM_DICT = {'1':'I', '2':'II', '3':'III', '4':'IV', '5':'V', '6':'VI', '7':'VII', '8':'VIII', '9':'IX', '10':'X',
            '11':'XI', '12':'XII'}


class InfoThread(QThread):
    """显示按下键盘的音高和音阶所在级数"""
    finished = pyqtSignal()
    info = pyqtSignal()

    def run(self):
        self.info.emit()
        self.finished.emit()


class UpdateThread(QThread):
    """检查更新线程"""
    infoSignal = pyqtSignal(str)
    updateSignal = pyqtSignal(str)

    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        }
        url = 'https://github.com/MyGitRobot/SimplePiano/releases'

        def check_it():
            global NEW_VERSION
            try:
                res = requests.get(url, headers, timeout=5)
            except requests.exceptions.ConnectTimeout:
                self.infoSignal.emit('Connection time out. Please try again later.')
                return None
            html = HTML(res.text)
            versions = html.xpath('//span[@class="ml-1 wb-break-all"]/text()')
            NEW_VERSION = versions[0].strip()[1:]
            # print(f'[Info] The newest version: {NEW_VERSION}')
            if VERSION != NEW_VERSION:
                if not os.path.exists(os.path.join(FILE_DIRNAME, f'SimplePiano-{"-".join(NEW_VERSION.split("."))}.exe')):
                    self.updateSignal.emit(NEW_VERSION)

        Thread(target=check_it).start()


class KeyboardButton:
    """包含各种属性的自定义键盘按钮"""
    def __init__(self, push_button: QPushButton, note_name: str, state: bool = False):
        self.button = push_button  # 键盘对应的 Qt 按钮
        self.noteName = note_name  # 音名
        self.isPressed = state  # 按键是否被按下
        self.oggFile = os.path.join(soundLibPath, f'{self.noteName}.ogg')  # 音源文件路径
        self.sound = pygame.mixer.Sound(self.oggFile)  # 能发声的 Sound 对象

    def update_attrs(self, note_name: str):
        """更新键盘按钮的属性"""
        self.noteName = note_name
        self.oggFile = os.path.join(soundLibPath, f'{self.noteName}.ogg')
        self.sound = pygame.mixer.Sound(self.oggFile)

    def set_connections(self):
        """建立按钮和按下/释放函数的连接"""
        if self.button.receivers(self.button.pressed) > 0: self.button.pressed.disconnect()
        if self.button.receivers(self.button.released) > 0: self.button.released.disconnect()
        self.button.pressed.connect(lambda: ui.mouse_press(self))
        self.button.released.connect(lambda: ui.mouse_release(self))


class Window(QWidget, Ui_Form):
    """窗口 UI"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置窗口图标 fixme: comment the following 4 lines please, or it might raise Exception
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(bytes.fromhex(icon_hex))
        self.icon = QIcon(self.pixmap)
        self.setWindowIcon(self.icon)

        # 设置窗口标题
        self.setWindowTitle(f'{self.windowTitle() + " " + VERSION}')
        # 设置窗口固定大小
        self.setFixedSize(800, 500)
        # 调整黑键大小
        self.resize_black_keys()
        # 加载笔记内容
        self.load_notepad()

        # 调式选择
        self.comboRootNote.setFocus()
        self.comboRootNote.addItems(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])
        self.comboScale.addItems(SCALE_MAP.keys())

        self.rootNote = self.comboRootNote.currentText()
        self.scale = self.comboScale.currentText()
        self.scaleNoteOrds = SCALE_MAP[self.scale]
        self.label_scale.setText(f'Scale : C  D  E  F  G  A  B')
        # print(f'[Info] Root Note: {self.rootNote}, Scale: {self.scale}')
        self.comboRootNote.currentTextChanged.connect(self.update_info)
        self.comboScale.currentTextChanged.connect(self.update_info)
        self.pressedNoteOrds = []

        # 音色库
        try:
            self.comboSound.addItems(os.listdir(soundLibDir))
            self.comboSound.currentTextChanged.connect(self.togglt_sound_combo)

            # 初始化键盘和音符
            self.rootOrd = 12
            # 知道这里很冗长，但是不想优化了哈哈哈哈哈哈哈哈哈哈哈略略略
            self.whiteKey_1 = KeyboardButton(self.buttonWhiteKey_1, NOTE_LIST[self.rootOrd])
            self.whiteKey_2 = KeyboardButton(self.buttonWhiteKey_2, NOTE_LIST[self.rootOrd + 2])
            self.whiteKey_3 = KeyboardButton(self.buttonWhiteKey_3, NOTE_LIST[self.rootOrd + 4])
            self.whiteKey_4 = KeyboardButton(self.buttonWhiteKey_4, NOTE_LIST[self.rootOrd + 5])
            self.whiteKey_5 = KeyboardButton(self.buttonWhiteKey_5, NOTE_LIST[self.rootOrd + 7])
            self.whiteKey_6 = KeyboardButton(self.buttonWhiteKey_6, NOTE_LIST[self.rootOrd + 9])
            self.whiteKey_7 = KeyboardButton(self.buttonWhiteKey_7, NOTE_LIST[self.rootOrd + 11])
            self.whiteKey_8 = KeyboardButton(self.buttonWhiteKey_8, NOTE_LIST[self.rootOrd + 12])
            self.whiteKey_9 = KeyboardButton(self.buttonWhiteKey_9, NOTE_LIST[self.rootOrd + 14])
            self.whiteKey_10 = KeyboardButton(self.buttonWhiteKey_10, NOTE_LIST[self.rootOrd + 16])
            self.whiteKey_11 = KeyboardButton(self.buttonWhiteKey_11, NOTE_LIST[self.rootOrd + 17])
            self.whiteKey_12 = KeyboardButton(self.buttonWhiteKey_12, NOTE_LIST[self.rootOrd + 19])
            self.whiteKey_13 = KeyboardButton(self.buttonWhiteKey_13, NOTE_LIST[self.rootOrd + 21])
            self.whiteKey_14 = KeyboardButton(self.buttonWhiteKey_14, NOTE_LIST[self.rootOrd + 23])
            self.whiteKey_15 = KeyboardButton(self.buttonWhiteKey_15, NOTE_LIST[self.rootOrd + 24])
            self.whiteKey_16 = KeyboardButton(self.buttonWhiteKey_16, NOTE_LIST[self.rootOrd + 26])
            self.whiteKey_17 = KeyboardButton(self.buttonWhiteKey_17, NOTE_LIST[self.rootOrd + 28])
            self.whiteKey_18 = KeyboardButton(self.buttonWhiteKey_18, NOTE_LIST[self.rootOrd + 29])
            self.whiteKey_19 = KeyboardButton(self.buttonWhiteKey_19, NOTE_LIST[self.rootOrd + 31])
            self.blackKey_1 = KeyboardButton(self.buttonBlackKey_1, NOTE_LIST[self.rootOrd + 1])
            self.blackKey_2 = KeyboardButton(self.buttonBlackKey_2, NOTE_LIST[self.rootOrd + 3])
            self.blackKey_3 = KeyboardButton(self.buttonBlackKey_3, NOTE_LIST[self.rootOrd + 6])
            self.blackKey_4 = KeyboardButton(self.buttonBlackKey_4, NOTE_LIST[self.rootOrd + 8])
            self.blackKey_5 = KeyboardButton(self.buttonBlackKey_5, NOTE_LIST[self.rootOrd + 10])
            self.blackKey_6 = KeyboardButton(self.buttonBlackKey_6, NOTE_LIST[self.rootOrd + 13])
            self.blackKey_7 = KeyboardButton(self.buttonBlackKey_7, NOTE_LIST[self.rootOrd + 15])
            self.blackKey_8 = KeyboardButton(self.buttonBlackKey_8, NOTE_LIST[self.rootOrd + 18])
            self.blackKey_9 = KeyboardButton(self.buttonBlackKey_9, NOTE_LIST[self.rootOrd + 20])
            self.blackKey_10 = KeyboardButton(self.buttonBlackKey_10, NOTE_LIST[self.rootOrd + 22])
            self.blackKey_11 = KeyboardButton(self.buttonBlackKey_11, NOTE_LIST[self.rootOrd + 25])
            self.blackKey_12 = KeyboardButton(self.buttonBlackKey_12, NOTE_LIST[self.rootOrd + 27])
            self.blackKey_13 = KeyboardButton(self.buttonBlackKey_13, NOTE_LIST[self.rootOrd + 30])
        except Exception as err:
            msgBox = self.Msgbox('Notification', 'Sound files not found.\nPlease check your soundLib files.')
            msgBox.exec()
            error_logging(err)
            sys.exit()

        # 键盘按钮列表
        self.buttonKeys = [self.whiteKey_1, self.blackKey_1, self.whiteKey_2, self.blackKey_2, self.whiteKey_3,
                           self.whiteKey_4, self.blackKey_3, self.whiteKey_5, self.blackKey_4, self.whiteKey_6,
                           self.blackKey_5, self.whiteKey_7,
                           self.whiteKey_8, self.blackKey_6, self.whiteKey_9, self.blackKey_7, self.whiteKey_10,
                           self.whiteKey_11,self.blackKey_8, self.whiteKey_12,self.blackKey_9, self.whiteKey_13,
                           self.blackKey_10,self.whiteKey_14,
                           self.whiteKey_15,self.blackKey_11,self.whiteKey_16,self.blackKey_12,self.whiteKey_17,
                           self.whiteKey_18,self.blackKey_13,self.whiteKey_19]

        self.keyMap = {'z': self.whiteKey_1, 'x': self.whiteKey_2, 'c': self.whiteKey_3, 'v': self.whiteKey_4,
                       'b': self.whiteKey_5, 'n': self.whiteKey_6, 'm': self.whiteKey_7, ',': self.whiteKey_8,
                       '.': self.whiteKey_9, '/': self.whiteKey_10,'q': self.whiteKey_8, 'w': self.whiteKey_9,
                       'e': self.whiteKey_10,'r': self.whiteKey_11,'t': self.whiteKey_12,'y': self.whiteKey_13,
                       'u': self.whiteKey_14,'i': self.whiteKey_15,'o': self.whiteKey_16,'p': self.whiteKey_17,
                       '[': self.whiteKey_18,']': self.whiteKey_19,
                       's': self.blackKey_1, 'd': self.blackKey_2, 'g': self.blackKey_3, 'h': self.blackKey_4,
                       'j': self.blackKey_5, 'l': self.blackKey_6, ';': self.blackKey_7, '2': self.blackKey_6,
                       '3': self.blackKey_7, '5': self.blackKey_8, '6': self.blackKey_9, '7': self.blackKey_10,
                       '9': self.blackKey_11,'0': self.blackKey_12,'=': self.blackKey_13}

        # 显示音符
        self.keyOriginText = []
        self.keyOnScaleText = []

        # 信息线程
        self.infoThread = InfoThread()
        self.infoThread.info.connect(self.set_info_text)
        self.infoThread.finished.connect(self.display_info)

        # 创建键盘监听
        self.is_listening = False
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        # 设置键盘焦点事件
        self.boxKeyboard.focusInEvent = self.keyboardFocusInEvent
        self.boxKeyboard.focusOutEvent = self.keyboardFocusOutEvent

        # 绑定键盘信号槽
        self.buttonSaveNote.clicked.connect(self.save_notepad)  # 保存按钮
        self.build_connections()
        self.buttonSwitch.clicked.connect(self.switch_keys)

        # 检查更新
        self.updateThread = UpdateThread()
        self.updateThread.infoSignal.connect(self.pop_msgbox)
        self.updateThread.updateSignal.connect(self.ask_update)
        self.updateThread.start()

    def Msgbox(self, title: str, text: str, button: str = 'ok' or 'yn'):
        """对话框"""
        msgBox = QMessageBox()
        msgBox.setWindowIcon(self.icon)  # fixme: comment this line please, or it might raise Exception
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setIcon(QMessageBox.Icon.Information)
        if button == 'yn':
            msgBox.addButton(QMessageBox.StandardButton.Yes)
            msgBox.addButton(QMessageBox.StandardButton.No)
        else:
            msgBox.addButton(QMessageBox.StandardButton.Ok)
        return msgBox

    def pop_msgbox(self, text: str):
        """弹出对话框，内容为 text"""
        msgBox = self.Msgbox('Notification', text)
        msgBox.exec()

    def togglt_sound_combo(self):
        """切换音色"""
        global soundLibPath
        soundLibPath = os.path.join(soundLibDir, self.comboSound.currentText())
        self.switch_keys()

    def set_info_text(self):
        """设置 Scale 调内音信息"""
        self.keyOriginText = [button.noteName for button in self.buttonKeys if button.isPressed]
        keyNoteOrds = [NOTE_LIST.index(noteName)-self.rootOrd+12 for noteName in self.keyOriginText]  # [12, 16, 19]
        for i in range(len(keyNoteOrds)):
            while keyNoteOrds[i] > 11:
                keyNoteOrds[i] -= 12
        self.keyOnScaleText = [NUM_DICT[str(self.scaleNoteOrds.index(ele)+1)] if ele in self.scaleNoteOrds else '#'
                               for ele in keyNoteOrds]

    def display_info(self):
        """显示 Scale 文本"""
        self.lineKeyOrigin.setText('  '.join(self.keyOriginText))
        self.lineKeyOnScale.setText('  '.join(self.keyOnScaleText))

    def update_info(self):
        """更新信息"""
        self.rootNote = self.comboRootNote.currentText()
        self.rootOrd = ORD_MAP[self.rootNote]
        self.scale = self.comboScale.currentText()
        self.scaleNoteOrds = SCALE_MAP[self.scale]
        scaleOrds = [num for num in self.scaleNoteOrds if num < 12]  # 0, 2, 3, 5
        scaleOrds = [(num+self.rootOrd)%12 for num in scaleOrds]
        scaleNotes = [NOTE_NAMES[num] for num in scaleOrds]
        self.label_scale.setText(f'Scale : {"  ".join(scaleNotes)}')
        self.label_info.setText(f'State: display information as scale {self.rootNote} {self.scale}')
        # print(f'[Info] Root Note: {self.rootNote}, Scale: {self.scale}, Scale Ords: {self.scaleNoteOrds}')

    def switch_keys(self):
        """更换键盘绑定音高"""
        # print(f'[Info] Root Ord: {self.rootOrd}')
        for i in range(len(self.buttonKeys)):
            try:
                self.buttonKeys[i].update_attrs(NOTE_LIST[self.rootOrd + i])
            except Exception as err:
                self.pop_msgbox(f'Error occurred: {err}')
                return None
        self.label_info.setText('State: keys switched to current soundLib / scale')

    def on_press(self, key):
        """按下键盘发出声音"""
        if hasattr(key, 'char'):
            if self.is_listening and key.char in self.keyMap.keys():
                if not self.keyMap[key.char].isPressed:
                    self.infoThread.start()
                    self.keyMap[key.char].isPressed = True
                    self.keyMap[key.char].button.setDown(True)
                    self.start_sound(self.keyMap[key.char])

    def on_release(self, key):
        """释放按键停止声音"""
        if hasattr(key, 'char'):
            if self.is_listening and key.char in self.keyMap.keys():
                self.infoThread.start()
                self.keyMap[key.char].isPressed = False
                self.keyMap[key.char].button.setDown(False)
                self.stop_sound(self.keyMap[key.char])

    def mouse_press(self, button_key: KeyboardButton):
        """鼠标点击键盘"""
        if not button_key.isPressed:
            self.infoThread.start()
            button_key.isPressed = True
            self.start_sound(button_key)

    def mouse_release(self, button_key: KeyboardButton):
        """鼠标释放键盘"""
        self.infoThread.start()
        button_key.isPressed = False
        self.stop_sound(button_key)

    @staticmethod
    def start_sound(button_key: KeyboardButton):
        button_key.sound.stop()
        button_key.sound.set_volume(100)
        button_key.sound.play()

    @staticmethod
    def stop_sound(button_key: KeyboardButton):

        def fade_and_stop(note: KeyboardButton):
            for i in range(100, 0, -10):
                if note.isPressed: return None
                sleep(0.01)
                note.sound.set_volume(i / 100)
            note.sound.stop()

        Thread(target=lambda: fade_and_stop(button_key)).start()

    def keyboardFocusInEvent(self, event):
        self.is_listening = True
        QGroupBox.focusInEvent(self.boxKeyboard, event)

    def keyboardFocusOutEvent(self, event):
        self.is_listening = False
        for buttonKey in self.buttonKeys:
            buttonKey.button.setDown(False)
            buttonKey.isPressed = False
        QGroupBox.focusOutEvent(self.boxKeyboard, event)

    def build_connections(self):
        """建立鼠标点击的信号连接"""
        for buttonKey in self.buttonKeys:
            buttonKey.set_connections()

    def closeEvent(self, event):
        """退出程序时保存笔记内容"""
        self.save_notepad()
        self.is_listening = False
        event.accept()

    def load_notepad(self):
        """加载 notepad.txt"""
        if not os.path.exists(os.path.join(FILE_DIRNAME, 'notepad.txt')):
            with open(os.path.join(FILE_DIRNAME, 'notepad.txt'), 'w', encoding='utf-8') as f:
                f.write('')
        with open('notepad.txt', 'r', encoding='utf-8') as f:
            self.textNotePad.setText(f.read())
        self.label_info.setText('State: NotePad loaded successfully')
        # print('[Info] NotePad loaded')

    def save_notepad(self):
        """保存 notepad.txt"""
        with open('notepad.txt', 'w', encoding='utf-8') as f:
            f.write(self.textNotePad.toPlainText())
        self.label_info.setText('State: NotePad saved')
        # print('[Info] NotePad saved')

    def resize_black_keys(self):
        """调整所有黑键宽度"""
        buttonBlackKeys = [self.buttonBlackKey_1, self.buttonBlackKey_2, self.buttonBlackKey_3, self.buttonBlackKey_4,
                           self.buttonBlackKey_5, self.buttonBlackKey_6, self.buttonBlackKey_7, self.buttonBlackKey_8,
                           self.buttonBlackKey_9, self.buttonBlackKey_10, self.buttonBlackKey_11,
                           self.buttonBlackKey_12, self.buttonBlackKey_13]
        for button in buttonBlackKeys:
            button.setGeometry(button.x(), button.y(), button.width() - 1, button.height())

    def ask_update(self, version:str):
        """询问是否更新"""
        msgBox = self.Msgbox('Notification', f'There is a new version Simple Piano {version},\n'
                                    f'would you like to download now?', 'yn')
        result = msgBox.exec()
        if result == QMessageBox.StandardButton.Yes:
            webbrowser.open(f'https://github.com/MyGitRobot/SimplePiano/releases/tag/v{NEW_VERSION}')


def error_logging(error: Exception):
    """记录错误日志"""
    filename = os.path.join(FILE_DIRNAME, 'error.log')
    logging.basicConfig(filename=filename, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR,
                        encoding='utf-8')
    logging.error(f"Error o rccurred: {error}", exc_info=True)


if __name__ == '__main__':
    try:
        # 初始化 pygame，使用 pygame 发出声音
        pygame.mixer.init()
        # 初始化 Qt 窗口
        app = QApplication(sys.argv)
        ui = Window()
        ui.show()
        sys.exit(app.exec())

    except Exception as e:
        print(f'[Error] {e}')
        error_logging(e)
