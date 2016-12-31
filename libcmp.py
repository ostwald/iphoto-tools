"""
Library Compare

- given two iPhoto Libraries (represented by spreadsheets such as those created by 
iPhotoLibrary.rollsToSpreadSheet)

- report missing, extra and different Rolls, where
-- missing - rolls that are in the other library but not this one
-- extra - rolls that are in this library but not in the other
-- different - rolls that have same date range but different title or number of photos
"""
import os, sys, re, time
from iPhoto import globals
from UserDict import UserDict
from tabdelimited import TabDelimitedFile, TabDelimitedRecord

class RollMap (UserDict):
	"""
	stores RollData Instance (read from spreadsheet) mapped to
	a key (e.g. '%s-%s-%d' % (self.name, self.start, self.size)
	"""
	strict = False
	
	def __init__ (self):
		self.data = {}
	
	def __setitem__ (self, key, value):
		if self.data.has_key(key):
			if self.strict:
				raise Exception, 'dup key: %s' % key
		else:
			self.data[key] = value
			
	def __getitem__ (self, key):
		if not self.data.has_key(key):
			return None
		return self.data[key]

class RollData (TabDelimitedRecord):
	
	date_format = '%m/%d/%Y'
	
	"""
	Represents one line (a Roll) from spreadsheet

	extend WorksheetEntry to specify field delmiter,
	to give class-specific attributes, etc

	sortable (via startData)
	"""
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.startDate = None
		self.endDate = None
		for attr in ['start', 'end']:
			# print 'self[%s] = %s' % (attr, self[attr])
			try:
				setattr(self, attr+'Date', time.strptime(self[attr], self.date_format))
				# self.startDate = time.strptime(self['start'], self.date_format)
				# self.endDate = time.strptime(self['end'], self.date_format)
			except ValueError, msg:
				print 'RoleData ValueError: %s (%s)' % (msg, self[attr])
		self.name = self['name']
		self.start = self['start']
		self.end = self['end']
		self.size = int(self['size'])
		self.id = self['id']

	def getKey (self):
		# return '%s-%s-%d' % (self.start, self.end, self.size)
		return '%s-%s-%d' % (self.name, self.start, self.size)
		
	def __cmp__ (self, other):
		return cmp(self.startDate, other.startDate)
				
class LibraryRollData (TabDelimitedFile):
	"""
	Represents a Library Rolls from spreadsheet

	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	
	note on encoding: we prefer utf-8, but ISO-8859-1 seems to work 
	most often ...
	"""
	
	verbose = 1
	linesep = "\n"  # for macs to override os.linesep
	max_to_read = None
	encoding = 'ISO-8859-1' # utf-8
	
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=RollData)
		self.rollMap = RollMap()
		self.path = path
		self.read (path)
		self.data.sort()
			
	def add (self, item):
		"""
		overide this to create other structurs, such as maps, e.g.,
		self.itemMap[item.key] = item
		"""
		if item.startDate:
			self.append(item)
			self.rollMap[item.getKey()] = item
		
	def report (self):
		print '\n------------------------\n%s' % os.path.basename(self.path)
		for roll in self:
			print '%s - %s (%s)' % (roll.start, roll.name, roll.size)
			
	def getItem (self, key):
		return self.rollMap[key]
		
class CompositeRollData (LibraryRollData):
	"""
	Reads two libraryRoll data files and creates composite list of
	RollData instances, ordered by sortDate
	"""
	
	def __init__ (self, lib1path, lib2path):
		TabDelimitedFile.__init__ (self, entry_class=RollData)
		self.rollMap = RollMap()
		self.read (lib1path)
		lib1data = self.data
		print "after first read: %d" % len(self)
		self.read (lib2path)
		print "after second read: %d" % len(self)
		self.data = self.data + lib1data
		self.data.sort()
		
			
	def report (self):
		print '\n------------------------\n%s' % os.path.basename(self.path)
		for roll in self:
			print '%s - %s (%s)' % (roll.start, roll.name, roll.size)
		
class RollDataCompare:
	"""
	Prints diff list between two repositories (i.e., reference and other)
	"""
	def __init__ (self, refPath, otherPath):
		self.ref = LibraryRollData (refPath)
		self.other = LibraryRollData (otherPath)
		self.refName = os.path.basename(refPath)
		self.otherName = os.path.basename(otherPath)
		self.missing = self.getMissing()
		self.extras = self.getExtras()
		print " - %s (%d)" % (self.refName, len(self.ref.data))
		print " - %s (%d)" % (self.otherName, len(self.other))


	def getMissing (self):
		"""
		missing are items that are in other lib that aren't in ref lib
		"""
		missing=[];add=missing.append
		for item in self.other:
			key = item.getKey()
			if not self.ref.getItem(key):
				add (item)
		return missing
		
	def getExtras (self):
		"""
		extras are rolls that are in ref but not in other
		"""
		extras=[];add=extras.append
		for item in self.ref:
			key = item.getKey()
			if not self.other.getItem(key):
				add (item)
		return extras
		
	def report (self):
		verbose = 1
		print '\n--------------------------------'
		print "Missing (%d) - rolls in %s that aren't in %s" % (len(self.missing), self.otherName, self.refName)
		if verbose:
			for roll in self.missing:
				print '- %s - %s (%s)' % (roll.start, roll.name, roll.size)
		
		print '\n--------------------------------'
		print "Extras (%d) - rolls in %s that aren't in %s" % (len(self.extras),  self.refName, self.otherName)
		if verbose:
			for roll in self.extras:
				print '- %s - %s (%s)' % (roll.start, roll.name, roll.size)
		
class RollDataCompareUsingComposite ():
	
	def __init__ (self, lib1, lib2):
		self.lib1 = LibraryRollData (lib1)
		self.lib2 = LibraryRollData (lib2)
		self.comp = CompositeRollData (lib1, lib2)
		
	def compare (self):
		for item in self.comp:
			key = item.getKey()
			display1 = self.lib1.rollMap.has_key(key) and '+' or '-'
			display2 = self.lib2.rollMap.has_key(key) and '+' or '-'
			if not display1 == display2:
				print "%s | %s | %s %s (%s)" % (display1, display2, item.start, item.name, key)
			
if __name__ == '__main__':
	# rolldata = 'data/xls'
	# jloData = os.path.join (rolldata, 'JLO_iLibraryRolls.txt')
	# mtShermanData = os.path.join (rolldata, 'MtShermanRollData.txt')
	# timeMachineData = os.path.join (rolldata, 'timemachine-iPhotoRolls.txt')
	if 0:
		rolls = CompositeRollData (jloData, mtShermanData)
	if 0:
		rolls = LibraryRollData (mtShermanData)
		rolls.report()
	if 0:
		comp = RollDataCompare (timeMachineData, mtShermanData)
		comp.report()
	if 1:
		comp = RollDataCompareUsingComposite (timeMachineData, mtShermanData)
		rolls.compare()
	# print '%d rolls read' % len(rolls)
	# rolls.report()
