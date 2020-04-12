import os
import urllib.request
import codecs
import csv
import json
from math import sqrt
from selenium import webdriver
from PIL import Image

try: os.mkdir('html')
except: pass
try: os.mkdir('frames')
except: pass

stateMap = {
    'Guam'                    : {'code': 'GU', 'displayName': '', 'left': '-10', 'top': '-10'},
    'Northern Mariana Islands': {'code': 'MP', 'displayName': '', 'left': '-10', 'top': '-10'},
    'Virgin Islands'          : {'code': 'VI', 'displayName': '', 'left': '-10', 'top': '-10'},

    'Alabama'                 : {'code': 'AL', 'displayName': 'Ala.'  , 'left': '68.802', 'top': '71.966'},
    'Alaska'                  : {'code': 'AK', 'displayName': 'Alaska', 'left': '9.837' , 'top': '85.217'},
    'Arizona'                 : {'code': 'AZ', 'displayName': 'Ariz.' , 'left': '22.387', 'top': '63.429'},
    'Arkansas'                : {'code': 'AR', 'displayName': 'Ark.'  , 'left': '58.912', 'top': '62.516'},
    'California'              : {'code': 'CA', 'displayName': 'Calif.', 'left': '8.285' , 'top': '49.761'},
    'Colorado'                : {'code': 'CO', 'displayName': 'Colo.' , 'left': '33.762', 'top': '45.511'},
    'Connecticut'             : {'code': 'CT', 'displayName': 'Conn.' , 'left': '90.164', 'top': '32.030'},
    'Delaware'                : {'code': 'DE', 'displayName': 'Del.'  , 'left': '87.418', 'top': '43.112'},
    'District of Columbia'    : {'code': 'DC', 'displayName': 'D.C.'  , 'left': '84.784', 'top': '43.994'},
    'Florida'                 : {'code': 'FL', 'displayName': 'Fla.'  , 'left': '80.872', 'top': '86.593'},
    'Georgia'                 : {'code': 'GA', 'displayName': 'Ga.'   , 'left': '76.596', 'top': '71.130'},
    'Hawaii'                  : {'code': 'HI', 'displayName': 'Hawaii', 'left': '31.982', 'top': '91.832'},
    'Idaho'                   : {'code': 'ID', 'displayName': 'Idaho' , 'left': '20.128', 'top': '25.668'},
    'Illinois'                : {'code': 'IL', 'displayName': 'Ill.'  , 'left': '62.597', 'top': '42.323'},
    'Indiana'                 : {'code': 'IN', 'displayName': 'Ind.'  , 'left': '69.221', 'top': '41.697'},
    'Iowa'                    : {'code': 'IA', 'displayName': 'Iowa'  , 'left': '56.056', 'top': '38.288'},
    'Kansas'                  : {'code': 'KS', 'displayName': 'Kan.'  , 'left': '46.639', 'top': '48.776'},
    'Kentucky'                : {'code': 'KY', 'displayName': 'Ky.'   , 'left': '71.014', 'top': '51.587'},
    'Louisiana'               : {'code': 'LA', 'displayName': 'La.'   , 'left': '58.698', 'top': '76.948'},
    'Maine'                   : {'code': 'ME', 'displayName': 'Maine' , 'left': '93.879', 'top': '16.761'},
    'Maryland'                : {'code': 'MD', 'displayName': 'Md.'   , 'left': '86.102', 'top': '42.557'},
    'Massachusetts'           : {'code': 'MA', 'displayName': 'Mass.' , 'left': '96.120', 'top': '27.532'},
    'Michigan'                : {'code': 'MI', 'displayName': 'Mich.' , 'left': '68.261', 'top': '28.078'},
    'Minnesota'               : {'code': 'MN', 'displayName': 'Minn.' , 'left': '53.175', 'top': '20.787'},
    'Mississippi'             : {'code': 'MS', 'displayName': 'Miss.' , 'left': '63.942', 'top': '72.460'},
    'Missouri'                : {'code': 'MO', 'displayName': 'Mo.'   , 'left': '58.628', 'top': '52.435'},
    'Montana'                 : {'code': 'MT', 'displayName': 'Mont.' , 'left': '28.278', 'top': '17.579'},
    'Nebraska'                : {'code': 'NE', 'displayName': 'Neb.'  , 'left': '44.346', 'top': '39.597'},
    'Nevada'                  : {'code': 'NV', 'displayName': 'Nev.'  , 'left': '14.774', 'top': '43.529'},
    'New Hampshire'           : {'code': 'NH', 'displayName': 'N.H.'  , 'left': '91.749', 'top': '25.425'},
    'New Jersey'              : {'code': 'NJ', 'displayName': 'N.J.'  , 'left': '88.770', 'top': '38.342'},
    'New Mexico'              : {'code': 'NM', 'displayName': 'N.M.'  , 'left': '34.067', 'top': '62.357'},
    'New York'                : {'code': 'NY', 'displayName': 'N.Y.'  , 'left': '86.044', 'top': '28.311'},
    'North Carolina'          : {'code': 'NC', 'displayName': 'N.C.'  , 'left': '85.559', 'top': '56.056'},
    'North Dakota'            : {'code': 'ND', 'displayName': 'N.D.'  , 'left': '43.192', 'top': '17.528'},
    'Ohio'                    : {'code': 'OH', 'displayName': 'Ohio'  , 'left': '73.940', 'top': '41.276'},
    'Oklahoma'                : {'code': 'OK', 'displayName': 'Okla.' , 'left': '49.016', 'top': '63.471'},
    'Oregon'                  : {'code': 'OR', 'displayName': 'Ore.'  , 'left': '10.562', 'top': '23.196'},
    'Pennsylvania'            : {'code': 'PA', 'displayName': 'Pa.'   , 'left': '83.444', 'top': '35.860'},
    'Puerto Rico'             : {'code': 'PR', 'displayName': 'P.R.'  , 'left': '95.5'  , 'top': '90.5'  },
    'Rhode Island'            : {'code': 'RI', 'displayName': 'R.I.'  , 'left': '93.770', 'top': '38.144'},
    'South Carolina'          : {'code': 'SC', 'displayName': 'S.C.'  , 'left': '79.358', 'top': '64.315'},
    'South Dakota'            : {'code': 'SD', 'displayName': 'S.D.'  , 'left': '44.584', 'top': '30.590'},
    'Tennessee'               : {'code': 'TN', 'displayName': 'Tenn.' , 'left': '69.876', 'top': '58.795'},
    'Texas'                   : {'code': 'TX', 'displayName': 'Texas' , 'left': '43.431', 'top': '74.315'},
    'Utah'                    : {'code': 'UT', 'displayName': 'Utah'  , 'left': '24.340', 'top': '44.421'},
    'Vermont'                 : {'code': 'VT', 'displayName': 'Vt.'   , 'left': '89.334', 'top': '21.275'},
    'Virginia'                : {'code': 'VA', 'displayName': 'Va.'   , 'left': '82.560', 'top': '50.150'},
    'Washington'              : {'code': 'WA', 'displayName': 'Wash.' , 'left': '12.023', 'top': '12.765'},
    'West Virginia'           : {'code': 'WV', 'displayName': 'W.Va.' , 'left': '78.881', 'top': '46.828'},
    'Wisconsin'               : {'code': 'WI', 'displayName': 'Wis.'  , 'left': '63.102', 'top': '30.758'},
    'Wyoming'                 : {'code': 'WY', 'displayName': 'Wyo.'  , 'left': '32.081', 'top': '32.285'},
}

