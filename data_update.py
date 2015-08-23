from location import read_all_from_disk, write_all_locations_to_disk
from location_type import museum, bar, park, landmark

read_from_file = "china_beijing.txt"
write_to_file = "updated-data.txt"
ordered_types = [museum, bar, park, landmark]

def update_data(read_from, write_to):
	all_locations = read_all_from_disk(read_from)
	updated_locations = []
	for location in all_locations:
		updated_locations.append(update_one_location(location))
	write_all_locations_to_disk(updated_locations, write_to)

def update_one_location(location):
	updated = location
	updated = update_one_location_duration(updated)
	updated = update_one_location_hours(updated)
	return updated

def update_one_location_duration(location):
	updated = location
	for t in ordered_types:
		updated = update_location_duration_by_type(updated, t)
	return updated

def update_one_location_hours(location):
	updated = location
	for t in ordered_types:
		updated = update_location_hours_by_type(updated, t)
	return updated

def update_location_duration_by_type(location, location_type):
	updated = location
	if(location.duration == ''):
		if(location_type.name in updated.types):
			updated.setDuration(location_type.duration)
	return updated

def update_location_hours_by_type(location, location_type):
	updated = location
	if(len(location.hours) == 0):
		if(location_type.name in updated.types):
			updated.setHours(location_type.hours)
	return updated

def test():
	# from data_update import test
	update_data(read_from_file, write_to_file)

def location_data(locations):
	print("TOTAL LOCATIONS: "+str(len(locations)))
	print("WITH DURATIONS: "+str(len(locations_with_durations(locations))))
	print("WITH HOURS: "+str(len(locations_with_hours(locations))))

def locations_with_durations(locations):
	return filter(lambda l: l.duration != '', locations)

def locations_with_hours(locations):
	return filter(lambda l: len(l.hours) > 0, locations)

def stats_on_durations(locations):
	type_and_count = []
	print(str(len(locations_with_durations(locations))) +" of "+ str(len(locations))+ " have durations")
	for location in locations:
		types = location.types
		has_duration = location.duration != ''
		for t in types:
			if(has_duration):
				type_and_count.append([t, 1])
			else:
				type_and_count.append([t, 0])
	all_types = list(set(map(lambda t: t[0], type_and_count)))
	for t in all_types:
		elements_of_type = filter(lambda k: k[0] == t, type_and_count)
		total_elements = len(elements_of_type)
		total_with_duration = len(filter(lambda k: k[1] == 1, elements_of_type))
		print("TYPE \""+t+"\": "+str(total_with_duration)+" of "+str(total_elements))




