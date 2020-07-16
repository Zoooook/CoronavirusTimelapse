# ---------------------------------------------------- User Input ---------------------------------------------------- #

videoTypes = {
    'Total County Cases':             {'startDate': '01-16', 'scale': 1,  'index': '01'},
    'Total County Deaths':            {'startDate': '02-24', 'scale': 2,  'index': '02'},
    'Total State Cases':              {'startDate': '01-16', 'scale': 1,  'index': '03'},
    'Total State Deaths':             {'startDate': '02-24', 'scale': 2,  'index': '04'},
    'Daily County Cases':             {'startDate': '01-20', 'scale': 5,  'index': '05'},
    'Daily County Deaths':            {'startDate': '02-25', 'scale': 10, 'index': '06'},
    'Daily State Cases':              {'startDate': '01-20', 'scale': 5,  'index': '07'},
    'Daily State Deaths':             {'startDate': '02-25', 'scale': 10, 'index': '08'},
    'Total County Cases Per Capita':  {'startDate': '02-12', 'scale': .5, 'index': '09'},
    'Total County Deaths Per Capita': {'startDate': '02-26', 'scale': 1,  'index': '10'},
    'Total State Cases Per Capita':   {'startDate': '02-12', 'scale': 2,  'index': '11'},
    'Total State Deaths Per Capita':  {'startDate': '02-26', 'scale': 4,  'index': '12'},
    'Daily County Cases Per Capita':  {'startDate': '02-12', 'scale': 3,  'index': '13'},
    'Daily County Deaths Per Capita': {'startDate': '02-29', 'scale': 6,  'index': '14'},
    'Daily State Cases Per Capita':   {'startDate': '02-12', 'scale': 15, 'index': '15'},
    'Daily State Deaths Per Capita':  {'startDate': '02-29', 'scale': 30, 'index': '16'},
}

casesLookbackDays = 7
deathsLookbackDays = 7

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

dirs = ['html', 'images', 'frames']
for dir in dirs:
    makeDir(dir)
    for subDir in videoTypes:
        makeDir(dir + '/' + subDir)

options = webdriver.ChromeOptions()
options.add_argument('--kiosk')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = None

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

dataTypes = {
    'Total Cases': {},
    'Total Deaths': {},
    'Daily Cases': {},
    'Daily Deaths': {},
    'Total Cases Per Capita': {},
    'Total Deaths Per Capita': {},
    'Daily Cases Per Capita': {},
    'Daily Deaths Per Capita': {},
}

for type in dataTypes:
    dataTypes[type]['cases']  = type.replace('Deaths', 'Cases')
    dataTypes[type]['deaths'] = type.replace('Cases', 'Deaths')
    if type.split(' ')[1] == 'Cases':
        dataTypes[type]['lookbackDays'] = casesLookbackDays
        if type[:6] == 'Daily ':
            dataTypes[type]['deaths'] = dataTypes[type]['deaths'] + ' for Cases'
    else:
        dataTypes[type]['lookbackDays'] = deathsLookbackDays
        if type[:6] == 'Daily ':
            dataTypes[type]['cases'] = dataTypes[type]['cases'] + ' for Deaths'

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

with open('static/us_states_centroids.json') as stateFile:
    stateData = json.load(stateFile)

for state in stateData['features']:
    if state['geometry'] is not None:
        states[state['properties']['state_abbrev']]['labelx']  = 50   + 2.325 * state['geometry']['coordinates'][0]
        states[state['properties']['state_abbrev']]['labely']  = 49.5 - 3.65  * state['geometry']['coordinates'][1]
        states[state['properties']['state_abbrev']]['x']       = 50   + 2.325 * state['geometry']['coordinates'][0]
        states[state['properties']['state_abbrev']]['y']       = 32.1 - 2.345 * state['geometry']['coordinates'][1]
states['HI']['labelx'] -= 1
states['HI']['labely'] += 1
states['WV']['labelx'] -= 1
states['WV']['labely'] += 2
states['WV']['x'] -= 1
states['WV']['y'] += 1
states['DC']['labely'] += 2
states['MD']['labelx'] -= 1
states['MD']['labely'] -= 1.5
states['MD']['y'] -= .5
states['DE']['labelx'] += .5
states['VT']['labely'] -= 1
states['NH']['labely'] += 1.5
states['MA']['labely'] -= .9
states['RI']['labelx'] += 1.2
states['CT']['labely'] += 1.4
states['PR']['labelx'] = 86
states['PR']['labely'] = 72
states['VI']['labelx'] = 95
states['VI']['labely'] = 72
states['GU']['labelx'] = 57
states['GU']['labely'] = 89
states['MP']['labelx'] = 71
states['MP']['labely'] = 89

