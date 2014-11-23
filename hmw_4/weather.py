#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#Polina Morozova 23.11.2014

import os
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

def get_weather_html(ip):
	r = requests.get('http://api.hostip.info/get_json.php?ip=%s' % ip)
	loc = r.json()
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?mode=html&q=%s,%s' %(loc['city'],loc['country_code']))
	return r.text

class WeatherServer(BaseHTTPRequestHandler):
	def do_GET(self):
		ip = self.headers['X-Forwarded-For'].split(',')[-1]
		text = get_weather_html(ip)
		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		self.end_headers()
		self.wfile.write(bytes(text, 'UTF-8'))
		
def main ():
	port = int(os.environ.get("PORT", 5000))
	server_address = ('0.0.0.0', port)
	httpd = HTTPServer(server_address, WeatherServer)
	httpd.serve_forever()
	
if __name__ == '__main__':
	main()
	