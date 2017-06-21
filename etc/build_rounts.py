# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on May 20, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School
# @reference: http://stackoverflow.com/questions/17756617/finding-an-unknown-point-using-weighted-multilateration


from pymongo import MongoClient, errors, ASCENDING
from core.log import *

start = datetime.datetime.now()
log(NOTICE, u'crawling jackd')
client = MongoClient('localhost', 27017)
db = client['test']

# a = db.ais.find({'lat': 0})
# a = db.ais.remove({'lat': 0})
# # print a.count()
# exit(-1)

distinct_ship_result = db.command({"distinct": "ais", "key": "mmsi"})
distinct_ship_list = distinct_ship_result.values()[1]

steps = []

file = open("ais.js", "w")
file.write("var ais = [\n")
print "total ships: ", str(len(distinct_ship_list))
j = 0
for ship in distinct_ship_list:
    j += 1
    statuses = db.ais.find({'mmsi': ship}).sort('timestamp', ASCENDING)
    num = statuses.count()
    print "total status: ", str(num)
    if num == 1:
        continue
    # for i in range(1, num):
    #     # steps.append({
    #     #     'mmsi': statuses[i -1]['mmsi'],
    #     #     'slat': statuses[i -1]['lat'],
    #     #     'slng': statuses[i]['lon'],
    #     #     'elat': statuses[i]['lat'],
    #     #     'elng': statuses[i]['lon'],
    #     #               })
    #     json = {
    #         'mmsi': statuses[i -1]['mmsi'],
    #         'slat': statuses[i -1]['lat'],
    #         'slng': statuses[i]['lon'],
    #         'elat': statuses[i]['lat'],
    #         'elng': statuses[i]['lon'],
    #                   }
    json = {
        'mmsi': statuses[0]['mmsi'],
        'slat': statuses[0]['lat'],
        'slng': statuses[0]['lon'],
        'elat': statuses[num - 1]['lat'],
        'elng': statuses[num - 1]['lon']
    }
    print j
    print json
    file.write(str(json) + ",\n")
file.write("]")
file.close()
log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass