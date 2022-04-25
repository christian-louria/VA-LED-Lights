import time
import math
import requests
import threading
from datetime import datetime
import boardClass
import json
import globe
import config

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core import legacy
from luma.led_matrix.device import max7219
from luma.core.legacy.font import proportional, TINY_FONT

class GameInfo:
    home = 'XXX'
    away = 'XXX'
    homeScore = 'X'
    awayScore = 'X'
    clock = '0'
    
    def changeAttr(self, attr, val):
        setattr(self, attr, val)
    
class TempInfo:
    temp = "X"
    high = "X"
    low = "X"
    
    def changeAttr(self, attr, val):
        setattr(self, attr, val)

gameInfo = GameInfo()
tempInfo = TempInfo()

def getDotMatrix():
    return {"custom": globe.dotMatrix.custom, "boards" : globe.dotMatrix.boards}


def addDot(dot):
    print(dot)
    return

def createBoard(boardInfo):    
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=boardInfo.cascaded, block_orientation=boardInfo.block_orientation, rotate=boardInfo.rotate, blocks_arranged_in_reverse_order=boardInfo.blocks_arranged_in_reverse_order)
    virtual = viewport(device, width=boardInfo.viewportWidth, height=boardInfo.viewportHeight)
    
    board = boardClass.Board(device, virtual)
    return board


def setTeam(draw):
    dotMatrix = globe.dotMatrix
    while True:
        showScore = 'scoreboard' in dotMatrix.boards
        showClock = 'scoreClock' in dotMatrix.boards
        if showScore or showClock:
            r = requests.get('http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard')

            if r.status_code == 200:
                js = r.json()
                events = js['events']
                
                mainEvent = {}
                for event in events:
                    if config.team in event['name']:
                        mainEvent = event
                        break
                
                if mainEvent == {}:
                    mainEvent = events[0]
                        
                competition = mainEvent['competitions'][0]
                for team in competition['competitors']:
                    teamInfo = team['team']
                    if team['homeAway'] == 'home':
                        gameInfo.changeAttr('home', teamInfo['abbreviation'])
                        gameInfo.changeAttr('homeScore', team['score'])
                    else:
                        gameInfo.changeAttr('away', teamInfo['abbreviation'])
                        gameInfo.changeAttr('awayScore', team['score'])
                        
                gameInfo.changeAttr('clock', str(competition['status']['displayClock']))

            else:
                return
            time.sleep(30)
        time.sleep(1)


def showScoreClock(draw, boardNumber):
    global gameInfo
    xOffset = boardNumber * 32

    legacy.text(draw, (xOffset + 1, 0), gameInfo.clock, fill="white", font=proportional(TINY_FONT))

def showScoreboard(draw, boardNumber):
    global gameInfo
    xOffset = boardNumber * 32
    
    legacy.text(draw, (xOffset, 0), gameInfo.home, fill="white", font=proportional(TINY_FONT))
    legacy.text(draw, (xOffset + 12, 0), gameInfo.homeScore, fill="white", font=proportional(TINY_FONT))
    draw.line([(xOffset, 7), (xOffset + 10, 7)], fill="white")
    
    legacy.text(draw, (xOffset + 17, 0), gameInfo.away, fill="white", font=proportional(TINY_FONT))
    legacy.text(draw, (xOffset + 29, 0), gameInfo.awayScore, fill="white", font=proportional(TINY_FONT))
    draw.line([(xOffset + 17, 7), (xOffset + 27, 7)], fill="white")
    
def setWeather(draw):
    dotMatrix = globe.dotMatrix
    while True:
        if 'weather' in dotMatrix.boards:
            r = requests.get('https://api.openweathermap.org/data/2.5/forecast?zip=14611&appid=' + config.weatherApiKey + '&units=imperial')
            global tempInfo

            if r.status_code == 200:
                js = r.json()
                weatherJs = js['list']
                newHigh = float('-inf')
                newLow = float('inf')
                newTemp = 0
                for i in range(8):
                    tempTemp = weatherJs[i]['main']['temp']
                    if i == 0:
                        newTemp = tempTemp
                    if tempTemp > newHigh:
                        newHigh = tempTemp
                    if tempTemp < newLow:
                        newLow = tempTemp
                
                tempInfo.changeAttr('low', str(math.trunc(newLow)))
                tempInfo.changeAttr('high', str(math.trunc(newHigh)))
                tempInfo.changeAttr('temp', str(math.trunc(newTemp)))
            else:
                low = "X"
                high = "X"
                temp = "X"
            time.sleep(900)
        time.sleep(1)

