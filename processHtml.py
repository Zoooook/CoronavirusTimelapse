import os

try: os.mkdir('html')
except: pass

def getChunk(text, cursor, strings):
    index = text[cursor[0]:].find(strings[0])
    end = cursor[0] + index
    for i in range(1,len(strings)):
        if index > -1:
            start = end + len(strings[i-1])
            index = text[start:].find(strings[i])
            end = start + index
    if index > -1:
        cursor[0] = end + len(strings[-1])
        return text[start:end]
    return ''

def parseNum(text, string1, string2):
    index1 = text.find(string1)
    if index1 > -1:
        start = index1 + len(string1)
        index2 = text[start:].find(string2)
        if index2 > -1:
            end = start + index2
            num = text[start:end]
            if num.replace(',','').isnumeric():
                return num
    return ''

deathMap = {
    '2020-03-03-4.html': '9',
    '2020-03-04-1.html': '9',
    '2020-03-04-2.html': '9',
    '2020-03-04-3.html': '9',
    '2020-03-04-4.html': '11',
    '2020-03-05-1.html': '11',
    '2020-03-05-2.html': '11',
    '2020-03-05-3.html': '11',
    '2020-03-05-4.html': '12',
}

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

statePositions = {
    'Ala.'  : {'left': '68.802', 'top': '71.966'},
    'Alaska': {'left': '9.837' , 'top': '85.217'},
    'Ariz.' : {'left': '22.387', 'top': '63.429'},
    'Ark.'  : {'left': '58.912', 'top': '62.516'},
    'Calif.': {'left': '8.285' , 'top': '49.761'},
    'Colo.' : {'left': '33.762', 'top': '45.511'},
    'Conn.' : {'left': '90.164', 'top': '32.030'},
    'Del.'  : {'left': '87.418', 'top': '43.112'},
    'D.C.'  : {'left': '84.784', 'top': '43.994'},
    'Fla.'  : {'left': '80.872', 'top': '86.593'},
    'Ga.'   : {'left': '76.596', 'top': '71.130'},
    'Hawaii': {'left': '31.982', 'top': '91.832'},
    'Idaho' : {'left': '20.128', 'top': '25.668'},
    'Ill.'  : {'left': '62.597', 'top': '42.323'},
    'Ind.'  : {'left': '69.221', 'top': '41.697'},
    'Iowa'  : {'left': '56.056', 'top': '38.288'},
    'Kan.'  : {'left': '46.639', 'top': '48.776'},
    'Ky.'   : {'left': '71.014', 'top': '51.587'},
    'La.'   : {'left': '58.698', 'top': '76.948'},
    'Maine' : {'left': '93.879', 'top': '16.761'},
    'Md.'   : {'left': '86.102', 'top': '42.557'},
    'Mass.' : {'left': '96.120', 'top': '27.532'},
    'Mich.' : {'left': '68.261', 'top': '28.078'},
    'Minn.' : {'left': '53.175', 'top': '20.787'},
    'Miss.' : {'left': '63.942', 'top': '72.460'},
    'Mo.'   : {'left': '58.628', 'top': '52.435'},
    'Mont.' : {'left': '28.278', 'top': '17.579'},
    'Neb.'  : {'left': '44.346', 'top': '39.597'},
    'Nev.'  : {'left': '14.774', 'top': '43.529'},
    'N.H.'  : {'left': '91.749', 'top': '25.425'},
    'N.J.'  : {'left': '88.770', 'top': '38.342'},
    'N.M.'  : {'left': '34.067', 'top': '62.357'},
    'N.Y.'  : {'left': '86.044', 'top': '28.311'},
    'N.C.'  : {'left': '85.559', 'top': '56.056'},
    'N.D.'  : {'left': '43.192', 'top': '17.528'},
    'Ohio'  : {'left': '73.940', 'top': '41.276'},
    'Okla.' : {'left': '49.016', 'top': '63.471'},
    'Ore.'  : {'left': '10.562', 'top': '23.196'},
    'Pa.'   : {'left': '83.444', 'top': '35.860'},
    'R.I.'  : {'left': '93.770', 'top': '38.144'},
    'S.C.'  : {'left': '79.358', 'top': '64.315'},
    'S.D.'  : {'left': '44.584', 'top': '30.590'},
    'Tenn.' : {'left': '69.876', 'top': '58.795'},
    'Texas' : {'left': '43.431', 'top': '74.315'},
    'Utah'  : {'left': '24.340', 'top': '44.421'},
    'Vt.'   : {'left': '89.334', 'top': '21.275'},
    'Va.'   : {'left': '82.560', 'top': '50.150'},
    'Wash.' : {'left': '12.023', 'top': '12.765'},
    'W.Va.' : {'left': '78.881', 'top': '46.828'},
    'Wis.'  : {'left': '63.102', 'top': '30.758'},
    'Wyo.'  : {'left': '32.081', 'top': '32.285'},
}

boilerplate = open('boilerplate.html', 'r').read()

