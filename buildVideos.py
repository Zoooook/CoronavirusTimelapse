# ---------------------------------------------------- User Input ---------------------------------------------------- #

buildVideos = {
    'Total Cases':             {'scale': 2},
    'Total Deaths':            {'scale': 4},
    'Daily Cases':             {'scale': 5},
    'Daily Deaths':            {'scale': 10},
    'Total Cases Per Capita':  {'scale': 1},
    'Total Deaths Per Capita': {'scale': 2},
    'Daily Cases Per Capita':  {'scale': 3},
    'Daily Deaths Per Capita': {'scale': 6},
}

casesLookbackDays = 3
deathsLookbackDays = 5

framesPerDay = 12
daysPerSecond = 2

# ------------------------------------------------------ Setup ------------------------------------------------------- #

import os
from selenium import webdriver
from urllib.request import urlopen
import json
from codecs import iterdecode
import csv
from math import floor, ceil, sqrt
from PIL import Image
from shutil import copyfile

def makeDir(dir):
    try: os.mkdir(dir)
    except: pass

makeDir('videos')
dirs = ['html', 'images', 'frames']
for dir in dirs:
    makeDir(dir)
    for subDir in buildVideos:
        makeDir(dir + '/' + subDir)

options = webdriver.ChromeOptions()
options.add_argument('--kiosk')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

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

types = {
    'Total Cases':             {'index': 1},
    'Total Deaths':            {'index': 2},
    'Daily Cases':             {'index': 3},
    'Daily Deaths':            {'index': 4},
    'Total Cases Per Capita':  {'index': 5},
    'Total Deaths Per Capita': {'index': 6},
    'Daily Cases Per Capita':  {'index': 7},
    'Daily Deaths Per Capita': {'index': 8},
}
for type in types:
    types[type]['title']  = type.replace('Capita', 'Million People')
    types[type]['cases']  = type.replace('Deaths', 'Cases')
    types[type]['deaths'] = type.replace('Cases', 'Deaths')
    typeWords = type.split(' ')
    if typeWords[1] == 'Cases':
        types[type]['circles'] = 'red'
        types[type]['labels'] = 'black'
        types[type]['lookbackDays'] = casesLookbackDays
    else:
        types[type]['circles'] = 'black'
        types[type]['labels'] = 'aqua'
        types[type]['lookbackDays'] = deathsLookbackDays

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
    states[state]['population'] = 0
    if 'displayName' not in states[state]:
        states[state]['displayName'] = states[state]['name']

# ------------------------------------------------- Get Static Data -------------------------------------------------- #

response = urlopen('https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/51a3a94e6fc49506549d9cfad8fd567653c2b2a3/slip-map/usa/us_states_centroids.json')
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

response = urlopen('https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/51a3a94e6fc49506549d9cfad8fd567653c2b2a3/slip-map/usa/us_counties_centroids.json')
countyData = json.loads(response.read())

counties = {}
for county in countyData['features']:
    if  county['properties']['displayname'] == 'Doña Ana':
        county['properties']['displayname'] =  'Dona Ana'
    counties[county['properties']['st'] + ':' + county['properties']['displayname']] = {
        'x': 50   + 2.325 * county['geometry']['coordinates'][0],
        'y': 32.1 - 2.345 * county['geometry']['coordinates'][1],
    }
counties['PR:Puerto Rico'] = {'x': 86, 'y': 49}
counties['VI:Unknown']     = {'x': 95, 'y': 49}
counties['GU:Unknown']     = {'x': 57, 'y': 60}
counties['MP:Unknown']     = {'x': 71, 'y': 60}

def countyKey(key):
    keyMap = {
        'AK:Anchorage': 'AK:Anchorage Municipality',
        'PR:Unknown':   'PR:Puerto Rico',
        'NM:Doña Ana':  'NM:Dona Ana',
    }
    if key in keyMap:
        return keyMap[key]
    if key[-5:] == ' city':
        return key[:-5] + ' City'
    return key

with open('population.json') as popFile:
    population = json.load(popFile)
totalPopulation = 0
for row in population:
    if row['us_county_fips'] == '35013':
        row['subregion'] = 'Dona Ana'
    state = stateMap[row['region']]
    counties[countyKey(state + ':' + row['subregion'])]['population'] = int(row['population'])
    states[state]['population'] += int(row['population'])
    totalPopulation += int(row['population'])

# ------------------------------------------------- Get Dynamic Data ------------------------------------------------- #

response = urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
file = csv.reader(iterdecode(response, 'utf-8'))

