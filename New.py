from PyQt5 import QtWidgets

# Импортируем наш шаблон.
from ui.settings import Ui_MainWindow
import sys


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton.clicked.connect(self.btnClicked)

    def btnClicked(self):
        self.ui.label.setText("Настройки")
        # Если не использовать, то часть текста исчезнет.
        self.ui.label.adjustSize()
        print((123,))
        print(self.textEdit.toPlainText())
        print((456,))


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())