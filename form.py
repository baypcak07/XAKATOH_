from PyQt5 import QtWidgets
import Main_form_design
import form_partn
import form_admin
import socket
import threading
from _thread import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class form_admin(QtWidgets.QMainWindow,form_admin.Ui_Administrator):
    def __init__(self,parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)

class form_partn(QtWidgets.QMainWindow,form_partn.Ui_Part):
    def __init__(self,parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)
class form(QtWidgets.QMainWindow, Main_form_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.PB_reg.clicked.connect(self.reg_form)
        self.PB_reg.clicked.connect(self.reciver)
        self.PB_enter.clicked.connect(self.enter)
        self.PB_enter.clicked.connect(self.reciver)


    def reg_form(self):
        print('reg')
        log_reg = self.LE_login_reg.text()
        pass_reg = self.LE_pass_reg.text()
        category_reg = self.CB_kat_reg.currentData()
        #print(str(log_reg) + str(pass_reg) + str(category_reg))
        #data_reg = reciver (self,log_reg,pass_reg,category_reg)
        global login,password,category,postgre_state
        login = log_reg
        password = pass_reg
        category = category_reg
        postgre_state = 0

    def enter(self):
        print('enter')
        log_enter = self.LE_login_enter.text()
        pass_enter = self.LE_pass_enter.text()
        category_enter = self.CB_kat_enter.currentData()
        global login,password,category,postgre_state
        login = log_enter
        password = pass_enter
        category = category_enter
        postgre_state = 1


    def reciver(self):

        ClientSocket = socket.socket()
        print('confirm')
        #host = socket.gethostbyname(socket.gethostname())
        host = 'localhost'
        port = 5001
        print('Ожидание соединения:',host,':',port)
        try:
            ClientSocket.connect((host,port))
            print('connect')
        except socket.error as e:
            print(str(e))

        global login,password,category,postgre_state
        Response = ClientSocket.recv(1024)

        Input = login +','+ password +',' + category + ',' + str(postgre_state)
        Input_e = str.encode(Input)
        ClientSocket.send(Input_e)
        print(Response.decode('utf-8'))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))
        if Response.decode('utf-8') == '0':
            print('Такой пользователь уже существует')
            self.LB_inf_string.setText('Такой пользователь уже существует')
        if Response.decode('utf-8') == '1':
            print('Пользователь зарегистрирован')
            self.LB_inf_string.setText('Пользователь зарегистрирован')
        ClientSocket.close()
        if Response.decode('utf-8') == '2':
            print('Вход')
            self.LB_inf_string.setText('Вход')
            if str(category) == 'admin':
                self.open_admin()
            if str(category) == 'part':
                self.open_part()
        ClientSocket.close()
        if Response.decode('utf-8') == '3':
            print('Неверные учетные данные')
            self.LB_inf_string.setText('Неверные учетные данные')
        ClientSocket.close()

    def open_admin(self):
        self.admin_win = form_admin(self)
        self.admin_win.show()

    def open_part(self):
        self.part_win = form_partn(self)
        self.part_win.show()




        #e1 = threading.Event()
        #t1 = threading.Thread(target=start_client, args=())
        #t1.start()
        #e1.set()