with open('static/us_counties_centroids.json') as countyFile:
    countyData = json.load(countyFile)

counties = {}
for county in countyData['features']:
    if county['properties']['fips'] == '35013':
        county['properties']['displayname'] = 'Dona Ana'
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
        'AK:Skagway':   'AK:Skagway Municipality',
        'PR:Unknown':   'PR:Puerto Rico',
        'NM:Doña Ana':  'NM:Dona Ana',
    }
    if key in keyMap:
        return keyMap[key]
    if key[-5:] == ' city':
        return key[:-5] + ' City'
    return key

with open('static/population.json') as popFile:
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

def typeSort(type):
    t = 0
    if type[:6] == 'Daily ':
        t += 1
    if type[-6:] == 'Capita':
        t += 2
    return t

response = urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
file = csv.reader(iterdecode(response, 'utf-8'))

csvData = []
for line in file:
    csvData.append(line)

missing = {}
dates = ['2019-12-31']
data = {'2019-12-31': {
    'counties': {},
    'states': {},
    'Daily Cases for Deaths': 0,
    'Daily Deaths for Cases': 0,
    'Daily Cases Per Capita for Deaths': 0,
    'Daily Deaths Per Capita for Cases': 0,
}}
for day in range(1, 21):
    date = '2020-01-' + str(day).zfill(2)
    dates.append(date)
    data[date] = data['2019-12-31'] # copies reference to object but it's ok because it never changes
    for type in dataTypes:
        data[date][type] = 0

for row in csvData[1:]:
    state = stateMap[row[2]]
    key = countyKey(state + ':' + row[1])
    if not key in counties:
        missing[key] = True

    today = row[0]
    if dates[-1] != today:
        dates.append(today)
        data[today] = {'counties': {}, 'states': {}}
        for type in dataTypes:
            data[today][type] = 0

    if state not in data[today]['states']:
        data[today]['states'][state] = {}
        for type in dataTypes:
            data[today]['states'][state][type] = 0

    data[today]['counties'][key] = {
        'Total Cases':  int(row[4]),
        'Total Deaths': int(row[5]),
    }

    # this is the sorted() parameter 'key', not the variable
    for type in sorted(dataTypes, key = typeSort):
        lookbackDay = dates[-1-dataTypes[type]['lookbackDays']]

        if type[:6] == 'Total ':
            if type[-6:] == 'Capita':
                data[today]['counties'][key][type] = 0
                if key in counties:
                    rawType = type.replace(' Per Capita', '')
                    data[today]['counties'][key][type] = data[today]['counties'][key][rawType] * 1000000 / counties[key]['population']
            else:
                data[today]['states'][state][type] += data[today]['counties'][key][type]
                data[today][type]                  += data[today]['counties'][key][type]
        else:
            totalType = type.replace('Daily', 'Total')
            subtrahend = data[lookbackDay]['counties'][key][totalType] if key in data[lookbackDay]['counties'] else 0
            data[today]['counties'][key][type] = max(0, (data[today]['counties'][key][totalType] - subtrahend) / dataTypes[type]['lookbackDays'])

for type in sorted(dataTypes, key = typeSort):
    totalType = type.replace('Daily', 'Total')
    rawType = type.replace(' Per Capita', '')

    for i in range(21, len(dates)):
        today = dates[i]
        lookbackDay = dates[i-dataTypes[type]['lookbackDays']]

        if type[:6] == 'Daily ' and type[-6:] != 'Capita':
            for state in data[today]['states']:
                subtrahend = data[lookbackDay]['states'][state][totalType] if state in data[lookbackDay]['states'] else 0
                data[today]['states'][state][type] = max(0, (data[today]['states'][state][totalType] - subtrahend) / dataTypes[type]['lookbackDays'])
            data[today][type] = max(0, (data[today][totalType] - data[lookbackDay][totalType]) / dataTypes[type]['lookbackDays'])

        if type[-6:] == 'Capita':
            for state in data[today]['states']:
                data[today]['states'][state][type] = data[today]['states'][state][rawType] * 1000000 / states[state]['population']
            data[today][type] = data[today][rawType] * 1000000 / totalPopulation

        if type[:6] == 'Daily ':
            altType = type.replace('Cases', 'Deaths') if type.split(' ')[1] == 'Cases' else type.replace('Deaths', 'Cases')
            lookbackDays = dataTypes[altType]['lookbackDays']
            data[today][type + ' for ' + altType.split(' ')[1]] = max(0, (data[today][totalType] - data[dates[i-lookbackDays]][totalType]) / lookbackDays)