csvData = []
for line in file:
    csvData.append(line)

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
    key = countyKey(state + ':' + row[1])
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

    if state not in data[today]['states']:
        data[today]['states'][state] = {}
        for type in types:
            data[today]['states'][state][type] = 0

    data[today]['counties'][key] = {
        'Total Cases':  int(row[4]),
        'Total Deaths': int(row[5]),
    }

    def typeSort(type):
        t = 0
        if type[:6] == 'Daily ':
            t += 1
        if type[-6:] == 'Capita':
            t += 2
        return t

    # this is the sorted() parameter 'key', not the variable
    for type in sorted(types, key = typeSort):
        lookbackDay = dates[-1-types[type]['lookbackDays']]

        if type[:6] == 'Total ' and type[-6:] == 'Capita':
            data[today]['counties'][key][type] = 0
            if key in counties:
                rawType = type.replace(' Per Capita', '')
                data[today]['counties'][key][type] = data[today]['counties'][key][rawType] * 1000000 / counties[key]['population']
        if type[:6] == 'Daily ':
            totalType = type.replace('Daily', 'Total')
            subtrahend = data[lookbackDay]['counties'][key][totalType] if key in data[lookbackDay]['counties'] else 0
            data[today]['counties'][key][type] = (data[today]['counties'][key][totalType] - subtrahend) / types[type]['lookbackDays']
            if  data[today]['counties'][key][type] < 0:
                data[today]['counties'][key][type] = 0

        if type[-6:] != 'Capita':
            data[today]['states'][state][type] += data[today]['counties'][key][type]
            data[today][type]                  += data[today]['counties'][key][type]

for type in types:
    if type[-6:] == 'Capita':
        rawType = type.replace(' Per Capita', '')
        for date in dates:
            for state in data[date]['states']:
                data[date]['states'][state][type] = data[date]['states'][state][rawType] * 1000000 / states[state]['population']
            data[date][type] = data[date][rawType] * 1000000 / totalPopulation
    for date in dates:
        for state in data[date]['states']:
            data[date]['states'][state][type] = data[date]['states'][state][type]
        data[date][type] = data[date][type]

missingList = sorted(filter(lambda x: x[2:] != ':Unknown', list(missing)))
if len(missingList):
    for key in missingList:
        print('Missing', key)
    exit()

# --------------------------------------------------- Build Videos --------------------------------------------------- #

with open('map.html', 'r') as mapFile:
    map = mapFile.read()

driver = webdriver.Chrome('chromedriver', options = options)

def weightedAverage(num1, num2, fraction):
    return num2*fraction + num1*(1-fraction)

def roundHalfUp(num):
    return floor(num) if num%1<.5 else ceil(num)

def formatNum(num):
    return f'{num:,}'

def buildHtml(day1, day2, numer, denom):
    day2 = day2 or day1
    date = day1 if 2*numer<denom else day2
    fraction = numer/denom

    html = map
    for county in sorted(set(data[day1]['counties']) | set(data[day2]['counties'])):
        if county not in missing:
            numDay1 = data[day1]['counties'][county][type] if county in data[day1]['counties'] else 0
            numDay2 = data[day2]['counties'][county][type] if county in data[day2]['counties'] else 0
            numFinal = weightedAverage(numDay1, numDay2, fraction)
            if numFinal:
                r = sqrt(numFinal) * buildVideos[type]['scale'] / 100
                html += '<circle cx="' + str(counties[county]['x']) + '" cy="' + str(counties[county]['y']) + '" r="' + str(r) + '" class="' + types[type]['circles'] + '"></circle>\n'
    html += '\n</svg>\n\n'

    for state in sorted(set(data[day1]['states']) | set(data[day2]['states'])):
        numDay1 = data[day1]['states'][state][type] if state in data[day1]['states'] else 0
        numDay2 = data[day2]['states'][state][type] if state in data[day2]['states'] else 0
        numFinal = roundHalfUp(weightedAverage(numDay1, numDay2, fraction))
        if numFinal:
            html += '<div class="point svelte-3fv2ao" style="left: '+ str(states[state]['x']) + '%; top: ' + str(states[state]['y']) + '%">'
            html += '<div class="labeled-count svelte-1krny27" style="top: -0.65em;">'
            html += '<span class="label ' + types[type]['labels'] + '">' + states[state]['displayName'] + '</span><span class="count ' + types[type]['labels'] + '">' + formatNum(numFinal) + '</span></div></div>\n'

    html += '\n<div class="point svelte-3fv2ao" style="left: 45%; top: 4%; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold; position: absolute; width: 100%; left: -50%">' + types[type]['title'] + '</span></div>\n'
    if type[:6] == 'Daily ':
        html += '\n<div class="point svelte-3fv2ao" style="left: 45%; top: 7.5%; text-align: center"><span class="label" style="font-size: 1.25em; font-weight: bold; position: absolute; width: 100%; left: -50%">Rolling ' + str(types[type]['lookbackDays']) + '-Day Average</span></div>\n'
    html += '\n<div class="point svelte-3fv2ao" style="left: 77.7%; top: 4%; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold; position: absolute; width: 100%; left: -50%">' + monthMap[int(date[5:7])] + str(int(date[8:10])) + '</span></div>\n'
    html += '<div class="point svelte-3fv2ao" style="left: 64%; top: 9%; width: 200px; text-align: center"><span class="label black" style="font-size: 2em">Cases</span><span class="count red" style="font-size: 2em">'    + formatNum(roundHalfUp(weightedAverage(data[day1][types[type]['cases']],  data[day2][types[type]['cases']],  fraction))) + '</span></div>\n'
    html += '<div class="point svelte-3fv2ao" style="left: 79%; top: 9%; width: 200px; text-align: center"><span class="label black" style="font-size: 2em">Deaths</span><span class="count black" style="font-size: 2em">' + formatNum(roundHalfUp(weightedAverage(data[day1][types[type]['deaths']], data[day2][types[type]['deaths']], fraction))) + '</span></div>\n\n</div></div>'

    return html

