#!/usr/bin/python

import urllib2
import json
import codecs
import pprint
import time,datetime
import dateutil.parser

# Get an API Key from http://api.burningman.com
# Download camp and event data

req = codecs.open('camps.json', encoding='utf-8')
data = req.read()
camp_data = json.loads(data)

req = codecs.open('events.json', encoding='utf-8')
data = req.read()
event_data = json.loads(data)

pp = pprint.PrettyPrinter(indent=4)

camps = {}
events = []
time_format = "%Y-%m-%dT%H:%M:%S"

for c in camp_data:
  uid = c['uid']
  camps[uid] = {}
  camps[uid]['name'] = c['name']
  camps[uid]['location_string'] = c['location_string']

for e in event_data:
    if 'occurrence_set' in e:
      for o in e['occurrence_set']:
        event                      = {}
        event['start_time']        = dateutil.parser.parse(o['start_time'])
        event['end_time']          = dateutil.parser.parse(o['end_time'])
        event['title']             = e['title']
        event['print_description'] = e['print_description']
        event['description']       = e['description']
        event['all_day']           = e['all_day']
        if 'hosted_by_camp' in e:
          event['hosted_by_camp']  = e['hosted_by_camp']
        event['other_location']  = e['other_location']
        event['label']           = e['event_type']['label']
        events.append(event)
    else:
      print "No occurence for " + e['title']

# pp.pprint(events)
events = sorted(events, key=lambda event: event['all_day'], reverse=True)
events = sorted(events, key=lambda event: event['start_time'])
# pp.pprint(events)

prev_day = 0
prev_all_day = None
out = None

index = codecs.open('index.html', encoding='utf-8', mode='w')
index.write('<html><body>')

for e in events:
  if  e['start_time'].day != prev_day:
    prev_day = e['start_time'].day
    if out:
      out.write('</body></html>')
      out.close()

    out = codecs.open(e['start_time'].strftime("%A-%m-%d") + '.html', encoding='utf-8', mode='w')
    index.write('<li><a href="' + e['start_time'].strftime("%A-%m-%d") + '.html">' + e['start_time'].strftime("%A-%m-%d") + '</a></li>')

    out.write('<html>\n')
    out.write('  <head>\n')
    out.write('  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
    out.write('  <link rel="stylesheet" href="style.css" type="text/css" media="screen"/>\n')
    out.write('  <link rel="stylesheet" href="style.css" type="text/css" media="print"/>\n')
    out.write('  <title>' + e['start_time'].strftime("%A %m/%d") + '</title>\n')
    out.write('  </head>\n')
    out.write('  <body>\n')
    out.write('<h1>' + e['start_time'].strftime("%A %m/%d") + "</h1>")

  out.write('<div><table>\n')
  out.write('  <tr>\n')
  out.write('  <td class="when">')
  if e['all_day']:
    out.write('All Day')
  else:
    out.write(e['start_time'].strftime("%H:%M") + " - " + e['end_time'].strftime("%H:%M"))
  out.write('</td>\n  <td class="what">' + e['title'] + '</td>\n')
  out.write('  </tr>\n  <tr>\n')
  out.write('  <td class="where">')

  has_location = False
  if 'hosted_by_camp' in e:
    uid = e['hosted_by_camp']
    if uid in camps:
      out.write(camps[uid]['name'] + '<br/>')
      if camps[uid]['location_string']:
        has_location = True
        out.write(camps[uid]['location_string'] + '<br/>')
  if not has_location:
    out.write(e['other_location'] +'<br/>')
  if e['label'] != 'None':
    out.write(e['label'] + '<br/>')
  out.write('</td>\n')

  out.write('  <td class="why">' + e['description'] + '</td>\n')
  out.write('  </tr>')
  out.write('</table></div>\n')

index.write('</body></html>')
