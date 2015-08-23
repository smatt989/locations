import os
from scraper import scrape_full
from data_update import update_data

def upload(country, city):
	print("STARTING FOR: "+country+", "+city)
	raw_file = country+"_"+city+"_full.txt"
	scrape_full(country, city, raw_file)
	updated_file = country+"_"+city+"_updated.txt"
	if(os.path.isfile(updated_file)):
		os.remove(updated_file)
	update_data(raw_file, updated_file)
	print("DONE")
