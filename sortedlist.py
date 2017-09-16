class sortedlist:
	
	#don't deal with this directly or you'll fuck everything up
	data = []
	
	def __init__(self, dat=[], presorted=False):
		if presorted:
			self.data = dat
		else:
			self.data = sorted(dat)
	
	def __getitem__(self, key):
		return self.data[key]
	
	def __len__(self):
		return len(self.data)
	
	def __str__(self):
		return str(self.data)
	
	def __delitem__(self, key):
		del(self.data[key])
	
	def __add__(self, operand):
		if isinstance(operand, list):
			return sortedlist(self.merge(self.data, sorted(operand)), True)
		elif isinstance(operand, sortedlist):
			return sortedlist(self.merge(self.data, operand.data), True)
		else:
			raise TypeError('can only concatenate list or sortedlist (not "%s") to sortedlist' % type(operand).__name__)
	
	#because of sorting, addition is commutative (a + b == b + a)
	def __radd__(self, operand):
		return self + operand
	
	def __iadd__(self, operand):
		self.data = (self + operand).data
	
	#takes two sorted lists (not sortedlists) and returns a sorted combination at O(n)
	def merge(self, data1, data2):
		ind1 = 0
		ind2 = 0
		merged = []
		
		while True:
			if data1[ind1] <= data2[ind2]:
				merged += [data1[ind1]]
				ind1 += 1
			else:
				merged += [data2[ind2]]
				ind2 += 1
			if ind1 >= len(data1):
				return merged + data2[ind2:]
				break
			elif ind2 >= len(data2):
				return merged + data1[ind1:]
	
		
	def add(self, entry):
		self.data = self.addhelper(self.data, entry)
		
	#I couldn't figure out how to do this recursively in the add method
	#and fuck trying to do this in a loop
	def addhelper(self, dat, entry):
		if dat == []:
			return [entry]
		ind = int(len(dat)/2)
		if entry < dat[ind]:
			return self.addhelper(dat[0:ind], entry) + dat[ind:]
		else:
			return dat[:ind+1] + self.addhelper(dat[ind+1:], entry)
	
	def isin(self, entry):
		return self.inhelper(self.data, entry)
		
	#ditto
	def inhelper(self, dat, entry):
		if len(dat) == 0:
			return False
		elif len(dat) == 1:
			return entry == dat[0]
		
		ind = int(len(dat)/2)
		if entry < dat[ind]:
			return self.inhelper(dat[:ind], entry)
		elif entry > dat[ind]:
			return self.inhelper(dat[ind+1:], entry)
		else:
			return True
	
	#returns an arbitrary index that contains the value at O(log(n))
	#returns -1 if the list doesn't contain the value
	def index(self, val):
		ind = self.indexhelper(self.data, val)
		if ind == len(self):
			ind = -1
		return ind
		pass
	
	#at this point I think I'm just bad at defining recursive functions
	def indexhelper(self, dat, val):
		ind = int(len(dat)/2)
		
		if len(dat) == 0:
			return 0
		elif dat[ind] == val:
			return ind
		elif dat[ind] < val:
			return ind + 1 + self.indexhelper(dat[ind+1:], val)
		else:
			return self.indexhelper(dat[:ind], val)
	
	#TODO: add functionality for single=False
	def remove(self, entry, single=True):
		del(self[self.index(entry)])