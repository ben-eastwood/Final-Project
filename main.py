import csv
import matchStatsFunction as f
import urlGetFunction as u
import time
import csvParse as c

print("Operation Started")
startTime = time.time()
eventUrls = []

f.ClearCsv()
u.ClearUrls()
c.ClearCsv()

u.GetEvents('https://www.vlr.gg/vct-2022')

file = open('eventUrl.csv', 'r')
data = list(csv.reader(file))
file.close()

i=0
while i<len(data):
    x = data[i]
    z = x[0]
    eventUrls.append(z)
    i += 1

u.GetUrls(eventUrls)

file = open('urls.csv', 'r')
data = list(csv.reader(file))
file.close()

print("Match Stats Gathering Started")

i=0
while i<len(data):
    x = data[i]
    z = x[0]
    f.GetMatchStats(z)
    i += 1

print("Parsing Data")
c.ParseCsv()

endTime = time.time()
finalTime = endTime - startTime
finalTimeStr = str(finalTime)

print("Operation Successful")
print("Operation took " + finalTimeStr + " to complete.")