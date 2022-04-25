# VA LED Lights

VA LED Lights Allows you to control and customize GeeekPi MAX7219 8 x 32 Dot Matrix LED Lights from your phone.


Download the app on the Appstore to control your lights "VA LED Lights"

## Config

- Read about configure your pi for the max7219 library here https://max7219.readthedocs.io/en/0.2.3/
- Change config.py.sample -> config.py
- Configure weatherApiKey from https://openweathermap.org/api
- Port forwarding needs to be configured on your router
- Team config is a EPL team name with proper capitalization

## Running 

python3.7 boardApp.py 

## Limitations

- Only one soccet conneciton can be made at a time
- Team scoreboard and stats only exist for a couple days around the game and will display a random game if the team score is not found
- You may have to change some of the parameters in creating the max7219 board in the createBoard function in board.py for the correct display

## Bugs/Issues

- Socket can get stuck hanging in rare cases and when starting up will take 2-3 minutes to actually start


