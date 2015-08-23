class LocationType:
	def __init__(self, name, duration, hours):
		self.name = name
		self.duration = duration
		self.hours = hours

museum = LocationType("Museums", "120", [])
bar = LocationType("Bars & Clubs", "90", ['0:00 - 1:00', '137:00 - 145:00', '161:00 - 168:00'])
park = LocationType("Nature & Parks", "90", [])
landmark = LocationType("Sights & Landmarks", "90", [])