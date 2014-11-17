#!/usr/bin/env python 
#Polina Morozova 17.11.2014

from html.parser import HTMLParser
import lxml.html as lxmlhtml
import sqlite3
import datetime
from urllib.request import urlopen


class LinkExtractor(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links=[]
		
	def handle_starttag(self, tag, attrs):
		if tag != "a":
			return
		attrs = dict(attrs)
		self.links.append(attrs['href'])
	
	
def get_title(url):
	try:
		t = lxmlhtml.parse(urlopen(url))
		return (t.find(".//title").text)
	except: 
		return 'No title!'

def get_urls(xml):
	p = LinkExtractor()
	p.feed('<xml>%s</xml>' % (xml))
	return p.links

def print_html(my_file, author, date, urls):
	m = '''
	 <tr>
		<td>%s</td>
		<td><a href="%s">%s</a></td>
		<td>%s</td>
	</tr>'''
	for url in urls:
		title = get_title(url)
		my_file.write(m%(author,url,title,date))
	
def query_messages(my_file):
	conn = sqlite3.connect('main.db')
	try:
		c = conn.cursor()
		r = c.execute("SELECT author,body_xml,timestamp FROM Messages WHERE body_xml like '%<a href=%' " )
		for row in r:
			date = datetime.datetime.fromtimestamp(int (row[2]))
			date = date.strftime('%d.%m.%Y')
			author = str(row[0])
			text = str (row[1])
			urls = get_urls(text)
			print_html (my_file, author,date,urls)
	finally:
		conn.close()

def print_html_start(my_file):
	m = '''<html><head><title>Links</title></head><body>
			<table>
			<th>Person</th>
			<th>URL</th>
			<th>Date</th>'''
	my_file.write(m)
	
def print_html_end(my_file):
	my_file.write('</table> </body> </html>')
		

def main():
	with open('links.html', "w") as my_file:
		print_html_start(my_file) 
		query_messages(my_file)
		print_html_end(my_file)
	

if __name__ == '__main__':
	main()

