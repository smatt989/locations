import re

time_extract_regex = '(\d+(:\d+)?)'

days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

last_time_of_week = str(len(days) * 24)+":00"
first_time_of_week = "0:00"

def get_date_ranges(day_string, time_string):
	dates = dates_in_date_range(date_range(day_string))
	times = time_range(time_string)
	start_time = parse_one_time(times[0])
	end_time = parse_one_time(times[1])
	open_ranges = []
	for date in dates:
		day_index = index_of(date)
		start = add_hours(start_time, 24 * day_index)
		end = ""
		if(hours_of(end_time) < hours_of(start_time)):
			end = add_hours(end_time, 24 * (day_index + 1))
			if(hours_of(end) >= len(days) * 24):
				open_ranges.append(start+" - "+last_time_of_week)
				start = first_time_of_week
				end = add_hours(end, - (len(days) * 24))
		else:
			end = add_hours(end_time, 24 * day_index)
		open_ranges.append(start+" - "+end)
	return open_ranges

def add_hours(time, to_add):
	return str(hours_of(time) + to_add) + ":" + str(format_minutes(minutes_of(time)))

def hours_of(time):
	return int(time.split(":")[0])

def minutes_of(time):
	return int(time.split(":")[1])

def format_minutes(minutes):
	if(minutes < 10):
		return "0"+str(minutes)
	else:
		return str(minutes)

def date_range(day_string):
	return day_string.lower().split(" - ")

def time_range(time_string):
	return time_string.lower().split(" - ")

def parse_one_time(time):
	hours = ""
	minutes = ""
	if(len(time.split("a")) > 1):
		extracted = re.match(time_extract_regex, time).group(1).split(":")
		pre_hours = extracted[0]
		if(int(pre_hours) == 12):
			hours = '0'
		else:
			hours = pre_hours
		if(len(extracted) > 1):
			minutes = extracted[1]
		else:
			minutes = "00"
	else:
		extracted = re.match(time_extract_regex, time).group(1).split(":")
		hours = str(int(extracted[0]) + 12)
		if(len(extracted) > 1):
			minutes = extracted[1]
		else:
			minutes = "00"
	return hours + ":" + minutes
		

def index_of(day):
	return days.index(day)

#for a range, not a single date
def dates_in_date_range(date_range):
	dates = []
	if(len(date_range) == 1):
		date = index_of(date_range[0])
		dates.append(days[date])
	else:
		start = index_of(date_range[0])
		end = index_of(date_range[1])
		if start > end:
			i = 0
			while i <= end:
				dates.append(days[i])
				i = i + 1
			j = start
			while j <= len(days) - 1:
				dates.append(days[j])
				j = j + 1
		else:
			i = start
			while i <= end:
				dates.append(days[i])
				i = i + 1
	return dates
