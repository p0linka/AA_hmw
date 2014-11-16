#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#Polina Morozova 16.11.2014

import sqlite3
import sys
import re
import datetime

def unescape(line):
	line = line.replace("&quot;", "\"")
	line = line.replace("&apos;", "'")
	line = line.replace("&amp;", "&")
	line = line.replace("&lt;", "<")
	line = line.replace("&gt;", ">")
	line = line.replace("&laquo;", "<<")
	line = line.replace("&raquo;", ">>")
	line = line.replace("&#039;", "'")
	line = line.replace("&#8220;", "\"")
	line = line.replace("&#8221;", "\"")
	line = line.replace("&#8216;", "\'")
	line = line.replace("&#8217;", "\'")
	line = line.replace("&#9632;", "")
	line = line.replace("&#8226;", "-")
	return line

def query_messages(autor, d_low, d_high):
	conn = sqlite3.connect('main.db')
	try:
		c = conn.cursor()
		r = c.execute('SELECT body_xml FROM Messages WHERE author = ? and timestamp >= ? and timestamp < ? order by timestamp asc', (autor, d_low, d_high))
		result=[]
		for row in r: 
			text = re.sub('<[^<]+>', "", str(row[0]))
			text = unescape(text)
			result.append(text)
		return result
	finally:
		conn.close()

def main(argv):
	if len(argv) < 2:
		print ("python fox.py date author")
		return
	date_input=argv[0] # 2014-11-30
	autor = argv [1]
	d = datetime.datetime.strptime( date_input, "%Y-%m-%d" )
	d_low = int(d.timestamp())
	d_high = d_low + 24*60*60*1000
	result = query_messages(autor, d_low, d_high)
	for message in result: 
		print (message)


if __name__ == '__main__':
	main(sys.argv[1:])