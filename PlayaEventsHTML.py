#!/usr/bin/python

import urllib2
import json
import codecs
import pprint
import time,datetime
import latexcodec

#req = urllib2.urlopen('http://playaevents.burningman.com/api/0.2/2013/event/')
req = codecs.open('events.json', encoding='utf-8')

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

prev_day = 0
prev_all_day = None
out = None

# index = codecs.open('index.html', encoding='utf-8', mode='w')
# index.write('<html><body><ul>')

for e in events:
    if  e['start_time'].day != prev_day:
        prev_day = e['start_time'].day
        if out:
            out.write('\\end{document}\n')
            out.close()

        # Create a new file
        out = codecs.open(e['start_time'].strftime("%m-%d-%A") + '.tex', encoding='utf-8', mode='w')
        out.write('\\input{playa_events.tex}\n')
        out.write('\\begin{document}')
        out.write('\\tiny')
        out.write('\\chead{' + e['start_time'].strftime("%A %m/%d") + '}\n')
        

    when =  'All Day' if e['all_day'] else e['start_time'].strftime("%H:%M") + " - " + e['end_time'].strftime("%H:%M")
    what =  e['title'].encode("latex", errors='replace')
    who =   e['hosted_by_camp']['name'].encode("latex", errors='replace') if 'hosted_by_camp' in e else '~'
    where = e['other_location'].encode("latex", errors='replace') 
    why =   e['description'].encode("latex", errors='replace')

    out.write(r"""
\begin{tabular}{ p{1in} p{2.2in} }
    \textbf{%s} & \textbf{%s} \\
    %s \newline %s & %s \\
    \hline 
\end{tabular}
    """ % (when, what, who, where, why))
    # out.write('\\event')
    # if e['all_day']:
    #     out.write('{All Day}')
    # else:
    #     out.write('{' + e['start_time'].strftime("%H:%M") + " - " + e['end_time'].strftime("%H:%M") + '}')
    # out.write('{' + e['title'].encode("latex", errors='replace') + '}')
    # if 'hosted_by_camp' in e:
    #     out.write('{' + e['hosted_by_camp']['name'].encode("latex", errors='replace') + '}')
    # out.write('{' + e['other_location'].encode("latex", errors='replace') + '}')
    # out.write('{' + e['print_description'].encode("latex", errors='replace') + '}\n')
     
#index.write('</ul></body></html>')
