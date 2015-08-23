import math
import numpy
from location import read_all_from_disk
import codecs
from lxml import html
import requests
import re
from unidecode import unidecode
from date_extract import get_date_ranges

file_name = 'scraped-data.txt'
to_write = 'matched-data.txt'
search_url = 'https://www.google.com/search?q='

google_link_entity = '//h3[@class="r"]/a/@href'

page_title_entity = '//h1[@id="HEADING"]/text()'
duration_entity = '//b[text() = "Recommended length of visit:"]/../text()'
rating_entity = '//ul[@class="barChart"]/li/*[1]/text()'

open_closed_entity = '//span[@class="days"]/..'
days_entity = 'span[@class="days"]/text()'
times_entity = 'span[@class="hours"]/text()'

heading_rating = '//div[@class="heading_ratings"]//img[@property="ratingValue"]/@content'
heading_types = '//div[@class="heading_details"]//div[@class="detail"]/a/text()'

certificate_of_excellence_entity = '//div[@class="coeBadgeDiv"]'

empty_ratings = ["","","","",""]

empty_details = ["", "", empty_ratings, [], "", [], ""]


def find_details_from_location(location, event_type):
	print(location.name)
	search_text = search_url+location.country+"+"+location.city+"+"+unidecode(location.name)+"+tripadvisor"
	search_page = requests.get(search_text)
	tree = html.fromstring(search_page.text)
	filtered_links = filter_links_by_regex(tree.xpath(google_link_entity), event_type.tripadvisor_regex)
	if(len(filtered_links) > 0):
		first_link = filtered_links[0]
		print(first_link)
		session = requests.Session()
		session.max_redirects = 200
		next_page = session.get(first_link)
		next_tree = html.fromstring(next_page.text)
		return parse_tree(next_tree)
	else:
		print("no link")
		return empty_details

def parse_tree(tree):
	header = parse_header(tree)
	duration = parse_duration(tree)
	ratings = parse_ratings(tree)
	hrs = parse_hours(tree)
	net_rating = parse_net_rating(tree)
	types = parse_types(tree)
	coe = parse_coe(tree)
	print("found:\t\t"+header)
	print("types:\t\t"+str(types))
	print("net rating:\t"+net_rating)
	print("duration:\t"+duration)
	print("ratings:\t"+str(ratings))
	print("excellence:\t"+str(coe))
	return [header, duration, ratings, hrs, net_rating, types, coe]

def parse_header(tree):
	return tree.xpath(page_title_entity)[1].replace("\n", "")

def parse_duration(tree):
	duration_raw = tree.xpath(duration_entity)
	duration = ""
	if(len(duration_raw) >= 1):
		duration = duration_raw[1].replace("\n", "")
		if(duration == " "):
			duration = " < 1 hour"
	return duration_adjust(duration)

def parse_ratings(tree):
	ratings_raw = tree.xpath(rating_entity)
	ratings = []
	if(len(ratings_raw) == 5):
		ratings = ratings_raw
	else:
		ratings = empty_ratings
	return ratings

def parse_net_rating(tree):
	net_rating = ""
	find_net = tree.xpath(heading_rating)
	if(len(find_net) == 1):
		net_rating = find_net[0]
	return net_rating

def parse_types(tree):
	return tree.xpath(heading_types)

def parse_coe(tree):
	coe = False
	if(len(tree.xpath(certificate_of_excellence_entity)) > 0):
		coe = True
	return coe

def parse_hours(tree):
	open_closed = tree.xpath(open_closed_entity)
	open_ranges = []
	for index, record in enumerate(open_closed):
		time = record.xpath(times_entity)[0].replace("\n", "")
		days = ""
		raw = record.xpath(days_entity)[0].replace("\n", "")
		if(raw == ''):
			days = open_closed[index - 1].xpath(days_entity)[0].replace("\n","")
		else:
			days = raw
		print(days + " : " + time)
		open_ranges = open_ranges + get_date_ranges(days, time)
	return open_ranges

def filter_links_by_regex(links, link_regex):
	new_links = []
	for link in links:
		results = re.findall(link_regex, link)
		if(len(results) > 0):
			new_links.append(results[0])
	return new_links

def duration_adjust(duration_string):
	hours = re.findall('\d', duration_string)
	num_hours = []
	for hour in hours:
		num_hours.append(float(hour))
	if(len(hours) == 1):
		less_than = re.findall('<', duration_string)
		if(less_than == 1):
			return str(int((num_hours[0] * 60) - 30))
		else:
			return str(int((num_hours[0] * 60) + 30))
	elif(len(hours) > 1):
		return str(int(numpy.mean(num_hours) * 60))
	else:
		return ""

def match_all_from_file_to_file(file, write_file):
	print("starting...")
	all_locations = read_all_from_disk(file)
	total_locations = len(all_locations)
	print("matching "+str(total_locations)+" locations...")
	all_details = []
	for index, location in enumerate(all_locations):
		print("getting details for location: "+str(index+1)+"/"+str(total_locations))
		details = find_details_from_location(location)
		details.insert(0, location.name)
		all_details.append(details)
	print("writing to disk...")
	write_to_file(write_file, all_details)
	print("done.")

def write_to_file(file, all_details):
	f = open(file, 'a')
	for detail in all_details:
		f.write(details_to_string(detail))
	f.close()

def details_to_string(details):
	return details[0].encode('utf-8')+"\t"+details[1]+"\t"+details[2]+"\t"+details[3][0]+"\t"+details[3][1]+"\t"+details[3][2]+"\t"+details[3][3]+"\t"+details[3][4]+"\t"+details[5]+"\t"+str(details[4])+"\t"+str(details[6])+"\t"+str(details[7])+"\n"

