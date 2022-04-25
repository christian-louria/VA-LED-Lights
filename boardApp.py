# Christian Louria
# VA LED Lights Allows you to control and customize GeeekPi MAX7219 8 x 32
# Dot Matrix LED Lights from your phone.

# To start, make sure you have GeeekPi MAX7219 lights and download the
# Raspberry Pi python code off of my GitHub (link here). Once the python
# code is set up. input the IP Address of your Raspberry Pi and use the
# custom features present in the app.

import time
import socket
import board
import boardClass
import threading
import json
import globe


# import both
# import weather
# import os

HOST = '192.168.1.26'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    print("Listening for connections")
    
    n = 0
    while True:
        try:
            sock.bind((HOST, PORT))
            break
        except:
            print("elapsed time: "  + str(n))
            n += 1
            time.sleep(1)
        
    sock.listen()

    boardInfo = boardClass.BoardInfo()
    myBoard = board.createBoard(boardInfo)

    boardThread = threading.Thread(target=board.renderBoard, args=(myBoard,))
    boardThread.start()
    
    stop = threading.Event()


    # never close socket
    while True:
        
        print("Searching for connection")
        conn, addr = sock.accept()
        print("Connected")
        with conn:
            # stay connected after you sendall back
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    # decode json
                    dataList = data.splitlines()
                    for dataObj in dataList:
                        jsonObj = dataObj.decode('utf8')
                        loadedJson = json.loads(jsonObj)

                        # color / weather
                        mode = loadedJson['mode']

                        if mode == 'isAlive':
                            mb = board.getDotMatrix()
                            conn.sendall(json.dumps(mb, indent=2).encode('utf-8'))
                        elif mode == 'close':
                            conn.sendall(data)
                            conn.close()
                            # sock.shutdown(socket.SHUT_RDWR)
                            break
                        elif mode == 'custom':
                            dataL = loadedJson['data']
                            boardNumber = dataL['board']
                            newMode = dataL['mode']
                            board.changeMode(boardNumber, newMode)
                            conn.sendall(data)
                        elif mode == 'addDot':
                            board.addDot(jsonObj)
                            conn.sendall(data)

                        # if dataType == 'weather':
                        #     weather.handleWeather(conn, dataObj)

                except Exception as e:
                    print(e)
                    try:
                        conn.sendall(data)
                    except:
                        break
                    