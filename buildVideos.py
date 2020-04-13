framesPerDay = 1

buildVideos = [
    'Total Cases',
    'Total Deaths',
    'New Cases',
    'New Deaths',
]

import os
import shutil
import urllib.request
import codecs
import csv
import json
from math import sqrt
from selenium import webdriver
from PIL import Image

def formatNum(num):
    return f'{num:,}'

def makeDir(dir):
    try: os.mkdir(dir)
    except: pass

makeDir('videos')
dirs = ['html', 'frames']
for dir in dirs:
    makeDir(dir)
    for subDir in buildVideos:
        makeDir(dir + '/' + subDir)

options = webdriver.ChromeOptions()
options.add_argument('--kiosk')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

types = {
    'Total Cases':  {'cases': 'Total Cases', 'deaths': 'Total Deaths', 'circles': 'red',   'labels': 'black', 'scale': 3},
    'Total Deaths': {'cases': 'Total Cases', 'deaths': 'Total Deaths', 'circles': 'black', 'labels': 'aqua',  'scale': 10},
    'New Cases':    {'cases': 'New Cases',   'deaths': 'New Deaths',   'circles': 'red',   'labels': 'black', 'scale': 10},
    'New Deaths':   {'cases': 'New Cases',   'deaths': 'New Deaths',   'circles': 'black', 'labels': 'aqua',  'scale': 25},
}

states = {
    'AL': {'name': 'Alabama'},
    'AK': {'name': 'Alaska'},
    'AZ': {'name': 'Arizona'},
    'AR': {'name': 'Arkansas'},
    'CA': {'name': 'California'},
    'CO': {'name': 'Colorado'},
    'CT': {'name': 'Connecticut'},
    'DE': {'name': 'Delaware'},
    'FL': {'name': 'Florida'},
    'GA': {'name': 'Georgia'},
    'HI': {'name': 'Hawaii'},
    'ID': {'name': 'Idaho'},
    'IL': {'name': 'Illinois'},
    'IN': {'name': 'Indiana'},
    'IA': {'name': 'Iowa'},
    'KS': {'name': 'Kansas'},
    'KY': {'name': 'Kentucky'},
    'LA': {'name': 'Louisiana'},
    'ME': {'name': 'Maine'},
    'MD': {'name': 'Maryland'},
    'MA': {'name': 'Massachusetts'},
    'MI': {'name': 'Michigan'},
    'MN': {'name': 'Minnesota'},
    'MS': {'name': 'Mississippi'},
    'MO': {'name': 'Missouri'},
    'MT': {'name': 'Montana'},
    'NE': {'name': 'Nebraska'},
    'NV': {'name': 'Nevada'},
    'NH': {'name': 'New Hampshire'},
    'NJ': {'name': 'New Jersey'},
    'NM': {'name': 'New Mexico'},
    'NY': {'name': 'New York'},
    'NC': {'name': 'North Carolina'},
    'ND': {'name': 'North Dakota'},
    'OH': {'name': 'Ohio'},
    'OK': {'name': 'Oklahoma'},
    'OR': {'name': 'Oregon'},
    'PA': {'name': 'Pennsylvania'},
    'RI': {'name': 'Rhode Island'},
    'SC': {'name': 'South Carolina'},
    'SD': {'name': 'South Dakota'},
    'TN': {'name': 'Tennessee'},
    'TX': {'name': 'Texas'},
    'UT': {'name': 'Utah'},
    'VT': {'name': 'Vermont'},
    'VA': {'name': 'Virginia'},
    'WA': {'name': 'Washington'},
    'WV': {'name': 'West Virginia'},
    'WI': {'name': 'Wisconsin'},
    'WY': {'name': 'Wyoming'},
    'DC': {'name': 'District of Columbia', 'displayName': 'D.C.'},
    'PR': {'name': 'Puerto Rico'},
    'VI': {'name': 'Virgin Islands'},
    'GU': {'name': 'Guam'},
    'MP': {'name': 'Northern Mariana Islands'},
}

stateMap = {}
for state in states:
    stateMap[states[state]['name']] = state
    if 'displayName' not in states[state]:
        states[state]['displayName'] = states[state]['name']

monthMap = {
    1: 'January ',
    2: 'February ',
    3: 'March ',
    4: 'April ',
    5: 'May ',
    6: 'June ',
    7: 'July ',
    8: 'August ',
    9: 'September ',
    10: 'October ',
    11: 'November ',
    12: 'December ',
}

