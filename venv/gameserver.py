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

def update_connection_status(uid,auth):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE players SET auth=? WHERE uid = ?",(auth, uid,))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        return e

def update_coordinates(uid, x, y):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE players SET x = ?, y= ? WHERE uid = ?",(x, y, uid,))
        conn.commit()
        return "Position Updated"
        conn.close()

    except sqlite3.Error as e:
        return e

def get_players(uid, mapid):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    try:
        players = c.execute("SELECT * FROM players WHERE map_id=? and auth=1 and uid!=?", ("1", uid,)).fetchall()
        return players
        conn.close()

    except sqlite3.Error as e:
        return e

def get_map_data(mapid):
    table = "map_"+str(mapid)
    conn = sqlite3.connect('maps.db')
    c = conn.cursor()
    query = 'SELECT * FROM {}'.format(table)
    results = c.execute(query).fetchall()
    return results

def process_data(auth,data):
    if data[0] == "get_map_data":
        reply = get_map_data(data[1])
        return reply
    elif data[0] == "update_coordinates":
        reply = update_coordinates(auth[0],data[1],data[2])
        print(reply)
        return reply
    elif data[0] == "get_players":
        reply = get_players(auth[0], data[1])
        return reply
    elif data[0] == "FUTURE":
        pass
    else:
        return("Unknown Command")

def threaded_client(conn):
    conn.send(b'Connected to server')
    reply = ""

    while True:
        try:
            received = pickle.loads(conn.recv(2048))
            auth = pickle.loads(received[0])
            data = pickle.loads(received[1])
            verified = verify_received(auth[0],auth[1],auth[2])
            if not data:
                print("Disconnected", conn.getpeername())
                break
            else:
                if verified:
                    update_connection_status(auth[0],"1")
                    print("Received Data: ",received,"\n         From: ", conn.getpeername())
                    reply = process_data(auth,data)
                    print("Sending: ", reply)
                    conn.sendall(pickle.dumps(reply))
                else:
                    conn.sendall(str.encode("Not Verified"))
        except:
            break
    update_connection_status(auth[0], "0")
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
