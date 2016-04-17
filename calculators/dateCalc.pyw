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
        funcLabel = QLabel("Specify a base date:")
        self.calen = QCalendarWidget()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.hide)

        grid.addWidget(funcLabel, 0, 0, 1, 2)
        grid.addWidget(self.calen, 1, 0)
        grid.addWidget(self.buttonBox, 2, 0)
        self.setLayout(grid)
        self.setWindowTitle("Date setting:")

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.baseCalDialog = None
        self.targetCalDialog = None
        self._setupUi()

    def _setupUi(self):
        self.baseDateLabel = QLabel("Base date:")
        self.baseDateEdit = QDateEdit()
        self.baseDateEdit.setDisplayFormat("yyyy-MM-dd")
        self.baseDateEdit.setDate(QDate.currentDate())
        self.baseButton = QPushButton(">>")

        self.diffLabel = QLabel("Difference:")
        self.diffSpinBox = QSpinBox()
        self.diffSpinBox.setRange(-100000, 100000)
        self.diffSpinBox.setValue(0)
        self.diffSpinBox.setSuffix("day(s)")
        self.resultLabel = QLabel()

        self.targetDateLabel = QLabel("Target date:")
        self.targetDateEdit = QDateEdit()
        self.targetDateEdit.setDisplayFormat("yyyy-MM-dd")
        self.targetDateEdit.setDate(QDate.currentDate())
        self.targetButton = QPushButton(">>")

        grid = QGridLayout()
        grid.addWidget(self.baseDateLabel, 1, 0)
        grid.addWidget(self.baseDateEdit, 1, 1)
        grid.addWidget(self.baseButton, 1, 2)
        grid.addWidget(self.diffLabel, 2, 0)
        grid.addWidget(self.diffSpinBox, 2, 1)
        grid.addWidget(self.targetDateLabel, 3, 0)
        grid.addWidget(self.targetDateEdit, 3, 1)
        grid.addWidget(self.targetButton, 3, 2)
        self.setLayout(grid)

        self.connect(self.baseDateEdit, SIGNAL("dateChanged(QDate)"), self._calcDate)
        self.connect(self.targetDateEdit, SIGNAL("dateChanged(QDate)"), self._calcDiff)
        self.connect(self.baseButton, SIGNAL("clicked()"), self._showBaseCalendar)
        self.connect(self.targetButton, SIGNAL("clicked()"), self._showTargetCalendar)
        self.connect(self.diffSpinBox, SIGNAL("valueChanged(int)"), self._calcDate)

    def _setBaseFromCalendar(self):
        self.baseCalDialog.hide()
        self.baseDateEdit.setDate(self.baseCalDialog.calen.selectedDate())

    def _setTargetFromCalendar(self):
        self.targetCalDialog.hide()
        self.targetDateEdit.setDate(self.targetCalDialog.calen.selectedDate())

    def _calcDate(self):
        baseDay = self.baseDateEdit.date() 
        diff = self.diffSpinBox.value()
        self.targetDateEdit.setDate(baseDay.addDays(diff))

    def _calcDiff(self):
        baseDay = self.baseDateEdit.date() 
        targetDay = self.targetDateEdit.date() 
        self.diffSpinBox.setValue(baseDay.daysTo(targetDay))
       
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



