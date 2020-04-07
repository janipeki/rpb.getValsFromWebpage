# peter@debian:~/tmp/corona$ egrep -i "main_table_countries_today|main_table_countries_yesterday|href=.country/iraq" index.html.4 

import re
import redis
import sys
import time
import configparser

import getValues
import persistValues

def getConfig():
    configParser = configparser.RawConfigParser()
    configFilePath = r'rpb.e-paper.showdata.config'
    configParser.read(configFilePath)
    return configParser

def searchForSection(webpage, startIndicator):
    for line in rd:
        if re.search(startIndicator, line):
            return True

################### M A I N ##########################################################################################
# The file where the web page is stored must be given as only parameter:
if len(sys.argv) != 2:
    raise ValueError('Please provide the file name of the webpage.')
     
webpage = sys.argv[1]

count = {}
ticks = int(time.time())
# Get the config to be able to crypt this in git
configParser = getConfig()
rhost = configParser.get('redis', 'rhost')
password = configParser.get('redis', 'password')
rhost = redis.Redis(host=rhost, port=6379, db=0, password=password)


# Get the data from the web page
with open (webpage) as rd:
    searchForSection(rd, 'main_table_countries_today')
    for line in rd:
        # Search the start of the section where the data shall be scratched from
        if re.search('main_table_countries_yesterday', line):
            break
        # Get the data for the world
        if re.match('<td style="text-align:left;">World</td>', line):
            infected = rd.readline().split('>')[1].split('<')[0]
            infecnew = rd.readline().split('>')[1].split('<')[0]
            deceased = rd.readline().split('>')[1].split('<')[0]
            deceanew = rd.readline().split('>')[1].split('<')[0]
            newvalues = {'Infec': infected, 'Newinf': infecnew, 'Deceas': deceased, 'Newdec': deceanew}
            valuesfornew = { 'World': str(newvalues)}
            print ('World: ' + str(newvalues), type(newvalues))
            worldnow = 'World:' + str(ticks)
            if not persistValues.addKey(rhost, 'World', valuesfornew):
                print ('World: ' + str(valuesfornew))
            if not persistValues.addKey(rhost, worldnow, newvalues):
                print ('worldnow: ' + str(valuesfornew))

        # Get the data for each country
        if re.search('href="country/', line):
            infected = "0"
            infecnew = "0"
            deceased = "0"
            deceanew = "0"
            countryLine = line

            # Get the new values for this country
            country = line.split('>')[2].split('<')[0]
            infected = getValues.getValue('(?<=">)[a-z,0-9+ ]*', rd.readline(), '0').replace(',', '.').replace(' ', '')
            infecnew = getValues.getValue('(?<=">)[a-z,0-9+ ]*', rd.readline(), '0').replace(',', '.').replace(' ', '')
            deceased = getValues.getValue('(?<=">)[a-z,0-9+ ]*', rd.readline(), '0').replace(',', '.').replace(' ', '')
            line = rd.readline()
            deceanew = getValues.getValue('(?<=right;">)[a-z,0-9+ ]*', rd.readline(), '0').replace(',', '.').replace(' ', '')
            newvalues = {'Infec': infected, 'Newinf': infecnew, 'Deceas': deceased, 'Newdec': deceanew}
            print ('New values for ' + country + ': ', str(newvalues))

            # Get the old values for this country
	    # The structure of the values of a country is a nested dict:
	    # country := {<country name>: {<param1> = <value1>, <param2> = <value2>, <param3> = <value3>, <param4> = <value4>}
            oldvaluesRedis = rhost.hgetall(country)
            if oldvaluesRedis:
                try:
                    oldvalues = str(oldvaluesRedis.items()).split(':')
        
                    infected = oldvalues[1].split('\'')[1].replace(' ', '')
                    infecnew = oldvalues[2].split('\'')[1].replace(' ', '')
                    deceased = oldvalues[3].split('\'')[1].replace(' ', '')
                    deceanew = oldvalues[4].split('\'')[1].replace(' ', '')
                except NameError:
                    infected = "0"
                    infecnew = "0"
                    deceased = "0"
                    deceanew = "0"
            else: 
                infected = "0"
                infecnew = "0"
                deceased = "0"
                deceanew = "0"
            oldvalues = {'Infec': infected, 'Newinf': infecnew, 'Deceas': deceased, 'Newdec': deceanew}
            print ('Old values for ' + country + ': ', str(oldvalues))

	    # Compare the old and the new values and persist if different
            if oldvalues:
                if persistValues.isnew(country, oldvalues, newvalues):
                    print ('New values for ' + country + ': ' + str(newvalues))
                    print ('Old values for ' + country + ': ' + str(oldvalues))
                    valuesfornew = { country: str(newvalues)}
                    if not persistValues.addKey(rhost, 'NewCounts', valuesfornew):
                        print ('NewCounts: ' + countryLine)
                    if not persistValues.addKey(rhost, 'NewLog:' + str(ticks), valuesfornew):
                        print ('NewLog: ' + countryLine)
                    if not persistValues.deleteEntries(rhost, country):
                        print ('CountryLine: ' + country)
                    if not persistValues.addKey(rhost, country, valuesfornew):
                        print ('Values for Country: ' + country + countryLine)
            else:
                if not persistValues.addKey(rhost, country, valuesfornew):
                    print ('Values for Country: ' + country + countryLine)
            count = {}

