import psycopg2
import socket
import threading
from _thread import *
import sys

try:
    conn = psycopg2.connect(dbname='test_db', user='postgres', password='Perkele1', host='localhost')
    print('Успешное подключение к БД')
except:
    print('Can`t establish connection to database')

print('Введите адрес на котором будет запущен сервер')
host = input()
print('Введите порт на котором будет запущен сервер')
port = int(input())
print(host,':',port)
#print('Введите количество участников')
#user_num = int(input())
user_num = 1000
ServerSocket = socket.socket()
global ThreadCount
ThreadCount = 0
try:
    ServerSocket.bind((str(host),int(port)))
except socket.error as e:
    print(str(e))
ServerSocket.listen(int(user_num))


def threaded_client(connection):
    connection.send(str.encode('соединение с сервером установлено'))
    data = connection.recv(2048)
    #reply = 'Ответ сервера: ' + data.decode('utf-8')
    client_data = data.decode('utf-8')
    print(client_data)
    client_data_e = client_data.split(',')
    print(client_data_e[3])
    #if client_data_e[3] == 0:
    reply = reg_bd(client_data_e[0],client_data_e[1],client_data_e[2])
    print('reply',reply)
    #if client_data_e[3] == 1:
    reply2 = enter_db(client_data_e[0],client_data_e[1])
    print('reply2',reply2)
    flag = str(client_data_e[3])
    print('flag',flag)
    if flag == '0':
        print('event1',reply)
        connection.sendall(str.encode(str(reply)))
    if flag == '1':
        print('event2',reply2)
        connection.sendall(str.encode(str(reply2)))
    connection.close()


def start_server():
    print('сервер запущен')
    global ThreadCount
    while True:
        Client, address = ServerSocket.accept()
        print('Соединение: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('число потоков: ' + str(ThreadCount))
    ServerSocket.close()

def reg_bd(login,password,category):
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT * FROM users WHERE username = '" + str(login) + "')")
    db_out = cur.fetchall()
    #print(db_out)
    db_out1 = str(db_out[0])
    db_out2 = db_out1[1:(len(db_out1)-2)]
    #print(str(db_out2))
    #print(login)
    if db_out2 == 'True':
        return(0)
    else:
        cur.execute("INSERT INTO users (username, password, category) VALUES (%s, %s, %s)",
                    (str(login), str(password), str(category)))
        conn.commit()
        return(1)

def enter_db(login,password):
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM users WHERE username = '" + str(login) + "'")
    db_out = cur.fetchall()
    print(db_out)
    db_out2 = db_out[0]
    print(db_out2)
    db_username = str(db_out2[0])
    db_password = str(db_out2[1])
    print('username',db_username)
    print('password',db_password)
    if db_username == login and db_password == password:
        return (2)
    else:
        return (3)

e1 = threading.Event()
t1 = threading.Thread(target=start_server, args=())
t1.start()
e1.set()
