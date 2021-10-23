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
    #lines = soup.find_all("span", {"class" : "numeric"}) #"game-price-current"})
    lines = soup.find_all("a", {"class" : "game-price-anchor-link"})
    #print("-------------")
    #print(str(site))
    #print(str(lines))
    #print("=============")
    return lines

def printPrices(currentName, inputLines, siteurl):
    #print("---inputLines: "+str(inputLines[:3]))
    if len(inputLines) > 0:
        #print("RAW:\n\n"+str(inputLines)+"\n\n##########################################\n\n")
        inputLines = str(inputLines[:10]).replace('</a>','\n')#.replace('</span></a>','\n').replace("<span class=\"numeric\">","\n").replace("[","").replace("]","").replace("</span>","")
        inputLines = inputLines.split("\n")
        #Get official price
        officialPrice = "-"
        foundOfficial = 0
        keyshopPrice = "-"
        historicalLow = "1000000000"
        #Find first line with price
        #print(str(inputLines)
        #print("//////////////////////////////////////////////////////////////")
        x=0
        ofiNotFound = 1
        keyNotFound = 1
        hisNotFound = 2
        for line in inputLines:
            if "empty" in str(line) and "official" in str(line) and ofiNotFound == 1:
                officialPrice = "Unavailable"
                ofiNotFound = 0
            elif "empty" in str(line) and "keyshop" in str(line) and keyNotFound == 1:
                keyshopPrice = "Unavailable"
                keyNotFound = 0
            elif "empty" in str(line) and "histor" in str(line) and hisNotFound == 1:
                historicalLow = "Unavailable"
                #hisNotFound = 0
            elif "official" in str(line) and "numeric" in str(line) and ofiNotFound == 1:
                #Cut off everything before 'numerical' and after next SLASH
                #print("OFII:"+str(line))
                officialPrice = str(line).split('<span class="numeric">')[1].split("\\")[0]
                ofiNotFound = 0
            elif "keyshop" in str(line) and "numeric" in str(line) and keyNotFound == 1:
                #print("KS::"+str(line))
                keyshopPrice = str(line).split('<span class="numeric">')[1].split("\\")[0]
                keyNotFound = 0
            elif "histor" in str(line) and "numeric" in str(line) and hisNotFound != 0:
                #print("HISTOR:"+str(line))
                newCandidate = str(line).split('<span class="numeric">')[1].split("\\")[0]
                if float(newCandidate.replace(",",".").replace("~","")) < float(historicalLow.replace(",",".").replace("~","")):
                    historicalLow = newCandidate
                hisNotFound -= 1
            x+=1
        #print("-------------------------------------")
        
        #
        #if "UNAVAILABLE" in inputLines[0]:
        #    print("X100:Found UNAVAILABLE IN:\n"+inputLines[0]+"\n")
        #    officialPrice = "n/a"
        #else:
        #    print("X101: Not found UNAVAILABLE IN:\n"+inputLines[0]+"\n")
        #    officialPrice = inputLines[1].split("\\")[0]+"€"
        #    foundOfficial = 1
        #If found official price
        #if foundOfficial == 1:
        #    print("\nX200:Found Official = 1; keyshopSearchIndex = 2;\n")
        #    keyshopSearchIndex = 2 
        #else:
        #    print("\nX201:Found Official = 0; keyshopSearchIndex = 1;\n")
        #    keyshopSearchIndex = 2
#
        #if "UNAVAILABLE" in inputLines[keyshopSearchIndex]:
        #    print("\nX300:Found UNAVAILABLE in inputLines["+str(keyshopSearchIndex)+"]:\n"+str(inputLines[keyshopSearchIndex]))
        #    keyshopPrice = "n/a"
        #else:
        #    print("\nX301:Not found UNAVAILABLE in inputLines["+str(keyshopSearchIndex)+"]:"+str(inputLines[keyshopSearchIndex]))
        #    keyshopPrice = str(inputLines[keyshopSearchIndex].split("\\")[0])+"€"

        #print("X400: OFI:\n"+officialPrice+"\n\n")
        #print("X401: KEYSH:\n"+keyshopPrice+"\n\n")
        #print("X402: HIST:\n"+historicalLow+"\n\n")
        #print("=1=1=1=1=1=1==1=1=1=1==1=1==1=1=1=1")
        #print(inputLines[0])
        #print("=2=2==2=2=2=2=2=2==2=2=2=2==2=2==2=2")
        #print(inputLines[1])
        #print("=3=3=3=3==3=3=3=3=3==3=3=3=3==3=3=3=")
        #if len(inputLines) > 2:
        #    print(inputLines[2])
        #print("=4=4=4==4=4=4=4=4=4==4=4=4==4=4==4=4=")
        print("Game: "+currentName)
        print("<"+siteurl+">")
        if officialPrice != "Unavailable":
            officialPrice += "€"
        if keyshopPrice != "Unavailable":
            keyshopPrice += "€"
        if historicalLow != "Unavailable":
            if float(historicalLow.replace(",",".").replace("~","")) > 10000:
                historicalLow = "Unavailable"
        if historicalLow != "Unavailable":
            historicalLow += "€"
        print("Official: "+str(officialPrice))
        print("Keyshops: "+str(keyshopPrice))
        print("Historical low: "+str(historicalLow))
        #getImageUrl(siteurl)
        #if len(inputLines) > 1:
        #    print("Official: "+str(inputLines[1].split("\\")[0])+"€")
        #if len(inputLines) > 2:
        #    print("Keyshops: "+str(inputLines[2].split("\\")[0])+"€")
        #if len(inputLines) > 3:
        #    print("Historical low: "+str(inputLines[3].split("\\")[0])+"€")
        getImageUrl(siteurl)
        return 0
    else:
        #print(str(inputLines))
        #print("Error - not enough lines:\n"+str(inputLines))
        return 1

def getSimilarName(inputName):
    #print("Game not found, searching for a similar game")
    gameName = inputName.replace(" - ","-").replace("---","-").replace("-","+")
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
    gameName=str(inputName).replace(" - ","-")
    #print("Input name2: "+str(inputName))
    gameName=str(inputName).replace(" ","-").replace("---","-")
    gameName=str(gameName).replace(":","").replace("/","").replace("+","")
    #print("Game name: "+str(gameName))
    siteurl='https://gg.deals/eu/region/switch/?return=%2Fgame%2F'+str(gameName)+'%2F&showKeyshops=1'
    #print("Site URL: "+siteurl)
    return siteurl

def getImageUrl(siteurl):
    r = requests.get(siteurl, allow_redirects=True)
    lines = str(r.content).split("<")
    #print(siteurl)
    for line in lines:
        if "image-game" in str(line):
            print(str(line).split("src=")[1].split(" alt=")[0].replace('"',''))
            break;
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
            #print(str(line))
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

