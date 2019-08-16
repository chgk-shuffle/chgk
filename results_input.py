import sys
import tour
import sqlite3

from ui.results_input import *
from PyQt5 import QtCore, QtGui, QtWidgets


class ButtonBlock(QtWidgets.QWidget):
    def __init__(self, *args):
        tour = args[0]
        ques = args[1]
        super(QtWidgets.QWidget, self).__init__()
        global nTeam
        self.grid = QtWidgets.QGridLayout()
        for g in range(nTeam):
            pushButton = QtWidgets.QPushButton(self)
            pushButton.setText("Команда " + str(g + 1))
            pushButton.setCheckable(1)
            pushButton.tour = tour
            pushButton.ques = ques
            pushButton.clicked.connect(self.make_calluser(g))
            self.grid.addWidget(pushButton, g // 4, g % 4)

        self.setLayout(self.grid)

    def make_calluser(self, curT):
        def calluser():
            sender = self.sender()
            if sender.isChecked():
                point1 = 1
            else:
                point1 = -1
            cur.execute(f"""UPDATE Team SET score = score + {point1}
                            WHERE id_table = {curT}""")
            cur.execute(f"""UPDATE User SET score = score + {point1}
                            WHERE id_user IN (SELECT id_user FROM Team
                                                WHERE id_table = {curT}
                                                AND id_round = {sender.tour}
                                                )""")
            cur.execute(f"""UPDATE Question SET point = {1 if point1 == 1 else 0}
                            WHERE id_round = {sender.tour} AND question_number = {sender.ques}
                            AND id_table = {curT}""")
            con.commit()

        return calluser

    def get(self):
        return self


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.tours = [tour.Tour(12, 3, 0), tour.Tour(12, 2, 1), tour.Tour(12, 6, 2)]
        self.ui.setupUi(self)
        self.curRound = 0
        self.curQ = 0
        global cur, TabFinallRes
        global ResInTourTab
        ResInTourTab = []
        count = 0
        for i in self.tours:
            global nTeam
            nTeam = len(i.teamScore)
            tab = QtWidgets.QWidget()
            verticalLayout = QtWidgets.QVBoxLayout(tab)
            verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            tabWidget = QtWidgets.QTabWidget(tab)
            tabWidget.addTab(QtWidgets.QTabWidget(), "Распределение")
            for j in range(i.countQ):
                tabQuestion = QtWidgets.QWidget()
                VerL = QtWidgets.QVBoxLayout(tabQuestion)
                bt = ButtonBlock(i.id, j)
                VerL.addWidget(bt)

                tabWidget.addTab(tabQuestion, str(j + 1) + " вопрос")
            tabWidget.currentChanged.connect(self.onChangeResTourTab)
            ResInTourTab.append(QtWidgets.QTableWidget(nTeam, i.countQ + 2))
            ResInTourTab[i.id].setHorizontalHeaderLabels(
                ['Номер команды'] + ['Вопрос ' + str(g) for g in range(i.countQ)] + ['Сумма'])

            tabWidget.addTab(ResInTourTab[i.id], "Итоги тура")
            # self.LoadResTour(i.countQ)
            verticalLayout.addWidget(tabWidget)
            self.ui.tabWidget.addTab(tab, str(count + 1) + " тур")
            count += 1

        self.ui.tabWidget.currentChanged.connect(self.onChangeTourTab)

        TabFinallRes = QtWidgets.QTableWidget(cur.execute("""
                                        SELECT count(*) FROM User
                                        """).fetchone()[0], 2)
        TabFinallRes.setHorizontalHeaderLabels(['Фамилия и Имя', 'Кол-во очков'])
        TabFinallRes.horizontalHeader().sectionClicked.connect(self.onChangeHeadResTab)
        TabFinallRes.horizontalHeader().sectionDoubleClicked.connect(self.onChangeHeadResTab2)
        self.LoadRes(0)
        self.ui.tabWidget.addTab(TabFinallRes, "Итоги")

    def onChangeTourTab(self, i):
        self.curRound = i
        if i == len(self.tours):
            self.LoadRes(0)

    def onChangeResTourTab(self, i):
        if (i > 0) and (i < self.tours[self.curRound].countQ + 1):
            self.curQ = i
        if i == self.tours[self.curRound].countQ + 1:
            self.LoadResTour(self.tours[self.curRound].countQ)

    def onChangeHeadResTab(self, logicalIndex):
        if logicalIndex == 0:
            self.LoadRes(-1)
        else:
            self.LoadRes(1)

    def onChangeHeadResTab2(self, logicalIndex):
        if logicalIndex == 0:
            self.LoadRes(-2)
        else:
            self.LoadRes(2)

    def LoadResTour(self, nQ):
        ResInTour = cur.execute(f"""
                                            SELECT id_table, point, question_number FROM Question
                                            WHERE id_round = {self.curRound}
                                            ORDER BY id_table
                                            """).fetchall()
        ResInTourInTable = [[0 for g in range(nQ + 2)] for _ in range(nTeam)]
        for j in range(nTeam):
            ResInTourInTable[j][0] = j + 1
        for j in range(len(ResInTour)):
            ResInTourInTable[ResInTour[j][0]][ResInTour[j][2] + 1] = ResInTour[j][1]
            ResInTourInTable[ResInTour[j][0]][nQ + 1] = sum(ResInTourInTable[ResInTour[j][0]][1:nQ + 1])
        ResInTourInTable.sort(key=lambda team: team[nQ + 1], reverse=True)
        for j in range(len(ResInTourInTable)):
            for k in range(len(ResInTourInTable[j])):
                ResInTourTab[self.curRound].setItem(j, k, QtWidgets.QTableWidgetItem(
                    str(ResInTourInTable[j][k]) if (k == 0) or (k == nQ + 1) else '+' if ResInTourInTable[j][
                                                                                             k] == 1 else '-'))

    def LoadRes(self, type):
        if type == 0:
            sort = "score DESC, name"
        elif type == -1:
            sort = "name"
        elif type == 1:
            sort = "score DESC"
        elif type == -2:
            sort = "name DESC"
        else:
            sort = "score"
        FinallRes = cur.execute(f"""
                                SELECT name, score FROM User
                                ORDER BY {sort}
                                """).fetchall()
        for i in range(len(FinallRes)):
            for j in range(len(FinallRes[i])):
                TabFinallRes.setItem(i, j, QtWidgets.QTableWidgetItem(str(FinallRes[i][j])))


if __name__ == "__main__":
    global con, cur
    con = sqlite3.connect('db')
    cur = con.cursor()
    con.commit()
    print(QtWidgets.QStyleFactory.keys())
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    myapp = MyWin()
    myapp.show()

    sys.exit(app.exec_())
