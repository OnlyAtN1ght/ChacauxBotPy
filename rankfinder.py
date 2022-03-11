import requests
from bs4 import BeautifulSoup
import sys


def rankbot_activation(username):
    try:
        name = "https://euw.op.gg/summoners/euw/" + username
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        source = requests.get(name, "lxml",headers=headers).text
        #print(source)
        soup = BeautifulSoup(source, "html.parser")
        lp = soup.find("span", {"class": "lp"}).text
        rank = soup.find("div", {"class": "tier-rank"}).text
        return rank + " "+  lp
        #print(str(rank).replace("\t", ""), str(lp).replace("\t", ""))
    except Exception as e:
        print(e)
        #print("There is no account of this name or the summoner is unranked")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass#print(rankbot_activation(sys.argv[1]))
    else:
        pass#print(rankbot_activation("OnlyAtN1ght"))

def draven():
    try:
        name = "https://euw.op.gg/summoners/euw/franciscoco" 
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        source = requests.get(name, "lxml",headers=headers).text
        soup = BeautifulSoup(source, "html.parser")

        winrate = soup.find("div", {"class": "css-44dt2d exxtup0"}).text
        print(winrate)
        played = soup.find("div", {"class": "count"}).text
        print(played)

        message = "Franciscoco on Draven : {winrate} in {played}".format(winrate=winrate,played=played)
        print(message)

    except Exception as e:
        print(e)
        #print("There is no account of this name or the summoner is unranked")

