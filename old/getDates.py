import os

for filename in os.listdir('originals/'):
    if filename[-5:] == '.html':
        text = open('originals/' + filename, 'r', encoding="utf8").read()
        index = text.find('<iframe src="https://web.archive.org/web/')
        timestamp = text[index+41:index+55]
        print(filename[5:12], timestamp[4:6] + '-' + timestamp[6:8] + ' ' + timestamp[8:10] + ':' + timestamp[10:12] + ':' + timestamp[12:14])