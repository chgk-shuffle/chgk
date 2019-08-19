import sqlite3
import math

from PyQt5 import QtWidgets

from ui.settings import Ui_MainWindow
import sys


class SettingsWindows(QtWidgets.QMainWindow):

    def save(self):
        cur.execute("DELETE FROM User")
        cur.execute("DELETE FROM Team_size")
        cur.execute("DELETE FROM Team")
        cur.execute("DELETE FROM Round")
        cur.execute("DELETE FROM Question")
        con.commit()
        round_one_start = self.ui.lineEdit.text()
        round_one_end = self.ui.lineEdit_2.text()
        round_two_start = self.ui.lineEdit_3.text()
        round_two_end = self.ui.lineEdit_4.text()
        round_three_start = self.ui.lineEdit_5.text()
        round_three_end = self.ui.lineEdit_6.text()
        round_four_start = self.ui.lineEdit_7.text()
        round_four_end = self.ui.lineEdit_8.text()
        round_five_start = self.ui.lineEdit_9.text()
        round_five_end = self.ui.lineEdit_10.text()
        round_six_start = self.ui.lineEdit_11.text()
        round_six_end = self.ui.lineEdit_12.text()
        round_seven_start = self.ui.lineEdit_13.text()
        round_seven_end = self.ui.lineEdit_14.text()
        round_eight_start = self.ui.lineEdit_15.text()
        round_eight_end = self.ui.lineEdit_16.text()
        names = (self.ui.textEditParticipants.toPlainText()).split('\n')
#        print(names)
        size = int(self.ui.lineEditNumParicipants.text())
#        print(size)
        combo_box = self.ui.comboBox.currentText()
        combo_box_2 = self.ui.comboBox_2.currentText()
        combo_box_3 = self.ui.comboBox_3.currentText()
        combo_box_4 = self.ui.comboBox_4.currentText()
        combo_box_5 = self.ui.comboBox_5.currentText()
        combo_box_6 = self.ui.comboBox_6.currentText()
        combo_box_7 = self.ui.comboBox_7.currentText()
        combo_box_8 = self.ui.comboBox_8.currentText()
        start = [round_one_start, round_two_start, round_three_start, round_four_start,
                 round_five_start, round_six_start, round_seven_start, round_eight_start]
        end = [round_one_end, round_two_end, round_three_end, round_four_end,
               round_five_end, round_six_end, round_seven_end, round_eight_end]
        boxes = [combo_box, combo_box_2, combo_box_3, combo_box_4, combo_box_5,
                 combo_box_6, combo_box_7, combo_box_8]

        return names, size, start, end, boxes

    def save_settings(self, names=None, size=None, start=None, end=None, boxes=None):
        names = None
        if names is None:
            names, size, start, end, boxes = self.save()

        for name in names:
            q = f"INSERT INTO User (name, score, level) VALUES ('{name}', 0, 0);"
            cur.execute(q)
        rounds_cnt = 0
        for i in range(8):
            if not start[i] + end[i]:
                break
            a = int(start[i])
            b = int(end[i])
            c = boxes[i]
            if 'Чгк' in c:
                type = 1
            else:
                type = 2
            q = f"INSERT INTO Round (start, end, type) VALUES ({a}, {b}, {type});"
            cur.execute(q)
            rounds_cnt += 1
        cur.execute(f"INSERT INTO Team_size (id) VALUES ({size});")
        for tabel_id in range(0, math.ceil(len(names) / size)):
            for round_id in range(0, rounds_cnt):
                start_round = int(start[round_id])
                end_round = int(end[round_id])
                for quest_num in range(start_round - 1, end_round):
                    cur.execute(
                        f"INSERT INTO Question (id_table, id_round, question_number, point) VALUES ({tabel_id}, {round_id}, {quest_num}, 0);")
        con.commit()




    def __init__(self):
        super(SettingsWindows, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.save_settings)


if __name__ == "__main__":
    global con, cur
    con = sqlite3.connect('db')
    cur = con.cursor()
    con.commit()

    app = QtWidgets.QApplication([])
    application = SettingsWindows()
    application.show()
    sys.exit(app.exec())
