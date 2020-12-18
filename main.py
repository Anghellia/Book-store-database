import sys
from PyQt5 import QtWidgets
from gui import ConnectWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ConnectWindow()
    sys.exit(app.exec_())