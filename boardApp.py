# Christian Louria

import time
import socket
import board
import boardClass
import threading
import json
import globe
import config


# import both
# import weather
# import os

HOST = '192.168.1.26'
PORT = config.port

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
                    