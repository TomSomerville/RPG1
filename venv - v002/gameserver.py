import socket
from _thread import *
import sys
import pickle
import pprint
import sqlite3
import time


server = "0.0.0.0"
port = 1336
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def verify_received(uid, usn, token):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    record = c.execute("SELECT * FROM accounts WHERE uid=?", (uid,)).fetchone()
    if str(uid) == str(record[0]) and str(usn) == str(record[1]) and str(token) == str(record[4]):
        return True
    else:
        return False
    conn.close()

def update_coordinates(uid, x, y):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE players SET x = ?, y= ? WHERE uid = ?",(x, y, uid,))
        conn.commit()
        players = c.execute("SELECT * FROM players WHERE map_id=? and auth=1 and uid!=?", ("1",uid,)).fetchall()
        return players
        conn.close()

    except sqlite3.Error as e:
        return e

def update_connection_status(uid,auth):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE players SET auth=? WHERE uid = ?",(auth, uid,))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        return e

def threaded_client(conn):
    conn.send(b'Connected to server')
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            reply = "Received Data"
            print("received Data is: ", data)
            update_connection_status(data[0], "1")
            if not data:
                print("Disconnected", conn.getpeername())
                break
            else:
                print("Received Data From: ", conn.getpeername())
                verified = verify_received(data[0], data[1], data[2])
                if verified ==  True:
                    players = update_coordinates(data[0], data[3], data[4])
                    conn.sendall(pickle.dumps(players))
                else:
                    conn.sendall(str.encode("Not Verified"))


        except:
            break
    update_connection_status(data[0], "0")
    print("Connection Closed: ", conn.getpeername())
    conn.close()


try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen()
print("Server Started")

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))
