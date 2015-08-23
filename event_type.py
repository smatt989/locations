class EventType:
	def __init__(self, name, tripadvisor_regex):
		self.name = name
		self.tripadvisor_regex = tripadvisor_regex

activity = EventType("activity", 'http[s]?://www\\.tripadvisor\\.com/Attraction_Review.+')
restaurant = EventType("restaurant", 'http[s]?://www\\.tripadvisor\\.com/Restaurant_Review.+')
hotel = EventType("hotel", 'http[s]?://www\\.tripadvisor\\.com/Hotel_Review.+')

def event_type_by_name(name):
	if(name == activity.name):
		return activity
	elif(name == restaurant.name):
		return restaurant
	elif(name == hotel.name):
		return hotel