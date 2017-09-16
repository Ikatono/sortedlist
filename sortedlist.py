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
    
    def __repr__(self):
        ret = 'sortedlist('
        for i in self.data:
            ret += str(i) + ', '
        return ret[:-2] + ')'
    
    def __str__(self):
        return str(self.data)
    
    def __delitem__(self, key):
        del(self.data[key])
    
    def __add__(self, operand):
        if isinstance(operand, list):
            return sortedlist(self.merge(self.data, sorted(operand)), presorted=True)
        elif isinstance(operand, sortedlist):
            return sortedlist(self.merge(self.data, operand.data), presorted=True)
        else:
            return NotImplemented
    
    #because of sorting, addition is commutative (a + b == b + a)
    def __radd__(self, operand):
        return self + operand
    
    def __iadd__(self, operand):
        self.data = (self + operand).data
        return self
    
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
    
    #returns an arbitrary index that contains the value, at O(log(n))
    def index(self, value):
        low = 0
        high = len(self)
        mid = (low + high) / 2
        while self[mid] != value:
            if self[mid] > value:
                high = mid
            else:
                low = mid
            mid = (high + low) / 2
            if high in (low, low+1):
                raise ValueError('sortedlist does not contain entry')
        return mid
    
    #removes a single instance of entry, raises exception if it doesn't exist
    def remove(self, entry):
        del(self[self.index(entry)])
    
    #removes every instance of entry, doesn't raise an exception if it doesn't exist
    #TODO: index once, then search adacent indices
    def removeall(self, entry):
        while True:
            try:
                del(self[self.index(entry)])
            except ValueError:
                break