def buildImages(htmlFilename, imageFilename, frameFilename):
    if not os.path.exists(imageFilename):
        driver.get('file:///' + os.getcwd().replace('\\','/') + '/' + htmlFilename)
        driver.save_screenshot('images/temp.png')

        image = Image.open('images/temp.png')
        image = image.crop((10, 30, 1610, 1030))
        image.save(imageFilename)
        os.remove('images/temp.png')

    if not os.path.exists(frameFilename):
        copyfile(imageFilename, frameFilename)

try:
    with open('lastFpd.json') as fpdFile:
        lastFpd = json.load(fpdFile)
except:
    lastFpd = {}

fps = framesPerDay * daysPerSecond
frameOffset = framesPerDay // 2 + 1

for type in buildVideos:
    if type not in lastFpd or lastFpd[type] != framesPerDay:
        for filename in os.listdir('frames/' + type):
            os.remove('frames/' + type + '/' + filename)
        lastFpd[type] = framesPerDay
        with open('lastFpd.json', 'w') as fpdFile:
            json.dump(lastFpd, fpdFile)

    for i in range(len(dates)):
        today = dates[i]
        yesterday = dates[i-1] if i else ''

        html = buildHtml(today, '', 0, 1)

        htmlFilename = 'html/' + type + '/' + today + '.000.html'
        imageFilename = 'images/' + type + '/' + today + '.000.png'
        frameFilename = 'frames/' + type + '/frame' + str(frameOffset+i*framesPerDay).zfill(5) + '.png'

        try:
            with open(htmlFilename, 'r') as oldFile:
                oldHtml = oldFile.read()
        except:
            oldHtml = ''

        if html != oldHtml or not os.path.exists(imageFilename):
            for filename in os.listdir('html/' + type):
                if filename[:10] in [yesterday, today] and filename[-9:] != '.000.html':
                    os.remove('html/' + type + '/' + filename)
            for filename in os.listdir('images/' + type):
                if filename[:10] in [yesterday, today] and filename[-8:] != '.000.png':
                    os.remove('images/' + type + '/' + filename)
            try: os.remove(imageFilename)
            except: pass
            for j in range(frameOffset+(i-1)*framesPerDay+1, frameOffset+(i+1)*framesPerDay):
                try: os.remove('frames/' + type + '/frame' + str(j).zfill(5) + '.png')
                except: pass

            with open(htmlFilename, 'w') as newFile:
                newFile.write(html)

        buildImages(htmlFilename, imageFilename, frameFilename)

        for j in range(1, framesPerDay):
            frame = frameOffset + (i-1)*framesPerDay + j
            if frame > 0:
                frameFilename = 'frames/' + type + '/frame' + str(frame).zfill(5) + '.png'
                if i < 20:
                    date = yesterday if 2*j<framesPerDay else today
                    htmlFilename = 'html/' + type + '/' + date + '.000.html'
                    imageFilename = 'images/' + type + '/' + date + '.000.png'
                else:
                    decimal = f'{j/framesPerDay:0.3f}'[1:]
                    htmlFilename = 'html/' + type + '/' + yesterday + decimal + '.html'
                    imageFilename = 'images/' + type + '/' + yesterday + decimal + '.png'

                if not os.path.exists(htmlFilename):
                    with open(htmlFilename, 'w') as newFile:
                        newFile.write(buildHtml(yesterday, today, j, framesPerDay))
                buildImages(htmlFilename, imageFilename, frameFilename)

    lastFrame = frameOffset + (len(dates)-1) * framesPerDay
    lastFrameFilename = 'frames/' + type + '/frame' + str(lastFrame).zfill(5) + '.png'
    for j in range(lastFrame+1, lastFrame+fps*5+1):
        copyFilename = 'frames/' + type + '/frame' + str(j).zfill(5) + '.png'
        copyfile(lastFrameFilename, copyFilename)

    os.system('ffmpeg -f image2 -r ' + str(fps) + ' -i "frames/' + type + '/frame%05d.png" -r ' + str(fps) + ' -c:a copy -c:v libx264 -crf 16 -preset veryslow "videos/' + str(types[type]['index']) + ' ' + type + '.mp4" -y')

driver.quit()