import redis
import base64

def addKey(rhost, dictionary, values):
    if type(values) == dict:
        print ('addKey for ' + dictionary + ': ' + str(values))
        rhost.delete(dictionary)
        for key, value in values.items():
            retVal = rhost.hset(dictionary, key, value.replace(',', '.').encode('UTF-8'))
            if retVal == 1:
                print ('addKey for ' + dictionary + ': ' + str(values))
                return True
            else:
                print ('ERROR: ' + str(retVal) + ', addKey for ' + dictionary + ': ' + str(values))
                return False

def deleteEntries(rhost, dictionary):
    retVal = rhost.delete(dictionary)
    print ('deleteEntries for value ' + dictionary + ': ' + str(retVal))

def isnew(country, oldvalues, newvalues):

    for newKey, newvalue in newvalues.items():
        if not oldvalues :
            print ('IsNew: oldvalues ist None')
            return True
        elif oldvalues.get(newKey) != newvalues.get(newKey):
            print ('isnew: newvalue for country ' + country + ', key ' + newKey + ': ' + newvalues.get(newKey))
            print ('isnew: oldvalue for country ' + country + ', key ' + newKey + ': ' + oldvalues.get(newKey))
            return True
    return False
