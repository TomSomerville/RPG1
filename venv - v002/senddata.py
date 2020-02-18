import socket
import pickle

def connect_server():
    global s
    HOST = "shittyrunescape.thomassomerville.com"
    PORT = 1336
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    response = s.recv(1024)

def close_server():
    s.close()

def send_data(uid, usn, token, x, y):
    data = str(uid), str(usn), str(token), str(x), str(y)
    s.sendall(pickle.dumps(data))
    response = s.recv(1024)
    return response