stateKeys = []
for state in stateMap:
    stateKeys.append(state)
for state in stateKeys:
    stateMap[stateMap[state]['code']] = stateMap[state]

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

response = urllib.request.urlopen('https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/51a3a94e6fc49506549d9cfad8fd567653c2b2a3/slip-map/usa/us_counties_centroids.json')
countyData = json.loads(response.read())

counties = {}
for county in countyData['features']:
    counties[county['properties']['st'] + ':' + county['properties']['displayname']] = {
        'x': 50   + 2.325 * county['geometry']['coordinates'][0],
        'y': 32.1 - 2.345 * county['geometry']['coordinates'][1],
    }

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
        'counties':    {},
        'states':      {},
        'totalCases':  0,
        'newCases':    0,
        'totalDeaths': 0,
        'newDeaths':   0,
    }

for row in csvData[1:]:
    state = stateMap[row[2]]['code']
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
            'counties':    {},
            'states':      {},
            'totalCases':  0,
            'newCases':    0,
            'totalDeaths': 0,
            'newDeaths':   0,
        }
    yesterday = dates[-2]

    if state not in data[today]['states']:
        data[today]['states'][state] = {
            'totalCases':  0,
            'newCases':    0,
            'totalDeaths': 0,
            'newDeaths':   0,
        }

    data[today]['counties'][key] = {
        'totalCases':  int(row[4]),
        'newCases':    int(row[4]),
        'totalDeaths': int(row[5]),
        'newDeaths':   int(row[5]),
    }
    if key in data[yesterday]['counties']:
        data[today]['counties'][key]['newCases']  -= data[yesterday]['counties'][key]['totalCases']
        data[today]['counties'][key]['newDeaths'] -= data[yesterday]['counties'][key]['totalDeaths']
    data[today]['states'][state]['totalCases']  += data[today]['counties'][key]['totalCases']
    data[today]['states'][state]['newCases']    += data[today]['counties'][key]['newCases']
    data[today]['states'][state]['totalDeaths'] += data[today]['counties'][key]['totalDeaths']
    data[today]['states'][state]['newDeaths']   += data[today]['counties'][key]['newDeaths']
    data[today]['totalCases']  += data[today]['counties'][key]['totalCases']
    data[today]['newCases']    += data[today]['counties'][key]['newCases']
    data[today]['totalDeaths'] += data[today]['counties'][key]['totalDeaths']
    data[today]['newDeaths']   += data[today]['counties'][key]['newDeaths']

