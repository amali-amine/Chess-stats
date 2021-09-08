# Chess-stats
Lichess stats of the top 200 players in each mode (09/08/2021).

## Overview

1. We extract the top 200 players in the 5 modes : | bullet | blitz | rapid | classical | ultraBullet |
2. We combine our player's traget : we get 858 unique player.
3. For each player, we save his records with the attributes : rating, number of victories, draws and loses for the 5 modes.

## The crash of the server

The server overloaded with many requests, crashes after receiving more than 200 requests.

So, there is two solutions.

1. Putting a clock, to pause the execution before the 200 request, and to deceive the server to not recognize that the requests is coming from a bot.
2. Changing the IP adress after certain iterations.

```
import requests

url = "http://lichess.com/"
page = requests.get(url, proxies={"http":"132.59.100.108:41311"})
```
