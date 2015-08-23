import codecs
import sys
import ast
from event_type import event_type_by_name

reload(sys)
sys.setdefaultencoding('utf-8')

class Location:
	def __init__(self, name, country, city, eventType):
		self.name = name
		self.country = country
		self.city = city
		self.description = ''
		self.duration = ''
		self.longitude = "None"
		self.latitude = "None"
		self.fun = "None"
		self.ratings = ["","","","",""]
		self.netrating = "None"
		self.hours = []
		self.types = []
		self.certificate = "None"
		self.eventType = eventType

	def setDescription(self, desc):
		self.description = desc

	def setLongitude(self, lon):
		self.longitude = lon

	def setLatitude(self, lat):
		self.latitude = lat

	def setDuration(self, dur):
		self.duration = dur

	def setRatings(self, rat):
		self.ratings = rat

	def setNetRating(self, rat):
		self.netrating = rat

	def setHours(self, hrs):
		self.hours = hrs

	def setTypes(self, typs):
		self.types = typs

	def setCertificate(self, cert):
		self.certificate = cert

	def toString(self):
		return self.country+'\t'+self.city+'\t'+self.name.encode('utf-8')+'\t'+self.description.encode('utf-8')+'\t'+self.duration+"\t"+str(self.longitude)+"\t"+str(self.latitude)+"\t"+str(self.fun)+"\t"+self.ratings[0]+"\t"+self.ratings[1]+"\t"+self.ratings[2]+"\t"+self.ratings[3]+"\t"+self.ratings[4]+"\t"+self.netrating+"\t"+str(self.hours)+"\t"+str(self.types)+"\t"+str(self.certificate)+"\t"+self.eventType.name

def write_all_locations_to_disk(locations, file):
	f = open(file, 'a')
	for location in locations:
		f.write(location.toString()+'\n')
	f.close()

def read_all_from_disk(file):
	f = codecs.open(file, "r", "utf-8")
	data = f.read()
	f.close()
	lines = data.split("\n")
	locations = []
	for line in lines:
		optional_location = parse_one_location_from_text(line)
		if(optional_location):
			locations.append(optional_location)
	return locations

def parse_one_location_from_text(text):
	columns = text.split("\t")
	if(len(columns) >= 8):
		country = columns[0]
		city = columns[1]
		name = columns[2]
		eventType = event_type_by_name(columns[17])
		location = Location(name, country, city, eventType)
		description = columns[3]
		duration = columns[4]
		longitude = columns[5]
		latitude = columns[6]
		fun = columns[7]
		ratings = [columns[8], columns[9], columns[10], columns[11], columns[12]]
		netRating = columns[13]
		hours = [ item.encode('ascii') for item in ast.literal_eval(columns[14]) ]
		types = [ item.encode('ascii') for item in ast.literal_eval(columns[15]) ]
		certificate = columns[16]
		if(description != "None"):
			location.setDescription(description)
		if(longitude != "None"):
			location.setLongitude(float(longitude))
		if(latitude != "None"):
			location.setLatitude(float(latitude))
		if(duration != "None"):
			location.setDuration(duration)
		if(ratings != "None"):
			location.setRatings(ratings)
		if(netRating != "None"):
			location.setNetRating(netRating)
		if(len(hours) > 0):
			location.setHours(hours)
		if(len(types) > 0):
			location.setTypes(types)
		if(certificate != "None"):
			location.setCertificate(certificate)
		return location
	else:
		return False


