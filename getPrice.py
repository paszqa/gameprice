import requests
from bs4 import BeautifulSoup
import os
import sys

gameName=sys.argv[1]
print("Game name: "+gameName)
gameName=gameName.replace(" ","-")
siteurl='https://gg.deals/eu/region/switch/?return=%2Fgame%2F'+gameName+'%2F'
htmlname='site.html'

r = requests.get(siteurl, allow_redirects=True)
f = open(htmlname, 'w+')
f.write(str(r.content))
f.close()

html = open(htmlname, encoding="utf8", errors='ignore')
soup = BeautifulSoup(html, 'html.parser')
lines = soup.find_all("span", {"class" : "numeric"}) #"game-price-current"})
if len(lines) > 3:
    lines = str(lines[:3]).replace("<span class=\"numeric\">","\n").replace("[","").replace("]","").replace("</span>","")
    lines = lines.split("\n")
    print("Official stores: "+str(lines[1].split("\\")[0])+"€")
    print("Keyshops: "+str(lines[2].split("\\")[0])+"€")
    print("Historical low: "+str(lines[3].split("\\")[0])+"€")
else:
    print("Game not found, searching for a similar game")
    gameName = gameName.replace("-","+")
    siteurl='https://gg.deals/games/?title='+gameName
    r = requests.get(siteurl, allow_redirects=True)
    f = open(htmlname, 'w+')
    f.write(str(r.content))
    f.close()
    html = open(htmlname, encoding="utf8", errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.find_all("a", {"class" : "title-inner"})#"game-info-title title"})
    lines = str(lines).replace("<div","\n")
    lines = lines.split(">")[1].split("<")[0]
    print(lines)

