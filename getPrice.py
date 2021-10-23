import requests
from bs4 import BeautifulSoup
import os
import sys
pathToScript = '/home/pi/gameprice/'

def getElementFromSite(site, elementName, elementAttributeName, elementAttribute):
    #print("Getting "+elementName+"/"+elementAttributeName+"/"+elementAttribute+" from site: "+site)
    r = requests.get(site, allow_redirects=True)
    f = open(pathToScript+'temp.html', 'w+')
    f.write(str(r.content))
    f.close()
    html = open(pathToScript+'temp.html', encoding="utf8", errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.find_all("span", {"class" : "numeric"}) #"game-price-current"})
    return lines

def printPrices(currentName, inputLines, siteurl):
    #print("inputLines: "+str(inputLines[:3]))
    if len(inputLines) > 3:
        inputLines = str(inputLines[:3]).replace("<span class=\"numeric\">","\n").replace("[","").replace("]","").replace("</span>","")
        inputLines = inputLines.split("\n")
        print("Game: "+currentName)
        print("<"+siteurl+">")
        #getImageUrl(siteurl)
        print("Official: "+str(inputLines[1].split("\\")[0])+"€")
        print("Keyshops: "+str(inputLines[2].split("\\")[0])+"€")
        print("Historical low: "+str(inputLines[3].split("\\")[0])+"€")
        getImageUrl(siteurl)
        return 0
    else:
        #print("Error - not enough lines:\n"+str(inputLines))
        return 1

def getSimilarName(inputName):
    #print("Game not found, searching for a similar game")
    gameName = inputName.replace("-","+")
    siteurl='https://gg.deals/games/?title='+gameName
    r = requests.get(siteurl, allow_redirects=True)
    f = open(pathToScript+'temp.html', 'w+')
    f.write(str(r.content))
    f.close()
    html = open(pathToScript+'temp.html', encoding="utf8", errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.find_all("a", {"class" : "title-inner"})#"game-info-title title"})
    lines = str(lines).replace("<div","\n")
    lines = lines.split(">")[1].split("<")[0]
    print("Exact game name not found, similar name: "+lines)
    return lines

def buildSiteUrl(inputName):
#    gameName=sys.argv[1]
    #print("Input name: "+str(inputName))
    gameName=str(inputName).replace(" ","-")
    gameName=str(gameName).replace(":","").replace("/"," ").replace("+","")
    siteurl='https://gg.deals/eu/region/switch/?return=%2Fgame%2F'+str(gameName)+'%2F'
    #print("Site URL: "+siteurl)
    return siteurl

def getImageUrl(siteurl):
    r = requests.get(siteurl, allow_redirects=True)
    lines = str(r.content).split("<")
    #print(siteurl)
    for line in lines:
        if "game-link-widget" in str(line):
            redirectLink = str(line).split('href="')[1].replace('">','')
            redirectRequest = requests.get(redirectLink, allow_redirects=True)
            targetUrl = str(redirectRequest.url)
            if "steampowered" in targetUrl:
                appId = str(targetUrl).split("/")[-2]
                print("https://steamcdn-a.akamaihd.net/steam/apps/"+appId+"/capsule_231x87.jpg")
                break;
        #if "steam" in str(line) or "Steam" in str(line):
        #    print(str(line))
        if "store.steampowered.com/app" in str(line):
            print(str(line))
            appId= str(line).split("/")[-2]
            print("https://steamcdn-a.akamaihd.net/steam/apps/"+appId+"/capsule_231x87.jpg")
            break;
        #else:
            #print(str(line))

#htmlname='site.html'
#print("------------")
inputName = str(sys.argv[1])
#print("X1:"+str(inputName))
siteurl = buildSiteUrl(str(inputName))
if printPrices(str(inputName), getElementFromSite(siteurl, "span", "class", "numeric"), siteurl) == 1:
    newName = getSimilarName(str(inputName))
    newUrl = buildSiteUrl(newName)
    #print("<"+newUrl+">")
    #print("newName: "+newName)
    printPrices(newName, getElementFromSite(newUrl, "span", "class", "numeric"), newUrl)

#print("\n\n===========================\n")

#html = open(htmlname, encoding="utf8", errors='ignore')
#soup = BeautifulSoup(html, 'html.parser')
#lines = soup.find_all("span", {"class" : "numeric"}) #"game-price-current"})
#if len(lines) > 3:
#    lines = str(lines[:3]).replace("<span class=\"numeric\">","\n").replace("[","").replace("]","").replace("</span>","")
#    lines = lines.split("\n")
#    print("Official stores: "+str(lines[1].split("\\")[0])+"€")
#    print("Keyshops: "+str(lines[2].split("\\")[0])+"€")
#    print("Historical low: "+str(lines[3].split("\\")[0])+"€")
#else:
#    print("Game not found, searching for a similar game")
#    gameName = gameName.replace("-","+")
#    siteurl='https://gg.deals/games/?title='+gameName
#    r = requests.get(siteurl, allow_redirects=True)
#    f = open(htmlname, 'w+')
#    f.write(str(r.content))
#    f.close()
#    html = open(htmlname, encoding="utf8", errors='ignore')
#    soup = BeautifulSoup(html, 'html.parser')
#    lines = soup.find_all("a", {"class" : "title-inner"})#"game-info-title title"})
#    lines = str(lines).replace("<div","\n")
#    lines = lines.split(">")[1].split("<")[0]
#    print(lines)

