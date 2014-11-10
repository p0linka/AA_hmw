#!/usr/bin/env python 
#Polina Morozova 10.11.2014
#Generate a CSV file with one million rows

from random import randint, choice

def generate_ik(sex, year, month, day):
	ik = str(getSex(sex,year))
	ik += getYear(year)
	ik += getMonth(month)
	ik += getDay(day)
	ik += getRandom()
	ik += getCheckSum(ik)
	return ik

# 1 numbri defineerimine
def getSex(sex,year):
	#0='male' 
	#1='female'	
	if 1800 <= year <= 1899:
		if sex=='M':
			return 1
		else:
			return 2
	if 1900 <= year <= 1999:
		if sex=='M':
			return 3
		else:
			return 4
	if 2000 <= year <= 2099:
		if sex=='M':
			return 5
		else:
			return 6
	if 2100 <= year <= 2199:
		if sex=='M':
			return 7
		else:
			return 8

# 2 ja 3 numbrite genereemine
def getYear (year):
	return str(year)[2:4]

# 4 ja 5 numbrite genereerimine
def getMonth(month):
	if month < 10:
		return '0%s' % (month)
	else:
		return str(month)
		
# 6 ja 7 numbrite genereerimine
def getDay(day):
	if day < 10:
		return '0%s' % (day)
	else:
		return str(day)
		
# 8-10 numbrite genereerimine
def getRandom():
	random_number = randint(0, 999)
	return ('%s' % (random_number)).zfill(3)

# 11 numbri genereerimine: checksum
def getCheckSum(ik):
	aste_I = [1,2,3,4,5,6,7,8,9,1]
	aste_II = [3,4,5,6,7,8,9,1,2,3]
	total = 0
	
	for num_ik, num_aste_I in zip(ik, aste_I):
		total += int(num_ik)*num_aste_I
	
	a = total % 11
	if a != 10:
		return str(a)
		
	total = 0
	
	for num_ik, num_aste_II in zip(ik, aste_II):
		total += int(num_ik)*num_aste_II
		
	a = total % 11
	if a != 10:
		return str(a)
	return '0'

# random ik genereerimie
def get_random_ik():
	days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] # kuupaevade arv kuudes
	sex = randint(0, 1)
	year = randint(1800, 2199)
	month = randint(1, 12)
	day = randint(1, days[month])
	if month == 2 and year %4 ==0 and year %100 != 0: # leap year
		day = randint(1, 29)
	return generate_ik(sex, year, month, day)

def read_from_names(file_name):
	names = []
	surnames = []
	with open(file_name, "r") as names_file:
		for l in names_file:
			l = l.split(",")
			if len(l) < 2:
				continue
			names.append(l[0].strip())
			surnames.append(l[1].strip())
	return names, surnames
	
def get_random_name(names, surnames):
	return choice(names), choice(surnames)

days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] # kuupaevade arv kuudes
	
def unique_people(names, surnames, n):
	used_ik = set()
	#used_names = set()
	result = set()
	#a = 10000
	for i in range(n):
		sex = choice(['M', 'F'])
		year = randint(1800, 2199)
		month = randint(1, 12)
		day = randint(1, days[month])
		if month == 2 and year %4 ==0 and year %100 != 0: # leap year
			day = randint(1, 29)
		new_ik = generate_ik(sex, year, month, day)
		while new_ik in used_ik:
			new_ik = generate_ik(sex, year, month, day)
		fn, sn = get_random_name(names, surnames)
		#while (fn, sn) in used_names:
		#	fn, sn = get_random_name(names, surnames)
		#used_names.add((fn, sn))
		used_ik.add(new_ik)
		
		result.add((new_ik, sn, fn, sex, '%s.%s.%s' % (day, month, year)))
		#if i == a:
			#print(i)
			#a += a
		
	return result
					
def write_to_csv(file_name, people):
	with open(file_name, "w") as my_file:
		my_file.write("SOCIAL_SECURITY_NUMBER,FORENAME,SURNAME,GENDER,DATE_OF_BIRTH\n")
		for person in people:
			line = "%s,%s,%s,%s,%s\n" % person
			my_file.write(line)
			
	
def main():
	names, surnames = read_from_names("names.txt")
	people = unique_people(names, surnames, 1000000)
	write_to_csv("unique_people.csv", people)


# https://docs.python.org/2/library/__main__.html	
if __name__ == '__main__':
	main()
	#import cProfile
	#cProfile.run('main()', sort='tottime')