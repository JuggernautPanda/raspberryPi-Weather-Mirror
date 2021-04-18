#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  weather_api.py
#  
#  Copyright 2021 root <root@raja-Inspiron-N5110>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from flask import Flask, render_template, request
import RPi.GPIO as GPIO

# import json to load JSON data to a python dictionary
import json,datetime

# urllib.request to make a request to api
import urllib.request
from newsapi import NewsApiClient
#
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   20 : {'name' : 'GPIO 20', 'state' : GPIO.LOW},
   21 : {'name' : 'GPIO 21', 'state' : GPIO.LOW}
   }
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.HIGH)
# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/black")
def black():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('black.html', **templateData)

@app.route("/LED")
def LED():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

@app.route('/', methods =['POST', 'GET'])
def weather():
        if request.method == 'POST':
                city = request.form['city']
        else:
                # for default name hyderabad
                city = 'hyderabad'

        # your API key will come here
        api = "194eb3e095efa8b065997a8872c63fd8"
        newsapi = NewsApiClient(api_key="db2b98850b494edeb364fbbef2a6c371")
        topheadlines = newsapi.get_top_headlines(sources="bbc-news")
        articles = topheadlines['articles']
        myarticles = articles[1]
        titlenews = myarticles['title']
        # source contain json data from api
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api).read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
        #for pin in pins:
        #        pins[pin]['state'] = GPIO.input(pin)
                
        #print(list_of_data)
        # data for variable list_of_data
        data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' '
                                        + str(list_of_data['coord']['lat']),
                "temp": str(int(list_of_data['main']['temp']-273)) + 'c',
                "time":str(datetime.datetime.fromtimestamp(int(list_of_data['dt'])).strftime('%Y-%m-%d %H:%M:%S')),
                "cityname": str(list_of_data['name']),
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "news":str(titlenews),
		#"pins":pins,
                "button1":str("unchecked"),
                "button2": str("checked"),
        }
        print(data)
        return render_template('weather.html', data = data)



if __name__ == '__main__':
        app.run(host='0.0.0.0',debug = True,threaded=True)