missingList = sorted(filter(lambda x: x[2:] != ':Unknown', list(missing)))
if len(missingList):
    for key in missingList:
        print('Missing', key)
#    exit()

# --------------------------------------------------- Build Videos --------------------------------------------------- #

for type in videoTypes:
    videoTypes[type]['frameOffset'] = framesPerDay // 2 + 1 - (dates.index('2020-'+videoTypes[type]['startDate']) - 1) * framesPerDay
    videoTypes[type]['title']  = type.replace('Capita', 'Million People').replace('County ', '').replace('State ', '')
    if type.split(' ')[2] == 'Cases':
        videoTypes[type]['circles'] = 'red'
        videoTypes[type]['labels'] = 'black'
    else:
        videoTypes[type]['circles'] = 'black'
        videoTypes[type]['labels'] = 'aqua'

with open('static/map.html', 'r') as mapFile:
    map = mapFile.read()

def weightedAverage(num1, num2, fraction):
    return num2*fraction + num1*(1-fraction)

def roundHalfUp(num):
    return floor(num) if num%1<.5 else ceil(num)

def formatNum(num):
    return f'{num:,}'

def buildHtml(day1, day2, type, numer, denom):
    day1 = day1 or day2
    day2 = day2 or day1
    date = day1 if 2*numer<denom else day2
    dataType = type.replace('County ', '').replace('State ', '')
    fraction = numer/denom

    html = map

    if type.split(' ')[1] == 'County':
        for county in sorted(set(data[day1]['counties']) | set(data[day2]['counties'])):
            if county not in missing:
                numDay1 = data[day1]['counties'][county][dataType] if county in data[day1]['counties'] else 0
                numDay2 = data[day2]['counties'][county][dataType] if county in data[day2]['counties'] else 0
                numFinal = weightedAverage(numDay1, numDay2, fraction)
                if numFinal:
                    r = sqrt(numFinal) * videoTypes[type]['scale'] / 100
                    html += '<circle cx="' + str(counties[county]['x']) + '" cy="' + str(counties[county]['y']) + '" r="' + str(r) + '" class="' + videoTypes[type]['circles'] + '"></circle>\n'
        html += '\n</svg>\n\n'

    for state in sorted(set(data[day1]['states']) | set(data[day2]['states'])):
        numDay1 = data[day1]['states'][state][dataType] if state in data[day1]['states'] else 0
        numDay2 = data[day2]['states'][state][dataType] if state in data[day2]['states'] else 0
        numFinal = weightedAverage(numDay1, numDay2, fraction)
        if type.split(' ')[1] == 'County':
            if roundHalfUp(numFinal) > 0:
                html += '<div class="point svelte-3fv2ao" style="left: '+ str(states[state]['labelx']) + '%; top: ' + str(states[state]['labely']) + '%">'
                html += '<div class="labeled-count svelte-1krny27" style="top: -0.65em;">'
                html += '<span class="label ' + videoTypes[type]['labels'] + '">' + states[state]['displayName'] + '</span><span class="count ' + videoTypes[type]['labels'] + '">' + formatNum(roundHalfUp(numFinal)) + '</span></div></div>\n'
        elif state not in ['PR', 'VI', 'GU', 'MP'] and numFinal > 0:
            r = sqrt(numFinal) * videoTypes[type]['scale'] / 100
            html += '<circle cx="' + str(states[state]['x']) + '" cy="' + str(states[state]['y']) + '" r="' + str(r) + '" class="' + videoTypes[type]['circles'] + '"></circle>\n'

    if type.split(' ')[1] == 'State':
        html += '\n</svg>\n\n'

    html += '\n<div class="point svelte-3fv2ao" style="left: 45%; top: 4%; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold; position: absolute; width: 100%; left: -50%">' + videoTypes[type]['title'] + '</span></div>\n'
    if type[:6] == 'Daily ':
        html += '\n<div class="point svelte-3fv2ao" style="left: 45%; top: 7.5%; text-align: center"><span class="label" style="font-size: 1.25em; font-weight: bold; position: absolute; width: 100%; left: -50%">Rolling ' + str(dataTypes[dataType]['lookbackDays']) + '-Day Average</span></div>\n'
    html += '\n<div class="point svelte-3fv2ao" style="left: 77.7%; top: 4%; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold; position: absolute; width: 100%; left: -50%">' + monthMap[int(date[5:7])] + str(int(date[8:10])) + '</span></div>\n'
    html += '<div class="point svelte-3fv2ao" style="left: 64%; top: 9%; width: 200px; text-align: center"><span class="label black" style="font-size: 2em">Cases</span><span class="count red" style="font-size: 2em">'    + formatNum(roundHalfUp(weightedAverage(data[day1][dataTypes[dataType]['cases']],  data[day2][dataTypes[dataType]['cases']],  fraction))) + '</span></div>\n'
    html += '<div class="point svelte-3fv2ao" style="left: 79%; top: 9%; width: 200px; text-align: center"><span class="label black" style="font-size: 2em">Deaths</span><span class="count black" style="font-size: 2em">' + formatNum(roundHalfUp(weightedAverage(data[day1][dataTypes[dataType]['deaths']], data[day2][dataTypes[dataType]['deaths']], fraction))) + '</span></div>\n\n</div></div>'

    return html

