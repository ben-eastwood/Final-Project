import requests
from bs4 import BeautifulSoup
import re
import csv

def ClearUrls():
    f = open('urls.csv', 'w+')
    f.close()

    f = open('eventUrl.csv', 'w+')
    f.close()

def GetUrls(urlToScrapeList):
    for url in urlToScrapeList:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        gameCodeList = []

        #Get Urls on Page
        for a in soup.find_all('a', href=True):
            parsedLink = a['href'].split('/')
            
            try:
                if(parsedLink[1].isdigit()):
                    gameCodeList.append(parsedLink[1])
            except:
                pass

        i = 0
        while i<len(gameCodeList):
            tempString = 'https://www.vlr.gg/'
            tempString += gameCodeList[i]

            with open('urls.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([tempString])
            i += 1

def GetEvents(eventUrl):

    response = requests.get(eventUrl)
    soup = BeautifulSoup(response.text, 'html.parser')

    eventCodeList = []

    #Get Urls on Page
    for a in soup.find_all('a', href=True):
        parsedLink = a['href'].split('/')
        
        try:
            if(parsedLink[1] == 'event'):
                eventCodeList.append(parsedLink[2])
        except:
            pass

    i = 0
    while(i < len(eventCodeList)):
        tempString = 'https://www.vlr.gg/event/'
        tempString += eventCodeList[i]

        with open('eventUrl.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([tempString])
        i += 1