response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
file = csv.reader(codecs.iterdecode(response, 'utf-8'))

csvData = []
for line in file:
    csvData.append(line)

response = urllib.request.urlopen('https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/51a3a94e6fc49506549d9cfad8fd567653c2b2a3/slip-map/usa/us_states_centroids.json')
stateData = json.loads(response.read())

for state in stateData['features']:
    if state['geometry'] is not None:
        states[state['properties']['state_abbrev']]['x'] = 50 + 2.325 * state['geometry']['coordinates'][0]
        states[state['properties']['state_abbrev']]['y'] = 49.5 - 3.65 * state['geometry']['coordinates'][1]
states['HI']['x'] -= 1
states['HI']['y'] += 1
states['WV']['x'] -= 1
states['WV']['y'] += 2
states['DC']['y'] += 2
states['MD']['x'] -= 1
states['MD']['y'] -= 1.5
states['DE']['x'] += .5
states['VT']['y'] -= 1
states['NH']['y'] += 1.5
states['MA']['y'] -= .9
states['RI']['x'] += 1.2
states['CT']['y'] += 1.4
states['PR']['x'] = 86
states['PR']['y'] = 72
states['VI']['x'] = 95
states['VI']['y'] = 72
states['GU']['x'] = 57
states['GU']['y'] = 89
states['MP']['x'] = 71
states['MP']['y'] = 89

response = urllib.request.urlopen('https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/51a3a94e6fc49506549d9cfad8fd567653c2b2a3/slip-map/usa/us_counties_centroids.json')
countyData = json.loads(response.read())

counties = {}
for county in countyData['features']:
    counties[county['properties']['st'] + ':' + county['properties']['displayname']] = {
        'x': 50   + 2.325 * county['geometry']['coordinates'][0],
        'y': 32.1 - 2.345 * county['geometry']['coordinates'][1],
    }
counties['PR:Puerto Rico'] = {'x': 86, 'y': 49}
counties['VI:Unknown']     = {'x': 95, 'y': 49}
counties['GU:Unknown']     = {'x': 57, 'y': 60}
counties['MP:Unknown']     = {'x': 71, 'y': 60}

keyMap = {
    'AK:Anchorage': 'AK:Anchorage Municipality',
    'PR:Unknown':   'PR:Puerto Rico',
}

missing = {}
dates = []
data = {}
for day in range(1, 21):
    date = '2020-01-' + str(day).zfill(2)
    dates.append(date)
    data[date] = {
        'counties': {},
        'states':   {},
    }
    for type in types:
        data[date][type] = 0

for row in csvData[1:]:
    state = stateMap[row[2]]
    key = state + ':' + row[1]
    if key[-5:] == ' city':
        key = key[:-5] + ' City'
    if key in keyMap:
        key = keyMap[key]
    if not key in counties:
        missing[key] = True

    today = row[0]
    if dates[-1] != today:
        dates.append(today)
        data[today] = {
            'counties': {},
            'states':   {},
        }
        for type in types:
            data[today][type] = 0

    yesterday = dates[-2]

    if state not in data[today]['states']:
        data[today]['states'][state] = {}
        for type in types:
            data[today]['states'][state][type] = 0

    data[today]['counties'][key] = {
        'Total Cases':  int(row[4]),
        'Total Deaths': int(row[5]),
    }
    for type in types:
        if type[:4] == 'New ':
            totalType = 'Total ' + type[4:]
            subtrahend = 0
            if key in data[yesterday]['counties']:
                subtrahend = data[yesterday]['counties'][key][totalType]
            data[today]['counties'][key][type] = data[today]['counties'][key][totalType] - subtrahend
            if  data[today]['counties'][key][type] < 0:
                data[today]['counties'][key][type] = 0
        data[today]['states'][state][type] += data[today]['counties'][key][type]
        data[today][type]                  += data[today]['counties'][key][type]

missingList = sorted(filter(lambda x: x[2:] != ':Unknown', list(missing)))
if len(missingList):
    for key in missingList:
        print('Missing', key)
    exit()



fps = framesPerDay * 2

try:
    with open('lastFps.json') as fpsFile:
        lastFps = json.load(fpsFile)
except:
    lastFps = {}
try:
    with open('lastFps.json') as fpsFile:
        lastFps = json.load(fpsFile)
except:
    lastFps = {}
