import csv

def ClearCsv():
    f = open('data.csv', 'w+')
    f.close()

def ParseCsv():
    file = open('match.csv', 'r')
    data = list(csv.reader(file))
    file.close()

    header = ['Map', 'Winner',
              'Team1StartingSide', 'Team2StartingSide',
              'AverageACSTeam1', 'AverageACSTeam2',
              'AverageKillsTeam1', 'AverageKillsTeam2', 
              'TotalFKTeam1', 'TotalFKTeam2',
              'TotalFDTeam1', 'TotalFDTeam2',
              'TotalKillsTeam1', 'TotalKillsTeam2',
              'TotalDeathsTeam1', 'TotalDeathsTeam2',
              'TotalFKFDTeam1', 'TotalFKFDTeam2',
              'EntryFKFDTeam1', 'EntryFKFDTeam2',
              'HsPercentageTeam1', 'HsPercentageTeam2']
    
    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    i=0
    while i<len(data):
        x=data[i]

        if(x[0] == '-'):
            map = data[i+1][0]
            if(map != '/'):
                i += 1
                team1score = data[i][2]
                team2score = data[i][4]

                if(int(team1score) > int(team2score)):
                    winner = 1
                elif(int(team1score) < int(team2score)):
                    winner = -1
                else:
                    winner = 0

                team1side = data[i][5]
                team2side = data[i][6]

                team1acs = []
                team1fk = []
                team1fd = []
                team1kills = []
                team1deaths = []
                team1fkfd = []
                team1entryfkfd = []
                team1headshotpercentage = []
                team2acs = []
                team2fk = []
                team2fd = []
                team2kills = []
                team2deaths = []
                team2fkfd = []
                team2entryfkfd = []
                team2headshotpercentage = []
                y=0
                while(y != 5):
                    try:
                        i += 1
                        team1acs.append(data[i][4])
                        team1fk.append(data[i][12])
                        team1fd.append(data[i][13])
                        team1kills.append(data[i][5])
                        team1deaths.append(data[i][6])
                        team1fkfd.append(data[i][14])
                        team1headshotpercentage.append(data[i][11])
                        if(data[i][2] == 'jett' or 'neon' or 'raze'):
                            team1entryfkfd.append(data[i][14])
                        y += 1
                    except:
                        y += 1
                while(y != 10):
                    i += 1
                    team2acs.append(data[i][4])
                    team2fk.append(data[i][12])
                    team2fd.append(data[i][13])
                    team2kills.append(data[i][5])
                    team2deaths.append(data[i][6])
                    team2fkfd.append(data[i][14])
                    team2headshotpercentage.append(data[i][11])
                    if(data[i][2] == 'jett' or 'neon' or 'raze'):
                        team2entryfkfd.append(data[i][14])
                    y += 1

                team1AverageAcs, team1AverageKills, team1TotalFk, team1TotalFd, team1TotalKills, team1TotalDeaths, team1TotalFkFd, team1AverageHS = 0, 0, 0, 0, 0, 0, 0, 0
                team2AverageAcs, team2AverageKills, team2TotalFk, team2TotalFd, team2TotalKills, team2TotalDeaths, team2TotalFkFd, team2AverageHS = 0, 0, 0, 0, 0, 0, 0, 0
                team1AverageEntryFkFd, team2AverageEntryFkFd, iteration1, iteration2 = 0, 0, 0, 0

                for duelist in team1entryfkfd:
                    try:
                        team1AverageEntryFkFd += int(duelist)
                        iteration1 += 1
                    except:
                        team1AverageEntryFkFd = 0
                for duelist in team2entryfkfd:
                    try:
                        team2AverageEntryFkFd += int(duelist)
                        iteration2 += 1
                    except:
                        team2AverageEntryFkFd = 0
                try:
                    team1AverageEntryFkFd = team1AverageEntryFkFd/iteration1
                    team2AverageEntryFkFd = team2AverageEntryFkFd/iteration2
                except:
                    print("0 duelist comp")

                try:
                    y=0
                    while(y != 5):
                        team1AverageAcs += int(team1acs[y])
                        team1AverageKills += int(team1kills[y])
                        team1AverageHS += int(team1headshotpercentage[y])
                        team1TotalFk += int(team1fk[y])
                        team1TotalFd += int(team1fd[y])
                        team1TotalKills += int(team1kills[y])
                        team1TotalDeaths += int(team1deaths[y])
                        team1TotalFkFd += int(team1fkfd[y])

                        team2AverageAcs += int(team2acs[y])
                        team2AverageKills += int(team2kills[y])
                        team2AverageHS += int(team2headshotpercentage[y])
                        team2TotalFk += int(team2fk[y])
                        team2TotalFd += int(team2fd[y])
                        team2TotalKills += int(team2kills[y])
                        team2TotalDeaths += int(team2deaths[y])
                        team2TotalFkFd += int(team2fkfd[y])
                        y += 1
                    team1AverageAcs = team1AverageAcs/5
                    team2AverageAcs = team2AverageAcs/5
                    team1AverageKills = team1AverageKills/5
                    team2AverageKills = team2AverageKills/5
                    team1AverageHS = team1AverageHS/5
                    team2AverageHS = team2AverageHS/5

                    row = [map, winner, team1side, team2side, team1AverageAcs, team2AverageAcs, team1AverageKills, team2AverageKills, team1TotalFk, team2TotalFk,
                            team1TotalFd, team2TotalFd, team1TotalKills, team2TotalKills, team1TotalDeaths, team2TotalDeaths, team1TotalFkFd, team2TotalFkFd, team1AverageEntryFkFd, team2AverageEntryFkFd,
                            team1AverageHS, team2AverageHS]

                    with open('data.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
                except:
                    pass
            else:
                i += 1
        else:
            i += 1

ClearCsv()
ParseCsv()