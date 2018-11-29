class Station():
	def __init__(self, name):
		self.name = name
		self.lat = 0
		self.lon = 0
		self.elev = 0
		self.data = []
		self.id = 0
		self.pcp = {}
		self.temp = {}
		self.wind = {}
		self.hmd = {}
		self.clouds = {}
		self.irrad = {}

	def __str__(self):
		return(self.name + str(self.pcp) + "\n")