with open('map.html', 'r') as mapFile:
    map = mapFile.read()

for type in buildVideos:
    if type not in lastFps or lastFps[type] != fps:
        for filename in os.listdir('html/' + type):
            os.remove('html/' + type + '/' + filename)
        for filename in os.listdir('frames/' + type):
            os.remove('frames/' + type + '/' + filename)
        lastFps[type] = fps
        with open('lastFps.json', 'w') as fpsFile:
            json.dump(lastFps, fpsFile)

    types[type]['anyUpdated'] = False
    i = 0
    for date in dates:
        i += 1

        month = int(date[5:7])
        day = int(date[8:10])

        html = map
        for county in data[date]['counties']:
            if county not in missing and data[date]['counties'][county][type] > 0:
                r = sqrt(data[date]['counties'][county][type]) * types[type]['scale'] / 100
                html += '<circle cx="' + str(counties[county]['x']) + '" cy="' + str(counties[county]['y']) + '" r="' + str(r) + '" class="' + types[type]['circles'] + '"></circle>\n'

        html += '\n</svg>\n\n'

        for state in data[date]['states']:
            if data[date]['states'][state][type] > 0:
                html += '<div class="point svelte-3fv2ao" style="left: '+ str(states[state]['x']) + '%; top: ' + str(states[state]['y']) + '%">'
                html += '<div class="labeled-count svelte-1krny27" style="top: -0.65em;">'
                html += '<span class="label ' + types[type]['labels'] + '">' + states[state]['displayName'] + '</span><span class="count ' + types[type]['labels'] + '">' + formatNum(data[date]['states'][state][type]) + '</span></div></div>\n'

        html += '\n<div class="point svelte-3fv2ao" style="left: 35%; top: 4%; width: 200px; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold">' + type + '</span></div>\n'
        html += '\n<div class="point svelte-3fv2ao" style="left: 71.5%; top: 4%; width: 200px; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold">' + monthMap[month] + str(day) + '</span></div>\n'
        html += '<div class="point svelte-3fv2ao" style="left: 64%; top: 9%; width: 200px; text-align: center"><span class="label black" style="font-size: 2em">Cases</span><span class="count red" style="font-size: 2em">' + formatNum(data[date][types[type]["cases"]]) + '</span></div>\n'
        html += '<div class="point svelte-3fv2ao" style="left: 79%; top: 9%; width: 200px; text-align: center"><span class="label black" style="font-size: 2em">Deaths</span><span class="count black" style="font-size: 2em">' + formatNum(data[date][types[type]["deaths"]]) + '</span></div>\n\n</div></div>'

        htmlFilename = 'html/' + type + '/' + date + '.html'
        imageFilename = 'frames/' + type + '/frame' + str(i).zfill(4) + '.png'

        try:
            with open(htmlFilename, 'r') as oldFile:
                oldHtml = oldFile.read()
        except:
            oldHtml = ''

        if html != oldHtml or not os.path.exists(imageFilename):
            types[type]['anyUpdated'] = True

            with open(htmlFilename, 'w') as newFile:
                newFile.write(html)

            driver = webdriver.Chrome('chromedriver', options = options)
            driver.get('file:///' + os.getcwd().replace('\\','/') + '/' + htmlFilename)
            driver.save_screenshot('frames/temp.png')
            driver.quit()

            image = Image.open('frames/temp.png')
            image = image.crop((10, 30, 1610, 1030))
            image.save(imageFilename)
            os.remove('frames/temp.png')

    for j in range(i+1, i+1+fps*2):
        copyFilename = 'frames/' + type + '/frame' + str(j).zfill(4) + '.png'
        if not os.path.exists(copyFilename):
            shutil.copyfile(imageFilename, copyFilename)
            types[type]['anyUpdated'] = True

    badFilename = 'frames/' + type + '/frame' + str(i+1+fps*2).zfill(4) + '.png'
    if os.path.exists(badFilename):
        print('Too many frames:', badFilename)
        exit()

    if types[type]['anyUpdated']:
        os.remove('videos/' + type + '.mp4')
    if not os.path.exists('videos/' + type + '.mp4'):
        os.system('ffmpeg -f image2 -r ' + str(fps) + ' -i "frames/' + type + '/frame%04d.png" -r ' + str(fps) + ' -c:a copy -c:v libx264 -crf 16 -preset veryslow "videos/' + type + '.mp4"')