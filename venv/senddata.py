import socket
import pickle
import time

def connect_server():
    global s
    HOST = "shittyrunescape.thomassomerville.com"
    PORT = 1336
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    response = s.recv(1024)

def close_server():
    s.close()

def send_data(auth, data):
    rawdata = auth,data
    send = pickle.dumps(rawdata)
    s.sendall(send)
    response = s.recv(1024)
    return response

#connect_server()

#uid = "1"
#username = "Beached"
#token = '3293853d4a0356f573ce3e870bf055e4707569857f9981f7f78e44ba95688e6e'

#authdata = uid,username,token
#auth = pickle.dumps(authdata)

#rawdata = "get_players", "1"
#data = pickle.dumps(rawdata)
#while True:
#    print(pickle.loads(send_data(auth,data)))
#    time.sleep(5)