for filename in os.listdir('originals/'):
    month = int(filename[5:7])
    day = int(filename[8:10])
    frame = int(filename[11])
    frameIndex = (month*31+day)*4+frame

    text = open('originals/' + filename, 'r', encoding="utf8").read()
    cursor = [0]
    states = {}

    paragraph1 = getChunk(text, cursor, ['<p class="g-body ">', '</p>'])[2:-1]

    circles = []
    while True:
        cx = getChunk(text, cursor, ['<circle cx="', '"'])
        if not cx:
            break
        cx = float(cx)
        cy = float(getChunk(text, cursor, ['cy="', '"']))
        r = float(getChunk(text, cursor, ['r="', '"']))
        skip = False

        if frameIndex <= 391:
            cx = (cx-50)*1.08+50
            cy = cy*1.08+1.706911263
            r *= 7/4
        if frameIndex in [395,396] and round(cx,6) == 13.713056 and round(cy,6) == 7.296820: # fix Washington
            cx = 12.307790654396314
            cy = 5.371074781233531
        if frameIndex <= 398 and round(cx,6) == 1.875461 and round(cy,6) == 27.353114: # fix San Francisco
            cx = 2.9438844722337123
            cy = 27.568193233040574
        if frameIndex in range(392,400) and round(cx,6) == 79.734663 and round(cy,6) == 57.291601: # fix Florida
            cx = 79.63526052896121
            cy = 56.60266344435024
        if frameIndex in range(399,405) and round(cx,6) == 71.888261 and round(cy,6) == 41.453826: # fix Georgia
            cx = 72.01207024960398
            cy = 42.079477155667746
        if frameIndex in [420,421,422] and (round(cx,6) == 59.604496 and round(cy,6) == 53.472522 or round(cx,6) == 63.350684 and round(cy,6) == 51.372097) or\
           frameIndex in range(420,431) and round(cx,6) == 62.581748 and round(cy,6) == 53.588514 or\
           frameIndex in range(427,431) and round(cx,6) == 64.826036 and round(cy,6) == 52.436027: # Fix Louisiana
            skip = True
        if round(cx,6) == 63.428247 and round(cy,6) == 52.174424: # fix New Orleans
            if frameIndex in [420,421,422]:
                r = 1.1608186766243898
            if frameIndex in range(423,427):
                r = 1.2124355652982141
            if frameIndex == 427:
                r = 1.75
            if frameIndex == 428:
                r = 1.8520259177452134
            if frameIndex in [429,430]:
                r = 1.5874507866387544
        if frameIndex <= 428:
            r *= 6/7
        if frameIndex <= 435:
            r *= 5/6
        if frameIndex <= 448:
            r *= 3/5
        if frameIndex <= 459:
            r *= 11/15
        if frameIndex <= 465:
            cx = (cx-50)*0.9851851852+50
            cy = cy*0.9851851852+0.4752875743
        if frameIndex <= 467:
            r *= 5/11

        if not skip:
            circles.append({'cx': str(cx), 'cy': str(cy), 'r': str(r)})

    while True:
        state = getChunk(text, cursor, ['" style="top: auto; height: auto">', '</span>'])
        if not state:
            break
        trash = getChunk(text, cursor, ['<span class="mobile label', '</span>'])
        states[state] = getChunk(text, cursor, ['>', '</span>'])

    paragraph2 = getChunk(text, cursor, ['<p class="g-body ">', '</p>'])[2:-1]
    paragraph3 = getChunk(text, cursor, ['<p class="g-body ">', '</p>'])[2:-1]

    cases = parseNum(paragraph1, ', at least ', ' p') or\
            parseNum(paragraph2, ', at least ', ' p') or\
            parseNum(paragraph3, ', at least ', ' p')
    deaths = parseNum(paragraph1, ', according to a New York Times database, and at least ', ' patients with the virus have died.') or\
             parseNum(paragraph2, ', according to a New York Times database, and at least ', ' patients with the virus have died.') or\
             parseNum(paragraph3, ', according to a New York Times database, and at least ', ' patients with the virus have died.') or\
             deathMap[filename]

    newText = boilerplate

    for circle in circles:
        newText += '<circle cx="' + circle['cx'] + '" cy="' + circle['cy'] + '" r="' + circle['r'] + '" class="svelte-12ai9yo"></circle>\n'

    newText += '\n</svg>\n\n'

    for state in states:
        newText += '<div class="point svelte-3fv2ao" style="left: '+ statePositions[state]['left'] + '%; top: ' + statePositions[state]['top'] + '%">'
        newText += '<div class="labeled-count svelte-1krny27" style="top: -0.65em;">'
        newText += '<span class="label">' + state + '</span><span class="count">' + states[state] + '</span></div></div>\n'

    newText += '\n<div class="point svelte-3fv2ao" style="left: 71.5%; top: 4%; width: 200px; text-align: center"><span class="label" style="font-size: 2em; font-weight: bold">' + monthMap[month] + str(day) + '</span></div>\n'
    newText += '<div class="point svelte-3fv2ao" style="left: 64%; top: 9%; width: 200px; text-align: center"><span class="label" style="font-size: 2em">Cases</span><span class="count" style="font-size: 2em">' + cases + '</span></div>\n'
    newText += '<div class="point svelte-3fv2ao" style="left: 79%; top: 9%; width: 200px; text-align: center"><span class="label" style="font-size: 2em">Deaths</span><span class="count" style="font-size: 2em">' + deaths + '</span></div>\n\n</div></div>'

    newFile = open('html/' + filename.replace('.txt', '.html'), 'w')
    newFile.write(newText)
    newFile.close()