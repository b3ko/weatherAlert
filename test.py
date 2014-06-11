#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText
import urllib2
import json
import MySQLdb
import MySQLdb.cursors
import sys
import config

db = MySQLdb.connect (host = config.host, user = config.user, passwd = config.passwd, db = config.db, cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()
#group by zipcode to reduce api calls (one per zip)
cursor.execute("select zipcode from zipsForUser group by zipcode")
zips = []
rows = cursor.fetchall()
for row in rows :
	zips.append(row['zipcode'])
	
# get the weather per zip
for zip in zips :
	f = urllib2.urlopen('http://api.wunderground.com/api/%s/geolookup/forecast/q/%s.json' % (config.key, zip))
	json_string = f.read()
	parsed_json = json.loads(json_string)
	high = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
	low = parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
	conditions = parsed_json['forecast']['simpleforecast']['forecastday'][0]['conditions']
	day = parsed_json['forecast']['simpleforecast']['forecastday'][0]['date']['weekday_short']
	location = parsed_json['location']['city']
	f.close()
# get users for this zip
	cursor.execute("select concat(u.mobile, '@', cl.domain) as number from carrier_lkp cl \
		left outer join users u on u.carrier_id = cl.carrier_id \
		left outer join zipsForUser z on z.user_id = u.user_id \
		where z.zipcode = %s and isActive = 1" % zip)
	recipients = []
	rows = cursor.fetchall()
	for row in rows :
		recipients.append(row['number'])

	# set the message's attributes
	msg = MIMEText("Forecast: %s, High: %s, Low: %s" % (conditions, high, low))
	msg['Subject'] = '%s forecast for %s' % (location, day)
	msg['From'] = 'mail@atownrobots.com'
	msg['To'] = ', '.join( recipients )

	# send the message:
	s = smtplib.SMTP('mail.atownrobots.com', 587)
	s.login('mail@atownrobots.com', config.password)
	s.sendmail(msg['from'], recipients, msg.as_string())
	s.quit()
db.close()