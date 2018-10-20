class Record():
	def __init__(self, date, RRR, tR):
		self.date = date
		if RRR == "":
			self.RRR = "no data"
		else:
			self.RRR = RRR
		if tR == "":
			self.tR = "no data"
		else:
			self.tR = tR

	def __str__(self):
		return str(self.date) + " {:>15s}".format(str(self.RRR)) + " {:>15s}".format(str(self.tR))