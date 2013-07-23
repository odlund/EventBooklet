#!/usr/bin/python

import urllib2
import json
import codecs
import pprint
import time,datetime
req = urllib2.urlopen('http://playaevents.burningman.com/api/0.2/2013/event/')

# req = codecs.open('events.json', encoding='utf-8')
data = req.read()
json_data = json.loads(data)

pp = pprint.PrettyPrinter(indent=4)

events = []
time_format = "%Y-%m-%d %H:%M:%S"

i = 0;
for e in json_data:
    for o in e['occurrence_set']:
        event = {}
        t = time.strptime(o['start_time'], time_format)
        event['start_time'] = datetime.datetime(*t[:6])
        t = time.strptime(o['end_time'], time_format)
        event['end_time'] = datetime.datetime(*t[:6])
        event['title'] = e['title']
        event['print_description'] = e['print_description']
        event['description'] = e['description']
        event['all_day'] = e['all_day']
        if 'hosted_by_camp' in e:
            event['hosted_by_camp'] = e['hosted_by_camp']
        event['other_location'] = e['other_location']
        events.append(event)

# pp.pprint(events)
events = sorted(events, key=lambda event: event['all_day'], reverse=True)
events = sorted(events, key=lambda event: event['start_time'])
# pp.pprint(events)

#{   'all_day': False,
#       'description': u'Not yet ready for Center Camp Stage prime time? Our Open Mic is waiting for you to sign up and give it your all on our mini-stage. Sign up early!',
#       'end_time': datetime.datetime(2011, 9, 1, 21, 0),
#       'hosted_by_camp': {   u'id': 3492, u'name': u'Cartoon Commune'},
#       'other_location': u'',
#       'start_time': datetime.datetime(2011, 9, 1, 19, 0),
#       'title': u'Open Mic'},

prev_day = 0
prev_all_day = None
out = None

index = codecs.open('index.html', encoding='utf-8', mode='w')
index.write('<html><body><ul>')

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
        out.write('    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
        out.write('    <link rel="stylesheet" href="style.css" type="text/css" media="screen"/>\n')
        out.write('    <link rel="stylesheet" href="style.css" type="text/css" media="print"/>\n')
        out.write('    <title>' + e['start_time'].strftime("%A %m/%d") + '</title>\n')
        out.write('  </head>\n')
        out.write('  <body>\n')
        out.write('<h1>' + e['start_time'].strftime("%A %m/%d") + "</h1>")

    out.write('<div><table>\n')
    out.write('  <tr>\n')
    out.write('    <td class="when">')
    if e['all_day']:
        out.write('All Day')
    else:
        out.write(e['start_time'].strftime("%H:%M") + " - " + e['end_time'].strftime("%H:%M"))
    out.write('</td>\n    <td class="what">' + e['title'] + '</td>\n')
    out.write('  </tr>\n  <tr>\n')
    out.write('    <td class="where">')
    if 'hosted_by_camp' in e:
        out.write(e['hosted_by_camp']['name'] + '<br/>')
    out.write(e['other_location'])
    out.write('</td>\n')
    
    out.write('    <td class="why">' + e['description'] + '</td>\n')
    out.write('  </tr>')
    out.write('</table></div>\n')
   
index.write('</ul></body></html>')