anyUpdated = False
i = 0
for date in dates:
    i += 1

    month = int(date[5:7])
    day = int(date[8:10])
    html = open('map.html', 'r').read()

    for county in data[date]['counties']:
        if county not in missing:
            r = sqrt(data[date]['counties'][county]['totalCases'])/50
            html += '<circle cx="' + str(counties[county]['x']) + '" cy="' + str(counties[county]['y']) + '" r="' + str(r) + '" class="svelte-12ai9yo"></circle>\n'

    html += '\n</svg>\n\n'

    for state in data[date]['states']:
        html += '<div class="point svelte-3fv2ao" style="left: '+ stateMap[state]['left'] + '%; top: ' + stateMap[state]['top'] + '%">'
        html += '<div class="labeled-count svelte-1krny27" style="top: -0.65em;">'
        html += '<span class="label">' + stateMap[state]['displayName'] + '</span><span class="count">' + str(data[date]['states'][state]['totalCases']) + '</span></div></div>\n'

    html += '\n<div class="point svelte-3fv2ao" style="left: 71.5%; top: 4%; width: 200px; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold">' + monthMap[month] + str(day) + '</span></div>\n'
    html += '<div class="point svelte-3fv2ao" style="left: 64%; top: 9%; width: 200px; text-align: center"><span class="label" style="font-size: 2em">Cases</span><span class="count" style="font-size: 2em">' + str(data[date]['totalCases']) + '</span></div>\n'
    html += '<div class="point svelte-3fv2ao" style="left: 79%; top: 9%; width: 200px; text-align: center"><span class="label" style="font-size: 2em">Deaths</span><span class="count" style="font-size: 2em">' + str(data[date]['totalDeaths']) + '</span></div>\n\n</div></div>'

    htmlFilename = 'html/' + date + '.html'
    imageFilename = 'frames/frame' + str(i).zfill(4) + '.png'

    try:
        with open(htmlFilename, 'r') as oldFile:
            oldHtml = oldFile.read()
    except:
        oldHtml = ''

    lastUpdated = False
    if html != oldHtml:
        lastUpdated = True
        anyUpdated = True

        with open(htmlFilename, 'w') as newFile:
            newFile.write(html)

        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome('chromedriver', options = options)

        driver.get('file:///' + os.getcwd().replace('\\','/') + '/' + htmlFilename)
        driver.save_screenshot(imageFilename)
        driver.quit()

        image = Image.open(imageFilename)
        image = image.crop((10, 30, 1610, 1030))
        image.save(imageFilename)

if lastUpdated:
    for j in range(4):
        i += 1
        image.save('frames/frame' + str(i).zfill(4) + '.png')

if anyUpdated:
    os.system('ffmpeg -f image2 -r 2 -i frames/frame%04d.png -r 2 -c:a copy -c:v libx264 -crf 16 -preset veryslow CoronavirusTimelapse.mp4 -y')

missing = sorted(list(missing))
for key in missing:
    if key[2:] != ':Unknown':
        print('Missing', key)