def showWeather(draw, boardNumber):
    global tempInfo
    
    xOffset = boardNumber * 32
    
    legacy.text(draw, (xOffset, 0), tempInfo.temp, fill="white", font=proportional(TINY_FONT))
    draw.line([(xOffset + 9, 1), (xOffset + 9, 6)], fill="white")
    draw.line([(xOffset + 8, 2), (xOffset + 10, 2)], fill="white")
    legacy.text(draw, (xOffset + 12, 0), tempInfo.high, fill="white", font=proportional(TINY_FONT))
    draw.line([(xOffset + 21, 1), (xOffset + 21, 6)], fill="white")
    draw.line([(xOffset + 20, 5), (xOffset + 22, 5)], fill="white")
    legacy.text(draw, (xOffset + 24, 0), tempInfo.low, fill="white", font=proportional(TINY_FONT))

def changeMode(boardNumber, newMode):
    globe.dotMatrix.changeMode(boardNumber, newMode)
    
def showTime(draw, boardNumber):
    xOffset = boardNumber * 32

    now = datetime.now()

    legacy.text(draw, (xOffset, 0), now.strftime("%I"), fill="white", font=proportional(TINY_FONT))
    legacy.text(draw, (xOffset + 12, 0), now.strftime("%M"), fill="white", font=proportional(TINY_FONT))
    legacy.text(draw, (xOffset + 24, 0), now.strftime("%S"), fill="white", font=proportional(TINY_FONT))
    draw.line([(xOffset + 1, 7), (xOffset + 5, 7)], fill="white")
    draw.line([(xOffset + 13, 7), (xOffset + 17, 7)], fill="white")
    draw.line([(xOffset + 25, 7), (xOffset + 29, 7)], fill="white")

# def drawAmogiAt(x, y, draw):
#     draw.line([(x, y), (x + 2, y)], fill="white")
#     draw.line([(x + 2,  y + 1), (x + 3, y + 1)], fill="white")
#     draw.line([(x, y + 2), (x + 3, y + 2)], fill="white")
#     draw.line([(x, y + 3), (x + 3, y + 3)], fill="white")
#     draw.point([(x, y + 4), (x + 2, y + 4)], fill="white")

# def fillAmogi(boardNumber, draw):
#     xPos = (boardNumber * 32) + 1
#     for i in range(6):
#         drawAmogiAt(xPos, 1, draw)
#         xPos = xPos + 5

def renderBoard(board):
    now = datetime.now()
    print("rendering board at " + now.strftime("%I %M %S"))
       
    device = board.device
    virtual = board.virtual

    # requestThread = threading.Thread(target=setWeather, args=(-1,))
    # requestThread.start()
    sportsRequestThread = threading.Thread(target=setTeam, args=(-1,))
    sportsRequestThread.start()
    
    weatherRequestThread = threading.Thread(target=setWeather, args=(-1,))
    weatherRequestThread.start()
    
    dotMatrix = globe.dotMatrix
    
    device.contrast(5)
    while True:
        with canvas(virtual) as draw:
            for boardIndex in range(len(dotMatrix.boards)):
                boardInfo = dotMatrix.boards[boardIndex]
                if boardInfo == 'weather':
                    showWeather(draw, boardIndex)
                elif boardInfo == 'time':
                    showTime(draw, boardIndex)
                elif boardInfo == 'scoreboard':
                    showScoreboard(draw, boardIndex)
                elif boardInfo == 'scoreClock':
                    showScoreClock(draw, boardIndex)

        time.sleep(1)



if __name__ == "__main__":
    renderBoard()