def deleteFile(filename):
    try: os.remove(filename)
    except: pass

def buildFiles(newHtml, htmlFilename, imageFilename, frameFilename, frame, dailyFrame, type):
    global driver

    if (frame > 0 or not dailyFrame) and '2019' not in htmlFilename:
        try:
            with open(htmlFilename, 'r') as oldFile:
                oldHtml = oldFile.read()
        except:
            oldHtml = ''
        if newHtml != oldHtml:
            deleteFile(imageFilename)
            with open(htmlFilename, 'w') as newFile:
                newFile.write(newHtml)

    if frame > 0:
        if not os.path.exists(imageFilename):
            deleteFile(frameFilename)

            if not driver:
                driver = webdriver.Chrome('chromedriver', options = options)
            driver.get('file:///' + os.getcwd().replace('\\','/') + '/' + htmlFilename)
            driver.save_screenshot('images/temp.png')

            image = Image.open('images/temp.png')
            image = image.crop((10, 30, 1610, 1030))
            image.save(imageFilename)
            os.remove('images/temp.png')
        if not os.path.exists(frameFilename):
            if not lastValues[type]['modified']:
                lastValues[type]['modified'] = True
                with open('lastValues.json', 'w') as valuesFile:
                    json.dump(lastValues, valuesFile)
            copyfile(imageFilename, frameFilename)

fps = framesPerDay * daysPerSecond

try:
    with open('lastValues.json') as valuesFile:
        lastValues = json.load(valuesFile)
except:
    lastValues = {}

for type in videoTypes:
    if type not in lastValues:
        lastValues[type] = {'params': {}, 'modified': True}

    params = {'framesPerDay': framesPerDay, 'startDate': videoTypes[type]['startDate']}
    if lastValues[type]['params'] != params:
        for filename in os.listdir('frames/' + type):
            os.remove('frames/' + type + '/' + filename)
        lastValues[type]['modified'] = True
        lastValues[type]['params'] = params
        with open('lastValues.json', 'w') as valuesFile:
            json.dump(lastValues, valuesFile)

    for i in range(len(dates)):
        today = dates[i]
        tomorrow = dates[i+1] if i+1<len(dates) else ''
        for j in range(0, framesPerDay):
            if i < 20:
                date = today if 2*j<framesPerDay else tomorrow
                htmlFilename = 'html/' + type + '/' + date + '.000.html'
                imageFilename = 'images/' + type + '/' + date + '.000.png'
            else:
                decimal = f'{j/framesPerDay:0.3f}'[1:]
                htmlFilename = 'html/' + type + '/' + today + decimal + '.html'
                imageFilename = 'images/' + type + '/' + today + decimal + '.png'
            frame = videoTypes[type]['frameOffset'] + (i-1)*framesPerDay + j
            frameFilename = 'frames/' + type + '/frame' + str(frame).zfill(5) + '.png'
            buildFiles(buildHtml(today, tomorrow, type, j, framesPerDay), htmlFilename, imageFilename, frameFilename, frame, j, type)
            if not tomorrow and not j:
                break

    for i in range(frame+1, frame+fps*5+1):
        copyFilename = 'frames/' + type + '/frame' + str(i).zfill(5) + '.png'
        if not os.path.exists(copyFilename) and not lastValues[type]['modified']:
            lastValues[type]['modified'] = True
            with open('lastValues.json', 'w') as valuesFile:
                json.dump(lastValues, valuesFile)
        copyfile(frameFilename, copyFilename)

    videoFilename = videoTypes[type]['index'] + ' ' + type + '.mp4'
    if lastValues[type]['modified'] or not os.path.exists(videoFilename):
        os.system('ffmpeg -f image2 -r ' + str(fps) + ' -i "frames/' + type + '/frame%05d.png" -r ' + str(fps) + ' -c:a copy -c:v libx264 -crf 16 -preset veryslow "' + videoFilename + '" -y')
        lastValues[type]['modified'] = False
        with open('lastValues.json', 'w') as valuesFile:
            json.dump(lastValues, valuesFile)

if driver:
    driver.quit()