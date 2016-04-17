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


class advancedForm(QDialog):
    def __init__(self, parent=None):
        super(advancedForm, self).__init__(parent)
        self.parent = parent
        self._setupUi()
        self.connect(self.buttonBox, SIGNAL("accepted()"),
                self, SLOT("accept()"))
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                self, SLOT("reject()"))


    def _setupUi(self):
        grid = QGridLayout()
        funcLabel = QLabel("Specify a rate for each deposit method:")
        grid.addWidget(funcLabel, 0, 0, 1, 2)

        self.rateSpinBoxes = {}
        depositMonths = self.parent.rateTable.keys()
        depositMonths.sort()
        for i in range(0, len(depositMonths)):
            grid.addWidget(QLabel(self.parent.labelTexts[i]), i+1, 0)
            rateSpinBox = QDoubleSpinBox();
            rateSpinBox.setRange(0.01, 100);
            rateSpinBox.setSingleStep(0.01)
            rateSpinBox.setValue(self.parent.rateTable[depositMonths[i]])
            rateSpinBox.setSuffix("%")
            self.rateSpinBoxes[depositMonths[i]] = rateSpinBox
            grid.addWidget(rateSpinBox, i+1, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        grid.addWidget(self.buttonBox, len(depositMonths)+1, 0, 1, 2)
        self.setLayout(grid)
        self.setWindowTitle("Default rate setting")



class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.rateTable = {0:0.5, 3:2.85, 6:3.05, 12:3.25, 24:3.75, 36:4.25, 48:4.5, 60:4.75}
        self.labelTexts = ("Current", "3 Months Fixed", "6 Months Fixed", 
                "1 Year Fixed", "2 Years Fixed", "3 Years Fixed", "4 Years Fixed", "5 Years Fixed")
        self._setupUi()

    def getMonths(self):
        return self.yearSpinBox.value()*12 + self.monthSpinBox.value()

    def getTPeriod(self):
        """returns time length of currently selected deposit period in months, or 0 for Current"""
        depositMonths = []
        depositMonths[:] = self.rateTable.keys()
        depositMonths.sort()
        return depositMonths[self.periodComboBox.currentIndex()]

    def getNPeriod(self):
        """ returns count of fixed periods within the deposit time. """
        try:
            return round(self.getMonths()/self.getTPeriod())
        except ZeroDivisionError:
            return -1

    def getSettedRate(self):
        return self.rateTable[self.getTPeriod()]

    def _autoUpdateRate(self):
        self.rateSpinBox.setValue(self.getSettedRate())

    def _clearWidgets(self):
        self.principalSpinBox.setValue(0)
        self.periodComboBox.setCurrentIndex(0)
        self.monthSpinBox.setValue(0)
        self.yearSpinBox.setValue(0)
        self._autoUpdateRate()
        self.updateUi()
    
    @staticmethod
    def periodCmp(x, y):
        return int.__cmp__(int(x), int(y))

    def _setupUi(self):
        principalLabel = QLabel("Principal:")
        self.principalSpinBox = QDoubleSpinBox()
        self.principalSpinBox.setRange(0, 1000000000)
        self.principalSpinBox.setValue(1000)
        self.principalSpinBox.setPrefix("$ ")
        self.clearPrincipalButton = QPushButton()
        self.clearPrincipalButton.setText("Clear") 

        periodLabel = QLabel("Deposit Period:")
        self.periodComboBox = QComboBox()
        self.periodComboBox.addItems(self.labelTexts)

        rateLabel = QLabel("Rate:")
        self.rateSpinBox = QDoubleSpinBox()
        self.rateSpinBox.setRange(0.01, 100)
        self.rateSpinBox.setSingleStep(0.01)
        self.rateSpinBox.setSuffix(" %")

        self.advancedButton = QPushButton();
        self.advancedButton.setText(">>>");

        timeLabel = QLabel("Deposit Time:")
        self.yearSpinBox = QSpinBox()
        self.yearSpinBox.setRange(0, 300) 
        self.yearSpinBox.setValue(1)
        self.yearSpinBox.setSuffix(" year(s)")
        self.monthSpinBox = QSpinBox()
        self.monthSpinBox.setRange(0, 11) 
        self.monthSpinBox.setValue(0)
        self.monthSpinBox.setSuffix(" month(s)")

        self.amountLabel = QLabel()
        self.dueLabel = QLabel()

        grid = QGridLayout()
        grid.addWidget(principalLabel, 0, 0)
        grid.addWidget(self.principalSpinBox, 0, 1)
        grid.addWidget(self.clearPrincipalButton, 0, 2)
        grid.addWidget(rateLabel, 1, 0)
        grid.addWidget(self.rateSpinBox, 1, 1)
        grid.addWidget(self.advancedButton, 1, 2)
        grid.addWidget(periodLabel, 2, 0)
        grid.addWidget(self.periodComboBox, 2, 1)
        grid.addWidget(timeLabel, 3, 0)
        grid.addWidget(self.yearSpinBox, 3, 1)
        grid.addWidget(self.monthSpinBox, 3, 2)
        grid.addWidget(self.amountLabel, 4, 1)
        grid.addWidget(self.dueLabel, 5, 0, 1, 3)
        self.setLayout(grid)

        self.connect(self.principalSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)
        self.connect(self.rateSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)
        self.connect(self.yearSpinBox, SIGNAL("valueChanged(int)"), self.updateUi)
        self.connect(self.monthSpinBox, SIGNAL("valueChanged(int)"), self.updateUi)
        self.connect(self.clearPrincipalButton, SIGNAL("clicked()"), self._clearWidgets)
        self.connect(self.advancedButton, SIGNAL("clicked()"), self._advancedSetting)
        self.connect(self.periodComboBox, SIGNAL("currentIndexChanged(int)"), self._autoUpdateRate)
        
        self.setWindowTitle("Interest Calc")
        self._autoUpdateRate()
        self.updateUi()

       
    def _handleCurrentCalc(self):
        principal = self.principalSpinBox.value()
        quarterRate = self.rateSpinBox.value()/3.0
        quarters = self.getMonths()/3
        amount = principal * (1 + (quarterRate/100.0)*quarters)
        self.amountLabel.setText("Amount: $ %.2f. " % amount)
        self.dueLabel.setText("Currency saving: interest decided every quarter")

    def _handleFixedCalc(self):
        principal = self.principalSpinBox.value()
        NPeriod = self.getNPeriod()
        monthRate = self.rateSpinBox.value()/12.0
        TPeriod = self.getTPeriod()
        amount = principal * ((1 + (monthRate/100.0)*TPeriod) ** NPeriod)
        self.amountLabel.setText("Amount: $ %.2f." % amount)
        dueMonths = TPeriod*(NPeriod+1) - self.getMonths()

        if NPeriod == 0:
            if dueMonths == TPeriod:
                dueStr = "new account."
            elif dueMonths == 1:
                dueStr = "due in one month."
            else:
                dueStr = "due in %d months." % dueMonths
        elif NPeriod == 1:
            if dueMonths == TPeriod:
                dueStr = "Due now"
            elif dueMonths == 1:
                dueStr = "1 due passed. Second due next month."
            else:
                dueStr = "1 due passed. Second due in %d months." % dueMonths
        else:
            dueStr = "%d dues passed." % NPeriod
            if dueMonths == TPeriod:
                dueStr += "Due again now."
            elif dueMonths == 1:
                dueStr += "Due again next month."
            else:
                dueStr += "Due again in %d months." % dueMonths

        dueStr = "Fixed deposit: " + dueStr
        self.dueLabel.setText(dueStr)


    def updateUi(self):
        if self.periodComboBox.currentIndex() == 0:
            self._handleCurrentCalc()
        else:
            self._handleFixedCalc()
        
    def _advancedSetting(self):
        dialog = advancedForm(self)
        if dialog.exec_():
            for key in self.rateTable.keys():
                self.rateTable[key] = dialog.rateSpinBoxes[key].value()

            self._autoUpdateRate()
            self.updateUi()

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()



