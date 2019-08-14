from PyQt5 import QtWidgets

from ui.settings import Ui_MainWindow
import sys


class SettingsWindows(QtWidgets.QMainWindow):
    def btnClicked(self):
        print(123)
        print(self.ui.textEdit.toPlainText())

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
