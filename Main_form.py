import sys
from PyQt5 import QtWidgets
from form import form


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = form()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()