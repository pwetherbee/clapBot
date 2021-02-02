import json

myDict = {'hello.mp3':0, 'ok.mp3':0, 'arnold.mp3':0}

path = 'tracker/popularity.txt'

with open(path, 'w') as file:
    file.write(json.dumps({}))
    file.close()

def addIndexToFile(key, path = path):
    with open(path, 'r') as file:
        #print(file.read())
        tempDict = json.loads(file.read())
        #print(tempDict)
        if tempDict.get(key):
            tempDict[key] += 1
        else:
            tempDict[key] = 1  
    with open(path, 'w') as file:
        file.write(json.dumps(tempDict))
        file.close()

def readFile(path = path):
    with open(path, 'r') as file:
        return json.loads(file.read())


addIndexToFile('hello.mp3')

for i in range(11):
    addIndexToFile('hi.mp3')

readFile()

#against pep8 but whatever
def checkTier(plays):
    if plays < 5: return '👶'  
    if plays < 10: return '👨' 
    if plays < 25: return '👴' 
    if plays < 50: return '🥉' 
    if plays < 75: return '🥈'
    if plays < 100: return '🥇'
    if plays < 150: return '💎'
print(checkTier(75))

def assignTier(key):
    return checkTier(readFile()[key])

print(assignTier('hi.mp3'))
