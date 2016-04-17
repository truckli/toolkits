#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class CalendarSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super(CalendarSelectionDialog, self).__init__(parent)
        self.parent = parent
        self._setupUi()

    def _setupUi(self):
        grid = QGridLayout()
        dateSelLabel = QLabel("Specify a date:")
        self.calen = QCalendarWidget()
        timeSelLabel = QLabel("Specify time of a day:")
        self.hourSpinBox = QSpinBox()
        self.hourSpinBox.setRange(0, 23)
        self.hourSpinBox.setPrefix("Hour:")
        self.hourSpinBox.setValue(QTime.currentTime().hour())
        self.minuteSpinBox = QSpinBox()
        self.minuteSpinBox.setRange(0, 59)
        self.minuteSpinBox.setPrefix("Minute:")
        self.minuteSpinBox.setValue(QTime.currentTime().minute())
        self.secondSpinBox = QSpinBox()
        self.secondSpinBox.setRange(0, 59)
        self.secondSpinBox.setPrefix("Second:")
        self.secondSpinBox.setValue(QTime.currentTime().second())

        timeLayout = QHBoxLayout()
        timeLayout.addWidget(self.hourSpinBox)
        timeLayout.addWidget(self.minuteSpinBox)
        timeLayout.addWidget(self.secondSpinBox)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.hide)

        grid.addWidget(dateSelLabel, 0, 0, 1, 2)
        grid.addWidget(self.calen, 1, 0)
        grid.addWidget(timeSelLabel, 2, 0, 1, 2)
        grid.addLayout(timeLayout, 3, 0)
        grid.addWidget(self.buttonBox, 4, 0)
        self.setLayout(grid)
        self.setWindowTitle("Date&Time Setting:")

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.baseCalDialog = None
        self.targetCalDialog = None
        self._setupUi()

    def _setupUi(self):
        self.baseLabel = QLabel("Base time:")
        self.baseDateTimeEdit = QDateTimeEdit()
        self.baseDateTimeEdit.setDisplayFormat("yyyy/MM/dd hh:mm:ss")
        self.baseDateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.baseButton = QPushButton(">>")
        baseLayout = QHBoxLayout()
        baseLayout.addWidget(self.baseDateTimeEdit)
        baseLayout.addWidget(self.baseButton)
        baseLayout.addStretch()

        self.diffLabel = QLabel("Difference:")
        self.diffDaySpinBox = QSpinBox()
        self.diffDaySpinBox.setRange(-100000, 100000)
        self.diffDaySpinBox.setValue(0)
        self.diffDaySpinBox.setSuffix(" day(s)")

        self.diffHourSpinBox = QSpinBox()
        self.diffHourSpinBox.setRange(-100000, 100000)
        self.diffHourSpinBox.setValue(0)
        self.diffHourSpinBox.setSuffix(" hour(s)")

        self.diffMinuteSpinBox = QSpinBox()
        self.diffMinuteSpinBox.setRange(-100000, 100000)
        self.diffMinuteSpinBox.setValue(0)
        self.diffMinuteSpinBox.setSuffix(" minute(s)")

        self.diffSecondSpinBox = QSpinBox()
        self.diffSecondSpinBox.setRange(-100000, 100000)
        self.diffSecondSpinBox.setValue(0)
        self.diffSecondSpinBox.setSuffix("second(s)")

        diffLayout = QHBoxLayout()
        diffLayout.addWidget(self.diffDaySpinBox)
        diffLayout.addWidget(self.diffHourSpinBox)
        diffLayout.addWidget(self.diffMinuteSpinBox)
        diffLayout.addWidget(self.diffSecondSpinBox)

        self.targetLabel = QLabel("Target time:")
        self.targetDateTimeEdit = QDateTimeEdit()
        self.targetDateTimeEdit.setDisplayFormat("yyyy/MM/dd hh:mm:ss")
        self.targetDateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.targetButton = QPushButton(">>")

        targetLayout = QHBoxLayout()
        targetLayout.addWidget(self.targetDateTimeEdit)
        targetLayout.addWidget(self.targetButton)
        targetLayout.addStretch()

        grid = QGridLayout()
        grid.addWidget(self.baseLabel, 0, 0)
        grid.addLayout(baseLayout, 0, 1)
        grid.addWidget(self.diffLabel, 1, 0)
        grid.addLayout(diffLayout, 1, 1)
        grid.addWidget(self.targetLabel, 2, 0)
        grid.addLayout(targetLayout, 2, 1)
        self.setLayout(grid)

        self.connect(self.baseDateTimeEdit, SIGNAL("dateTimeChanged(QDateTime)"), self._calcTarget)
        self.connect(self.targetDateTimeEdit, SIGNAL("dateTimeChanged(QDateTime)"), self._calcDiff)
        self.connect(self.baseButton, SIGNAL("clicked()"), self._showBaseCalendar)
        self.connect(self.targetButton, SIGNAL("clicked()"), self._showTargetCalendar)
        self.connect(self.diffDaySpinBox, SIGNAL("valueChanged(int)"), self._calcTarget)
        self.connect(self.diffHourSpinBox, SIGNAL("valueChanged(int)"), self._calcTarget)
        self.connect(self.diffMinuteSpinBox, SIGNAL("valueChanged(int)"), self._calcTarget)
        self.connect(self.diffSecondSpinBox, SIGNAL("valueChanged(int)"), self._calcTarget)

    def _setBaseFromCalendar(self):
        self.baseCalDialog.hide()
        date = self.baseCalDialog.calen.selectedDate()
        self.baseDateTimeEdit.setDate(date)
        time = QTime(self.baseCalDialog.hourSpinBox.value(), self.baseCalDialog.minuteSpinBox.value(), self.baseCalDialog.secondSpinBox.value())
        self.baseDateTimeEdit.setTime(time)

    def _setTargetFromCalendar(self):
        self.targetCalDialog.hide()
        date = self.targetCalDialog.calen.selectedDate()
        time = QTime(self.targetCalDialog.hourSpinBox.value(), self.targetCalDialog.minuteSpinBox.value(), self.targetCalDialog.secondSpinBox.value())
        self.targetDateTimeEdit.setDate(date)
        self.targetDateTimeEdit.setTime(time)

    def _calcTarget(self):
        compDayTime = self.baseDateTimeEdit.dateTime() 
        diffDays = self.diffDaySpinBox.value()
        diffSecs = self.diffSecondSpinBox.value() + self.diffMinuteSpinBox.value()*60 + self.diffHourSpinBox.value()*3600 
        compDayTime = compDayTime.addDays(diffDays)
        compDayTime = compDayTime.addSecs(diffSecs)
        self.targetDateTimeEdit.setDateTime(compDayTime)

    def _calcDiff(self):
        baseDayTime = self.baseDateTimeEdit.dateTime() 
        diff = baseDayTime.secsTo(self.targetDateTimeEdit.dateTime())
        self.diffSecondSpinBox.setValue(diff % 60)
        diff = diff / 60 
        self.diffMinuteSpinBox.setValue(diff % 60)
        diff = diff / 60 
        self.diffHourSpinBox.setValue(diff % 24)
        diff = diff / 24
        self.diffDaySpinBox.setValue(diff)
       
    def _showBaseCalendar(self):
        if self.baseCalDialog == None:
            self.baseCalDialog = CalendarSelectionDialog(self)
            self.connect(self.baseCalDialog.buttonBox, SIGNAL("accepted()"), self._setBaseFromCalendar)

        self.baseCalDialog.show()
        self.baseCalDialog.raise_()
        self.baseCalDialog.activateWindow()

    def _showTargetCalendar(self):
        if self.targetCalDialog == None:
            self.targetCalDialog = CalendarSelectionDialog(self)
            self.connect(self.targetCalDialog.buttonBox, SIGNAL("accepted()"), self._setTargetFromCalendar)

        self.targetCalDialog.show()
        self.targetCalDialog.raise_()
        self.targetCalDialog.activateWindow()


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()



