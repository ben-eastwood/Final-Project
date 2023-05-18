import requests
from bs4 import BeautifulSoup
import re
import csv

def CleanString(string):
    return re.sub(r'[^a-zA-Z0-9 -]', '', ' '.join(string.split()).strip())

def ClearCsv():
    f = open('match.csv', 'w+')
    f.close()

def GetMatchStats(url):
    urlCodes = url.split('/')
    matchCode = urlCodes[3]

    keepGoing = 1

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Get BoX (eg. Bo3, Bo5)
    boXDiv = soup.find('div', {'class': 'match-header-vs-note'})
    boXDiv = boXDiv.findNext('div', {'class': 'match-header-vs-note'})
    boXData = CleanString(boXDiv.text).split(" ")
    boXText = boXData[0]

    #Total Match Stats
    #Get Map
    mapText = 'All Maps'

    #Get Team Names
    teamNameDiv = soup.find('div', {'class': 'wf-title-med'})
    teamNameData = CleanString(teamNameDiv.text)
    team1NameText = teamNameData

    teamNameDiv = teamNameDiv.findNext('div', {'class': 'wf-title-med'})
    teamNameData = CleanString(teamNameDiv.text)
    team2NameText = teamNameData

    #Get Map Scores
    teamScoreDiv = soup.find('div', {'class': 'js-spoiler'})
    teamScoreData = CleanString(teamScoreDiv.text).split(" ")
    team1ScoreText = teamScoreData[0]
    team2ScoreText = teamScoreData[2]

    teamScoreTotal = [mapText, team1NameText, team1ScoreText, team2NameText, team2ScoreText, matchCode, boXText]

    with open('match.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(teamScoreTotal)

    try:
        #Overall Stats
        table = soup.find('div', {'class': 'vm-stats-game'})
        table = table.findNext('div', {'class': 'vm-stats-game'})
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                playerteam = CleanString(cells[0].text).split(" ")
                player, team = playerteam[0], playerteam[1]
                if(player == 'gob' and team == 'b'): # Fix for a player with a space in the name
                    player = 'gob-b'
                    team = playerteam[2]
                agents = []
                
                for img in row.find_all('img', alt=True):
                    agents.append(CleanString(img['alt']))

                ratings = CleanString(cells[2].text).split(" ")
                ratingOverall = ratings[0]
                acs = CleanString(cells[3].text).split(" ")
                acsOverall = acs[0]
                kills = CleanString(cells[4].text).split(" ")
                killsOverall = kills[0]
                deaths = CleanString(cells[5].text).split(" ")
                deathsOverall = deaths[1]
                assists = CleanString(cells[6].text).split(" ")
                assistsOverall = assists[0]
                kdDifference = CleanString(cells[7].text).split(" ")
                kdDifferenceOverall = kdDifference[0]
                kast = CleanString(cells[8].text).split(" ")
                kastOverall = kast[0]
                adr = CleanString(cells[9].text).split(" ")
                adrOverall= adr[0]
                hs = CleanString(cells[10].text).split(" ")
                hsOverall = hs[0]
                fk = CleanString(cells[11].text).split(" ")
                fkOverall = fk[0]
                fd = CleanString(cells[12].text).split(" ")
                fdOverall = fd[0]
                fkDifference = CleanString(cells[13].text).split(" ")
                fkDifferenceOverall = fkDifference[0]

                data = [player, team, agents, ratingOverall, acsOverall, killsOverall, deathsOverall, assistsOverall, kdDifferenceOverall, kastOverall, adrOverall, hsOverall, fkOverall, fdOverall, fkDifferenceOverall]
                with open('match.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
        with open('match.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow('-')
    except:
        #In case of forfeit get header to see which team won
        headerDiv = soup.find('div', {'class': 'match-header-vs-note'})
        headerData = CleanString(headerDiv.text)
        headerText = headerData

        with open('match.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([headerText])
        keepGoing = 0

    #Map 1 Stats
    if(keepGoing):
        try:
            #Get Map
            mapDiv = soup.find('div', {'class': 'map'})
            mapData = CleanString(mapDiv.text).split(" ")
            mapText = mapData[0]

            #Get Map Score
            teamScoreDiv = soup.find('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team1ScoreText = teamScoreData[0]

            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team2ScoreText = teamScoreData[0]

            # Get if Team1 is on Attack or Defence in first half
            roundsDiv = soup.find('div', {'class': 'vlr-rounds'})
            sideDiv = roundsDiv.find('div', {'class': 'vlr-rounds-row-col'})
            sideDiv = sideDiv.findNext('div', {'class': 'vlr-rounds-row-col'})
            team2 = False
            for div in sideDiv:
                if("rnd-sq mod-win mod-ct" in str(div)):
                    if(team2):
                        sideText = 'T'
                    else:
                        sideText = 'CT'
                elif("rnd-sq mod-win mod-t" in str(div)):
                    if(team2):
                        sideText = 'CT'
                    else:
                        sideText = 'T'
                elif("rnd-sq" in str(div)):
                    team2 = True

            team1StartingSide = sideText
            if(team1StartingSide == 'CT'):
                team2StartingSide = 'T'
            elif(team1StartingSide == 'T'):
                team2StartingSide = 'CT'
            else:
                team2StartingSide = 'NA'

            teamScoreMap = [mapText, team1NameText, team1ScoreText, team2NameText, team2ScoreText, team1StartingSide, team2StartingSide]

            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(teamScoreMap)

            #Stats
            table = soup.find('div', {'class': 'vm-stats-game'})
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    playerteam = CleanString(cells[0].text).split(" ")
                    player, team = playerteam[0], playerteam[1]
                    if(player == 'gob' and team == 'b'):
                        player = 'gob-b'
                        team = playerteam[2]
                    
                    for img in row.find_all('img', alt=True):
                        agent = CleanString(img['alt'])

                    ratings = CleanString(cells[2].text).split(" ")
                    ratingOverall = ratings[0]
                    acs = CleanString(cells[3].text).split(" ")
                    acsOverall = acs[0]
                    kills = CleanString(cells[4].text).split(" ")
                    killsOverall = kills[0]
                    deaths = CleanString(cells[5].text).split(" ")
                    deathsOverall = deaths[1]
                    assists = CleanString(cells[6].text).split(" ")
                    assistsOverall = assists[0]
                    kdDifference = CleanString(cells[7].text).split(" ")
                    kdDifferenceOverall = kdDifference[0]
                    kast = CleanString(cells[8].text).split(" ")
                    kastOverall  = kast[0]
                    adr = CleanString(cells[9].text).split(" ")
                    adrOverall = adr[0]
                    hs = CleanString(cells[10].text).split(" ")
                    hsOverall = hs[0]
                    fk = CleanString(cells[11].text).split(" ")
                    fkOverall = fk[0]
                    fd = CleanString(cells[12].text).split(" ")
                    fdOverall = fd[0]
                    fkDifference = CleanString(cells[13].text).split(" ")
                    fkDifferenceOverall = fkDifference[0]

                    data = [player, team, agent, ratingOverall, acsOverall, killsOverall, deathsOverall, assistsOverall, kdDifferenceOverall, kastOverall, adrOverall, hsOverall, fkOverall, fdOverall, fkDifferenceOverall]
                    with open('match.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow('-')
        except:
            keepGoing = 0

    #Map 2 Stats
    if(keepGoing):
        try:
            #Get Map
            mapDiv = mapDiv.findNext('div', {'class': 'map'})
            mapData = CleanString(mapDiv.text).split(" ")
            mapText = mapData[0]

            #Get Map Score
            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team1ScoreText = teamScoreData[0]

            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team2ScoreText = teamScoreData[0]

            # Get if Team1 is on Attack or Defence in first half
            roundsDiv = roundsDiv.findNext('div', {'class': 'vlr-rounds'})
            sideDiv = roundsDiv.find('div', {'class': 'vlr-rounds-row-col'})
            sideDiv = sideDiv.findNext('div', {'class': 'vlr-rounds-row-col'})
            team2 = False
            for div in sideDiv:
                if("rnd-sq mod-win mod-ct" in str(div)):
                    if(team2):
                        sideText = 'T'
                    else:
                        sideText = 'CT'
                elif("rnd-sq mod-win mod-t" in str(div)):
                    if(team2):
                        sideText = 'CT'
                    else:
                        sideText = 'T'
                elif("rnd-sq" in str(div)):
                    team2 = True

            team1StartingSide = sideText
            if(team1StartingSide == 'CT'):
                team2StartingSide = 'T'
            elif(team1StartingSide == 'T'):
                team2StartingSide = 'CT'
            else:
                team2StartingSide = 'NA'

            teamScoreMap = [mapText, team1NameText, team1ScoreText, team2NameText, team2ScoreText, team1StartingSide, team2StartingSide]

            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(teamScoreMap)

            #Stats
            table = table.findNext('div', {'class': 'vm-stats-game'})
            table = table.findNext('div', {'class': 'vm-stats-game'})
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    playerteam = CleanString(cells[0].text).split(" ")
                    player, team = playerteam[0], playerteam[1]
                    if(player == 'gob' and team == 'b'):
                        player = 'gob-b'
                        team = playerteam[2]
                    
                    for img in row.find_all('img', alt=True):
                        agent = CleanString(img['alt'])

                    ratings = CleanString(cells[2].text).split(" ")
                    ratingOverall = ratings[0]
                    acs = CleanString(cells[3].text).split(" ")
                    acsOverall = acs[0]
                    kills = CleanString(cells[4].text).split(" ")
                    killsOverall = kills[0]
                    deaths = CleanString(cells[5].text).split(" ")
                    deathsOverall = deaths[1]
                    assists = CleanString(cells[6].text).split(" ")
                    assistsOverall = assists[0]
                    kdDifference = CleanString(cells[7].text).split(" ")
                    kdDifferenceOverall = kdDifference[0]
                    kast = CleanString(cells[8].text).split(" ")
                    kastOverall = kast[0]
                    adr = CleanString(cells[9].text).split(" ")
                    adrOverall = adr[0]
                    hs = CleanString(cells[10].text).split(" ")
                    hsOverall = hs[0]
                    fk = CleanString(cells[11].text).split(" ")
                    fkOverall = fk[0]
                    fd = CleanString(cells[12].text).split(" ")
                    fdOverall = fd[0]
                    fkDifference = CleanString(cells[13].text).split(" ")
                    fkDifferenceOverall = fkDifference[0]

                    data = [player, team, agent, ratingOverall, acsOverall, killsOverall, deathsOverall, assistsOverall, kdDifferenceOverall, kastOverall, adrOverall, hsOverall, fkOverall, fdOverall, fkDifferenceOverall]
                    with open('match.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow('-')
        except:
            keepGoing = 0

    #Map 3 Stats
    if(keepGoing):
        try:
            #Get Map
            mapDiv = mapDiv.findNext('div', {'class': 'map'})
            mapData = CleanString(mapDiv.text).split(" ")
            mapText = mapData[0]

            #Get Map Score
            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team1ScoreText = teamScoreData[0]

            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team2ScoreText = teamScoreData[0]

            # Get if Team1 is on Attack or Defence in first half
            roundsDiv = roundsDiv.findNext('div', {'class': 'vlr-rounds'})
            sideDiv = roundsDiv.find('div', {'class': 'vlr-rounds-row-col'})
            sideDiv = sideDiv.findNext('div', {'class': 'vlr-rounds-row-col'})
            team2 = False
            for div in sideDiv:
                if("rnd-sq mod-win mod-ct" in str(div)):
                    if(team2):
                        sideText = 'T'
                    else:
                        sideText = 'CT'
                elif("rnd-sq mod-win mod-t" in str(div)):
                    if(team2):
                        sideText = 'CT'
                    else:
                        sideText = 'T'
                elif("rnd-sq" in str(div)):
                    team2 = True

            team1StartingSide = sideText
            if(team1StartingSide == 'CT'):
                team2StartingSide = 'T'
            elif(team1StartingSide == 'T'):
                team2StartingSide = 'CT'
            else:
                team2StartingSide = 'NA'

            teamScoreMap = [mapText, team1NameText, team1ScoreText, team2NameText, team2ScoreText, team1StartingSide, team2StartingSide]

            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(teamScoreMap)

            #Stats
            table = table.findNext('div', {'class': 'vm-stats-game'})
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    playerteam = CleanString(cells[0].text).split(" ")
                    player, team = playerteam[0], playerteam[1]
                    if(player == 'gob' and team == 'b'):
                        player = 'gob-b'
                        team = playerteam[2]
                    
                    for img in row.find_all('img', alt=True):
                        agent = CleanString(img['alt'])

                    ratings = CleanString(cells[2].text).split(" ")
                    ratingOverall = ratings[0]
                    acs = CleanString(cells[3].text).split(" ")
                    acsOverall = acs[0]
                    kills = CleanString(cells[4].text).split(" ")
                    killsOverall = kills[0]
                    deaths = CleanString(cells[5].text).split(" ")
                    deathsOverall = deaths[1]
                    assists = CleanString(cells[6].text).split(" ")
                    assistsOverall = assists[0]
                    kdDifference = CleanString(cells[7].text).split(" ")
                    kdDifferenceOverall = kdDifference[0]
                    kast = CleanString(cells[8].text).split(" ")
                    kastOverall = kast[0]
                    adr = CleanString(cells[9].text).split(" ")
                    adrOverall = adr[0]
                    hs = CleanString(cells[10].text).split(" ")
                    hsOverall = hs[0]
                    fk = CleanString(cells[11].text).split(" ")
                    fkOverall = fk[0]
                    fd = CleanString(cells[12].text).split(" ")
                    fdOverall = fd[0]
                    fkDifference = CleanString(cells[13].text).split(" ")
                    fkDifferenceOverall = fkDifference[0]

                    data = [player, team, agent, ratingOverall, acsOverall, killsOverall, deathsOverall, assistsOverall, kdDifferenceOverall, kastOverall, adrOverall, hsOverall, fkOverall, fdOverall, fkDifferenceOverall]
                    with open('match.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow('-')
        except:
            keepGoing = 0

    #Map 4 Stats
    if(keepGoing):
        try:
            #Get Map
            mapDiv = mapDiv.findNext('div', {'class': 'map'})
            mapData = CleanString(mapDiv.text).split(" ")
            mapText = mapData[0]

            #Get Map Score
            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team1ScoreText = teamScoreData[0]

            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team2ScoreText = teamScoreData[0]

            # Get if Team1 is on Attack or Defence in first half
            roundsDiv = roundsDiv.findNext('div', {'class': 'vlr-rounds'})
            sideDiv = roundsDiv.find('div', {'class': 'vlr-rounds-row-col'})
            sideDiv = sideDiv.findNext('div', {'class': 'vlr-rounds-row-col'})
            team2 = False
            for div in sideDiv:
                if("rnd-sq mod-win mod-ct" in str(div)):
                    if(team2):
                        sideText = 'T'
                    else:
                        sideText = 'CT'
                elif("rnd-sq mod-win mod-t" in str(div)):
                    if(team2):
                        sideText = 'CT'
                    else:
                        sideText = 'T'
                elif("rnd-sq" in str(div)):
                    team2 = True

            team1StartingSide = sideText
            if(team1StartingSide == 'CT'):
                team2StartingSide = 'T'
            elif(team1StartingSide == 'T'):
                team2StartingSide = 'CT'
            else:
                team2StartingSide = 'NA'

            teamScoreMap = [mapText, team1NameText, team1ScoreText, team2NameText, team2ScoreText, team1StartingSide, team2StartingSide]

            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(teamScoreMap)

            #Stats
            table = table.findNext('div', {'class': 'vm-stats-game'})
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    playerteam = CleanString(cells[0].text).split(" ")
                    player, team = playerteam[0], playerteam[1]
                    if(player == 'gob' and team == 'b'):
                        player = 'gob-b'
                        team = playerteam[2]
                    
                    for img in row.find_all('img', alt=True):
                        agent = CleanString(img['alt'])

                    ratings = CleanString(cells[2].text).split(" ")
                    ratingOverall = ratings[0]
                    acs = CleanString(cells[3].text).split(" ")
                    acsOverall = acs[0]
                    kills = CleanString(cells[4].text).split(" ")
                    killsOverall = kills[0]
                    deaths = CleanString(cells[5].text).split(" ")
                    deathsOverall = deaths[1]
                    assists = CleanString(cells[6].text).split(" ")
                    assistsOverall = assists[0]
                    kdDifference = CleanString(cells[7].text).split(" ")
                    kdDifferenceOverall = kdDifference[0]
                    kast = CleanString(cells[8].text).split(" ")
                    kastOverall = kast[0]
                    adr = CleanString(cells[9].text).split(" ")
                    adrOverall = adr[0]
                    hs = CleanString(cells[10].text).split(" ")
                    hsOverall = hs[0]
                    fk = CleanString(cells[11].text).split(" ")
                    fkOverall = fk[0]
                    fd = CleanString(cells[12].text).split(" ")
                    fdOverall = fd[0]
                    fkDifference = CleanString(cells[13].text).split(" ")
                    fkDifferenceOverall = fkDifference[0]

                    data = [player, team, agent, ratingOverall, acsOverall, killsOverall, deathsOverall, assistsOverall, kdDifferenceOverall, kastOverall, adrOverall, hsOverall, fkOverall, fdOverall, fkDifferenceOverall]
                    with open('match.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow('-')
        except:
            keepGoing = 0

    #Map 5 Stats
    if(keepGoing):
        try:
            #Get Map
            mapDiv = mapDiv.findNext('div', {'class': 'map'})
            mapData = CleanString(mapDiv.text).split(" ")
            mapText = mapData[0]

            #Get Map Score
            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team1ScoreText = teamScoreData[0]

            teamScoreDiv = teamScoreDiv.findNext('div', {'class': 'score'})
            teamScoreData = CleanString(teamScoreDiv.text).split(" ")
            team2ScoreText = teamScoreData[0]

            # Get if Team1 is on Attack or Defence in first half
            roundsDiv = roundsDiv.findNext('div', {'class': 'vlr-rounds'})
            sideDiv = roundsDiv.find('div', {'class': 'vlr-rounds-row-col'})
            sideDiv = sideDiv.findNext('div', {'class': 'vlr-rounds-row-col'})
            team2 = False
            for div in sideDiv:
                if("rnd-sq mod-win mod-ct" in str(div)):
                    if(team2):
                        sideText = 'T'
                    else:
                        sideText = 'CT'
                elif("rnd-sq mod-win mod-t" in str(div)):
                    if(team2):
                        sideText = 'CT'
                    else:
                        sideText = 'T'
                elif("rnd-sq" in str(div)):
                    team2 = True

            team1StartingSide = sideText
            if(team1StartingSide == 'CT'):
                team2StartingSide = 'T'
            elif(team1StartingSide == 'T'):
                team2StartingSide = 'CT'
            else:
                team2StartingSide = 'NA'

            teamScoreMap = [mapText, team1NameText, team1ScoreText, team2NameText, team2ScoreText, team1StartingSide, team2StartingSide]

            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(teamScoreMap)

            #Stats
            table = table.findNext('div', {'class': 'vm-stats-game'})
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    playerteam = CleanString(cells[0].text).split(" ")
                    player, team = playerteam[0], playerteam[1]
                    if(player == 'gob' and team == 'b'):
                        player = 'gob-b'
                        team = playerteam[2]
                    
                    for img in row.find_all('img', alt=True):
                        agent = CleanString(img['alt'])

                    ratings = CleanString(cells[2].text).split(" ")
                    ratingOverall = ratings[0]
                    acs = CleanString(cells[3].text).split(" ")
                    acsOverall = acs[0]
                    kills = CleanString(cells[4].text).split(" ")
                    killsOverall = kills[0]
                    deaths = CleanString(cells[5].text).split(" ")
                    deathsOverall = deaths[1]
                    assists = CleanString(cells[6].text).split(" ")
                    assistsOverall = assists[0]
                    kdDifference = CleanString(cells[7].text).split(" ")
                    kdDifferenceOverall = kdDifference[0]
                    kast = CleanString(cells[8].text).split(" ")
                    kastOverall = kast[0]
                    adr = CleanString(cells[9].text).split(" ")
                    adrOverall = adr[0]
                    hs = CleanString(cells[10].text).split(" ")
                    hsOverall = hs[0]
                    fk = CleanString(cells[11].text).split(" ")
                    fkOverall = fk[0]
                    fd = CleanString(cells[12].text).split(" ")
                    fdOverall = fd[0]
                    fkDifference = CleanString(cells[13].text).split(" ")
                    fkDifferenceOverall = fkDifference[0]

                    data = [player, team, agent, ratingOverall, acsOverall, killsOverall, deathsOverall, assistsOverall, kdDifferenceOverall, kastOverall, adrOverall, hsOverall, fkOverall, fdOverall, fkDifferenceOverall]
                    with open('match.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
            with open('match.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow('-')
        except:
            keepGoing = 0

    with open('match.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow('/')