import sys
import tour
import sqlite3

from ui.results_input import *
from PyQt5 import QtCore, QtGui, QtWidgets


class ButtonBlock(QtWidgets.QWidget):
    def __init__(self, *args):
        super(QtWidgets.QWidget, self).__init__()
        global nTeam
        self.grid = QtWidgets.QGridLayout()
        for g in range(nTeam):
            pushButton = QtWidgets.QPushButton(self)
            pushButton.setText("Команда " + str(g + 1))
            pushButton.setCheckable(1)
            pushButton.clicked.connect(self.make_calluser(g))
            self.grid.addWidget(pushButton, g // 4, g % 4)

        self.setLayout(self.grid)

    def make_calluser(self, curT):
        def calluser():
            cur.execute(f"""UPDATE Team SET score = score + 1
                            WHERE id_table = {curT}""")
            con.commit()

        return calluser

    def get(self):
        return self.grid


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        tours = [tour.Tour(12, 3), tour.Tour(12, 2), tour.Tour(12, 6)]
        self.ui.setupUi(self)

        count = 0
        for i in tours:
            global nTeam
            nTeam = len(i.teamScore)
            tab = QtWidgets.QWidget()
            verticalLayout = QtWidgets.QVBoxLayout(tab)
            verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            tabWidget = QtWidgets.QTabWidget(tab)
            for j in range(i.countQ):
                tabQuestion = QtWidgets.QWidget()
                bt = ButtonBlock()
                bt.setParent(tabQuestion)

                tabWidget.addTab(tabQuestion, str(j + 1) + " вопрос")

            verticalLayout.addWidget(tabWidget)
            self.ui.tabWidget.addTab(tab, str(count + 1) + " тур")
            count += 1


if __name__ == "__main__":
    global con, cur

    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()

    con = sqlite3.connect('db')
    cur = con.cursor()
    con.commit()

    sys.exit(app.exec_())
