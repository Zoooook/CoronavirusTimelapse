import os
from math import sqrt

try: os.mkdir('originals')
except: pass

csv = open('history.csv', 'r').readlines()

dates = {}
counties = []

headers = csv[0].split(',')
deaths = csv[1].split(',')
for county in csv[2:]:
    counties.append(county.split(','))

for i in range(4, len(headers)-1):
    circles = []
    states = {}
    cases = 0

    for county in counties:
        if county[i]:
            circles.append({
                'cx': county[0],
                'cy': county[1],
                'r': str(sqrt(int(county[i]))/5)
            })

            state = county[3]
            if state not in states: states[state] = 0
            states[state] += int(county[i])
            cases += int(county[i])

    dates[headers[i]] = {
        'cases': str(cases),
        'deaths': deaths[i],
        'circles': circles,
        'states': states,
    }

for day in range(1,21):
    newFile = open('originals/2020-01-' + str(day).zfill(2) + '-1.txt', 'w')
    newFile.write('<p class="g-body ">  , at least 0 p   , according to a New York Times database, and at least 0 patients with the virus have died. </p>\n')
    newFile.close()

for date in dates:
    text = '<p class="g-body ">  , at least ' + dates[date]['cases'] + ' p   , according to a New York Times database, and at least ' + dates[date]['deaths'] + ' patients with the virus have died. </p>\n'
    for circle in dates[date]['circles']:
        text += '<circle cx="' + circle['cx'] + '" cy="' + circle['cy'] + '" r="' + circle['r'] + '"></circle>\n'
    for state in dates[date]['states']:
        text += '<span class="desktop label" style="top: auto; height: auto">' + state + '</span><span class="mobile label"></span><span>' + str(dates[date]['states'][state]) + '</span>\n'

    newFile = open('originals/2020-' + date + '-1.txt', 'w')
    newFile.write(text)
    newFile.close()