import sys
from PyQt5 import QtCore, QtWidgets
from main_window import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(None)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
