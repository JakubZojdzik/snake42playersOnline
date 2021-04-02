import socket
from _thread import *
import pickle
import time
from threading import Thread

server = "100.118.124.114"

port = 5556
started = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")
players = [1, 1]
currentPlayer = -1
p1accept = False
p2accept = False
food = [0, 0]


def countdown():
    global started
    while started >= 0:
        started -= 1
        time.sleep(1)


countThread = Thread(target=countdown)


def threaded_client(conn, player):
    global players
    global started
    global p1accept
    global p2accept
    global food
    global started
    global currentPlayer
    conn.send(pickle.dumps(player))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                if data == "status":
                    reply = started
                else:
                    if data == "restart":
                        players[0] = 1
                        players[1] = 1
                        if player == 0:
                            p1accept = True
                        else:
                            p2accept = True
                    elif data == "both":
                        reply = (p1accept and p2accept)

                    elif data == "wait":
                        p1accept = False
                        p2accept = False
                    elif data == "get_food":
                        reply = food
                    elif type(data) == list:
                        food = data
                    else:
                        players[player] = data
                        if player == 1:
                            reply = players[0]
                        else:
                            reply = players[1]

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")

    started = 3
    players = [1, 1]
    currentPlayer -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    if currentPlayer == -1:
        print("Looking for oponentes...")
        currentPlayer = 0
    else:
        currentPlayer = 1
        start_new_thread(countdown, ())
        #if not countThread.is_alive():
        #    countThread.start()
        print("Starting game...")

    start_new_thread(threaded_client, (conn, currentPlayer))
