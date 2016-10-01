# coding:utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import re


class Find(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Find, self).__init__(parent)
        self.parent = parent
        self.lastMatch = None
        self.initUI()

    def initUI(self):
        findButton = QtGui.QPushButton(u"寻找", self)
        findButton.clicked.connect(self.find)

        replaceButton = QtGui.QPushButton(u"替换", self)
        replaceButton.clicked.connect(self.replace)

        allButton = QtGui.QPushButton(u"替换全部", self)
        allButton.clicked.connect(self.replaceAll)

        self.normalRadio = QtGui.QRadioButton(u"正常",self)
        self.normalRadio.toggled.connect(self.normalMode)

        self.regexRadio = QtGui.QRadioButton(u"正则",self)
        self.regexRadio.toggled.connect(self.regexMode)

        self.findField = QtGui.QTextEdit(self)
        self.findField.resize(250,50)

        self.replaceField = QtGui.QTextEdit(self)
        self.replaceField.resize(250,50)

        optionsLabel = QtGui.QLabel(u"选项",self)

        self.caseSenses = QtGui.QCheckBox(u"case sensitive",self)

        self.wholeWorlds = QtGui.QCheckBox(u"整个单词",self)

        layout = QtGui.QGridLayout()

        layout.addWidget(self.findField,1,0,1,4)
        layout.addWidget(self.normalRadio,2,2)
        layout.addWidget(self.regexRadio,2,3)
        layout.addWidget(findButton,2,0,1,2)

        layout.addWidget(self.replaceField,3,0,1,4)
        layout.addWidget(replaceButton,4,0,1,2)
        layout.addWidget(allButton,4,2,1,2)

        spacer = QtGui.QWidget(self)
        spacer.setFixedSize(0,10)

        layout.addWidget(spacer,5,0)

        layout.addWidget(optionsLabel,6,0)
        layout.addWidget(self.caseSenses,6,1)
        layout.addWidget(self.wholeWorlds,6,2)

        self.setGeometry(300,300,360,250)
        self.setWindowTitle(u"寻找和替换")
        self.setLayout(layout)

        self.normalRadio.setChecked(True)

    def find(self):
        text = self.parent.text.toPlainText()

        query = self.findField.toPlainText()

        if self.wholeWorlds.isChecked():
            query = str(r"\w"+query+r"\w")
        flags = 0 if self.caseSenses.isChecked() else re.I

        pattern = re.compile(str(query),flags)

        start = self.lastMatch.start()+1 if self.lastMatch else 0

        self.lastMatch = pattern.search(text,start)

        if self.lastMatch:

            start = self.lastMatch.start()
            end = self.lastMatch.end()

            if self.wholeWorlds.isChecked():
                start += 1
                end -= 1

            self.moveCursor(start,end)
        else:
            self.parent.text.moveCursor(QtGui.QTextCursor.End)

    def replace(self):
        cursor = self.parent.text.textCursor()
        if self.lastMatch and cursor.hasSelection():
            cursor.insertText(self.replaceField.toPlainText())
            self.parent.text.setTextCursor(cursor)

    def replaceAll(self):
        self.lastMatch = None

        self.find()
        while self.lastMatch:
            self.replace()
            self.find()

    def regexMode(self):

        self.caseSenses.setChecked(False)
        self.wholeWorlds.setChecked(False)

        self.caseSenses.setEnabled(False)
        self.wholeWorlds.setEnabled(False)

    def normalMode(self):
        self.caseSenses.setEnabled(True)
        self.wholeWorlds.setEnabled(True)

    def moveCursor(self,start,end):
        cursor = self.parent.text.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,end-start)

        self.parent.text.setTextCursor(cursor)



