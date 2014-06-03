weatherAlert
============

a daily text message weather alert.

- uses the weatherunderground API
- currently just sends a few people a text with the daily high, low and conditions for the day.
- currently hard coded to only get data for pittsburgh

to do:
------

- set up a mysql server to hold users sms numbers and zipcodes
- build a page to have people sign up (gather their email and zip)
- add weatherunderground's logo to page
- change .py script to connect to database, get user's zip, hit the api and send them the forecast.
- add a severe weather alert feature
- add a schedule choice
- look into how to get a "stop" reply via sms to unscribe someone
