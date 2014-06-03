#!/usr/bin/python
import config
import smtplib
from email.mime.text import MIMEText
import urllib2
import json

recipients = config.users
# get the data
f = urllib2.urlopen('http://api.wunderground.com/api/%s/forecast/q/PA/pittsburgh.json' % config.key)
json_string = f.read()
parsed_json = json.loads(json_string)
high = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
low = parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
conditions = parsed_json['forecast']['simpleforecast']['forecastday'][0]['conditions']
day = parsed_json['forecast']['simpleforecast']['forecastday'][0]['date']['weekday_short']
f.close()

# set the message's attributes
msg = MIMEText("Forecast: %s, High: %s, Low: %s" % (conditions, high, low))
msg['Subject'] = 'Pittsburgh forecast for %s' % day
msg['From'] = 'mail@atownrobots.com'
msg['To'] = ', '.join( recipients )

# send the message:
s = smtplib.SMTP('mail.atownrobots.com', 587)
s.login('mail@atownrobots.com', config.password)
s.sendmail(msg['from'], recipients, msg.as_string())
s.quit()