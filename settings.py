from PyQt5 import QtWidgets

from ui.settings import Ui_MainWindow
import sys


class SettingsWindows(QtWidgets.QMainWindow):
    def save_settings(self):
        print(self.ui.lineEdit.text())
        print(self.ui.lineEdit_2.text())
        print(self.ui.lineEdit_3.text())
        print(self.ui.lineEdit_4.text())
        print(self.ui.lineEdit_5.text())
        print(self.ui.lineEdit_6.text())
        print(self.ui.lineEdit_7.text())
        print(self.ui.lineEdit_8.text())
        print(self.ui.lineEdit_9.text())
        print(self.ui.lineEdit_10.text())
        print(self.ui.lineEdit_11.text())
        print(self.ui.lineEdit_12.text())
        print(self.ui.lineEdit_13.text())
        print(self.ui.lineEdit_15.text())
        print(self.ui.lineEdit_16.text())
        print(self.ui.textEditParticipants.toPlainText())
        print(self.ui.lineEditNumParicipants.text())
        print(self.ui.comboBox.currentText())
        print(self.ui.comboBox_2.currentText())
        print(self.ui.comboBox_3.currentText())
        print(self.ui.comboBox_4.currentText())
        print(self.ui.comboBox_5.currentText())
        print(self.ui.comboBox_6.currentText())
        print(self.ui.comboBox_7.currentText())
        print(self.ui.comboBox_8.currentText())

    def __init__(self):
        super(SettingsWindows, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.btnClicked)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = SettingsWindows()
    application.show()
    sys.exit(app.exec())
