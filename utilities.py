from os import listdir, remove
import json
import string, random

URL = '127.0.0.1'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './uploads/'
VERSION = '0.0.1 ALPHA'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateFilename(length = 7):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def generateToken(length = 16):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def checkToken(token):
    with open('database.json', 'r') as database:
        data = json.load(database)

        if token in data:
            return True
        else:
            return False

def checkAdmin(token):
    with open('database.json', 'r') as database:
        data = json.load(database)

        if data[token]['admin'] == True:
            return True
        else:
            return False

def getUsername(token):
    with open('database.json', 'r') as database:
        data = json.load(database)
        username = data[token]['username']
        return username

def addUpload(token, upload):
    with open('database.json', 'r') as database:
        data = json.load(database)
        data[token]['uploads'].append(upload)
        open('database.json', 'w').write(json.dumps(data, indent=2))

def removeUploads(token):
    with open('database.json', 'r') as database:
        data = json.load(database)
        data[token]['uploads'].clear()
        open('database.json', 'w').write(json.dumps(data, indent=2))

def deleteAll():
    directory = './uploads'
    for file in listdir(directory):
        remove(f'{directory}/{file}')

    with open('database.json', 'r') as database:
        data = json.load(database)
        for token in data:
            data[token]['uploads'].clear()
            open('database.json', 'w').write(json.dumps(data, indent=2))

def userCount():
    with open('database.json', 'r') as database:
        data = json.load(database)
        usercount = len(data)
        return usercount

def imageCount():
    imagecount = len(listdir('./uploads'))
    return imagecount

def randomImage():
    return random.choice(listdir(UPLOAD_FOLDER))