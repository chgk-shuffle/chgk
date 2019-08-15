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
            sender = self.sender()
            if sender.isChecked():
                point = 1
            else:
                point = -1
            cur.execute(f"""UPDATE Team SET score = score + {point}
                            WHERE id_table = {curT}""")
            con.commit()

        return calluser

    def get(self):
        return self


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        tours = [tour.Tour(12, 3), tour.Tour(12, 2), tour.Tour(12, 6)]
        self.ui.setupUi(self)

        global cur
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
                VerL = QtWidgets.QVBoxLayout(tabQuestion)
                bt = ButtonBlock()
                VerL.addWidget(bt)

                tabWidget.addTab(tabQuestion, str(j + 1) + " вопрос")

            
            DistribTable = QtWidgets.QTableWidget()
            DistribTable.setColumnCount(2)
            DistribTable.setRowCount(nTeam)
            DistribTable.setHorizontalHeaderLabels(['Номер команды', 'Кол-во очков'])
            ResInTour = cur.execute("""
                                    SELECT name, score FROM User
                                    ORDER BY score DESC
                                    """).fetchall()
            for i in range(len(ResInTour)):
                for j in range(len(ResInTour[i])):
                    DistribTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(ResInTour[i][j])))
            tabWidget.addTab(DistribTable, "Распределение")


            verticalLayout.addWidget(tabWidget)
            self.ui.tabWidget.addTab(tab, str(count + 1) + " тур")
            count += 1
        TabFinallRes = QtWidgets.QTableWidget()
        TabFinallRes.setColumnCount(2)

        TabFinallRes.setRowCount(cur.execute("""
                                        SELECT count(*) FROM User
                                        """).fetchone()[0])
        TabFinallRes.setHorizontalHeaderLabels(['Фамилия и Имя', 'Кол-во очков'])
        FinallRes = cur.execute("""
                        SELECT name, score FROM User
                        ORDER BY score DESC
                        """).fetchall()
        for i in range(len(FinallRes)):
            for j in range(len(FinallRes[i])):
                TabFinallRes.setItem(i, j, QtWidgets.QTableWidgetItem(str(FinallRes[i][j])))
        self.ui.tabWidget.addTab(TabFinallRes, "Итоги")

if __name__ == "__main__":
    global con, cur

    con = sqlite3.connect('db')
    cur = con.cursor()
    con.commit()
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()



    sys.exit(app.exec_())
