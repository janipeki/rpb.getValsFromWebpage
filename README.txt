This project belongs to a project of two micro services:
1. Collect data from an internet page and store in redis
2. Show the data from redis on an raspberry zero with an e-paper display attached.

Here you get part one of this project.

Precondition:
=============
- A redis data base must be available.
- The access to redis is in src/rpb.e-paper.showdata.config of the structure:
[redis]
rhost=<hostname of redis server>
password=<password  for redis server>

The file is encrypted with git-crypt.

Short description:
==================
The web page must be downloaded before running "python3 getValues.py". 
The name of the web page must be provided by the only parameter.
"getValues.sh" shows how to use it.

The data is stored in redis in the keys:
- NewLog: All changed data for all countries with a epoch time stamp in one place.
- NewLog:<epoch>: The last changed data that may be used by a display.
- <country>: All data for each country.

