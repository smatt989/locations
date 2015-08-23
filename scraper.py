from lxml import html
import requests
from location import Location
from location import write_all_locations_to_disk
from name_match import find_details_from_location
from event_type import activity, restaurant, hotel
import os

#country = 'usa'
#city = 'memphis'
file_name = 'scraped-data.txt'

url_root = 'http://www.lonelyplanet.com'

overallElement = '//div[@class="card__mask"]'

linkInElement = 'a/@href'

locationNameOnPage = '//h1/text()'
locationDescriptionOnPage = '//div[@class="ttd__section ttd__section--description"]/p/text()'
latitudeOnPage = '//div/@data-latitude'
longitudeOnPage = '//div/@data-longitude'

def url(country, city):
	return url_root+'/'+country+'/'+city+'/sights.json'

def restaurants_url(country, city):
	return url_root+'/'+country+'/'+city+'/restaurants.json'

def hotels_url(country, city):
	return url_root+'/'+country+'/'+city+'/hotels.json'

def parse_sight_element(element):
	return int(element.replace("(","").replace(")",""))

def parse_location_element(element):
	return element.replace("\n","")

def get_pages(country, city, local_url):
	keep_looking = True
	page_count = 1
	pages = []
	while(keep_looking):
		page = requests.get(local_url+'?page='+str(page_count))
		most_recent_page_text = page.text
		if(most_recent_page_text != ' '):
			if(len(html.fromstring(most_recent_page_text).xpath(overallElement)) > 0):
				print("page: "+str(page_count))
				pages.append(page)
			else:
				keep_looking = False
		else:
			keep_looking = False
		page_count = page_count + 1
	return pages

def parse_page_for_elements(page):
	elements = html.fromstring(page.text).xpath(overallElement)
	return elements

def parse_element_for_location(element, country, city, event_type):
	location_url = url_root+element.xpath(linkInElement)[0]
	location_page = html.fromstring(requests.get(location_url).text)
	location = parse_one_location_page(location_page, country, city, event_type)
	return location

def parse_one_location_page(page, country, city, event_type):
	location_name = parse_location_element(page.xpath(locationNameOnPage)[0])
	location = Location(location_name, country, city, event_type)
	description = ""
	raw_description = page.xpath(locationDescriptionOnPage)
	for p in raw_description:
		description = description + p.replace("\n","")
	location.setDescription(description)
	latitude_raw = page.xpath(latitudeOnPage)
	longitude_raw = page.xpath(longitudeOnPage)
	if(len(latitude_raw) > 0):
		location.setLatitude(float(latitude_raw[0]))
	if(len(longitude_raw) > 0):
		location.setLongitude(float(longitude_raw[0]))
	additional_details = find_details_from_location(location, event_type)
	location.setDuration(additional_details[1])
	location.setRatings(additional_details[2])
	location.setNetRating(additional_details[4])
	location.setHours(additional_details[3])
	location.setTypes(additional_details[5])
	location.setCertificate(additional_details[6])
	return location

def scrape_one_event_type(country, city, url, event_type):
	pages = get_pages(country, city, url)
	all_elements = []
	print("parsing elements...")
	for page in pages:
		all_elements = all_elements + parse_page_for_elements(page)
	all_locations = []
	print("parsing individual locations")
	total_elements = len(all_elements)
	for index, element in enumerate(all_elements):
		print("\n\nparsing location: "+str(index+1)+"/"+str(total_elements))
		all_locations.append(parse_element_for_location(element, country, city, event_type))
	return all_locations

def scrape_full(country, city, file):
	print("starting...")
	local_url = url(country, city)
	restaurant_url = restaurants_url(country, city)
	hotel_url = hotels_url(country, city)

	activities = scrape_one_event_type(country, city, local_url, activity)
	restaurants = scrape_one_event_type(country, city, restaurant_url, restaurant)
	hotels = filter(lambda l: l.longitude != "None"
		, scrape_one_event_type(country, city, hotel_url, hotel))

	all_locations = activities + restaurants + hotels

	if(os.path.isfile(file)):
		os.remove(file)
	write_all_locations_to_disk(all_locations, file)
	print("done.")

#scrape_full('usa', 'chicago')
#scrape_full('china', 'beijing')
#scrape_full('usa', 'new-york-city', file_name)
#scrape_full('china', 'shanghai', file_name)
#scrape_full('france', 'paris', file_name)
#scrape_full('usa', 'chicago', file_name)