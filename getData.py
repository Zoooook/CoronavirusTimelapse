import urllib.request
import codecs
import csv
import json

stateMap = {
    'Guam':                     'GU',
    'Northern Mariana Islands': 'MP',
    'Virgin Islands':           'VI',

    'Alabama':                  'AL',
    'Alaska':                   'AK',
    'Arizona':                  'AZ',
    'Arkansas':                 'AR',
    'California':               'CA',
    'Colorado':                 'CO',
    'Connecticut':              'CT',
    'Delaware':                 'DE',
    'District of Columbia':     'DC',
    'Florida':                  'FL',
    'Georgia':                  'GA',
    'Hawaii':                   'HI',
    'Idaho':                    'ID',
    'Illinois':                 'IL',
    'Indiana':                  'IN',
    'Iowa':                     'IA',
    'Kansas':                   'KS',
    'Kentucky':                 'KY',
    'Louisiana':                'LA',
    'Maine':                    'ME',
    'Maryland':                 'MD',
    'Massachusetts':            'MA',
    'Michigan':                 'MI',
    'Minnesota':                'MN',
    'Mississippi':              'MS',
    'Missouri':                 'MO',
    'Montana':                  'MT',
    'Nebraska':                 'NE',
    'Nevada':                   'NV',
    'New Hampshire':            'NH',
    'New Jersey':               'NJ',
    'New Mexico':               'NM',
    'New York':                 'NY',
    'North Carolina':           'NC',
    'North Dakota':             'ND',
    'Ohio':                     'OH',
    'Oklahoma':                 'OK',
    'Oregon':                   'OR',
    'Pennsylvania':             'PA',
    'Puerto Rico':              'PR',
    'Rhode Island':             'RI',
    'South Carolina':           'SC',
    'South Dakota':             'SD',
    'Tennessee':                'TN',
    'Texas':                    'TX',
    'Utah':                     'UT',
    'Vermont':                  'VT',
    'Virginia':                 'VA',
    'Washington':               'WA',
    'West Virginia':            'WV',
    'Wisconsin':                'WI',
    'Wyoming':                  'WY',
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
}

missing = {}
dates = ['2020-01-20']
data = {'2020-01-20': {}}
for row in csvData[1:]:
    state = stateMap[row[2]]
    key = state + ':' + row[1]
    if key[-5:] == ' city':
        key = key[:-5] + ' City'
    if key in keyMap:
        key = keyMap[key]
    if row[1] != 'Unknown' and not key in counties:
        missing[key] = True

    today = row[0]
    if dates[-1] != today:
        dates.append(today)
        data[today] = {}
    yesterday = dates[-2]

    if state not in data[today]:
        data[today][state] = {
            'totalCases':  0,
            'newCases':    0,
            'totalDeaths': 0,
            'newDeaths':   0,
        }

    data[today][key] = {
        'totalCases':  int(row[4]),
        'newCases':    int(row[4]),
        'totalDeaths': int(row[5]),
        'newDeaths':   int(row[5]),
    }
    if key in data[yesterday]:
        data[today][key]['newCases']  -= data[yesterday][key]['totalCases']
        data[today][key]['newDeaths'] -= data[yesterday][key]['totalDeaths']
    data[today][state]['totalCases']  += data[today][key]['totalCases']
    data[today][state]['newCases']    += data[today][key]['newCases']
    data[today][state]['totalDeaths'] += data[today][key]['totalDeaths']
    data[today][state]['newDeaths']   += data[today][key]['newDeaths']

missing = sorted(list(missing))
# for key in missing:
#     print(key)

for date in dates:
    print(date)
    for key in data[date]:
        print('   ', key, data[date][key])