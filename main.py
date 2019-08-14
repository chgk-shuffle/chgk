import sys
from ui.test import *
from PyQt5 import QtCore, QtGui, QtWidgets
import tour

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        tours = [tour.Tour(12, 3), tour.Tour(12, 2), tour.Tour(12, 6)]
        self.ui.setupUi(self, tours)






if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())