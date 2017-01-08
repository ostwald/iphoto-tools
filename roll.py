import sys, os, time
from UserDict import UserDict
from iPhoto import IPhotoDict, getappletime
import globals
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from iPhotoItem import IPhotoItemRecord

class Roll_API (IPhotoDict):
	"""
	use getItemByFileName to find the IPhotoItem in this Roll with the specified
	filename. ASSUMES there is only one item per roll with a given filename

	attributes include:
		- name
		- id
		- itemIds
		- comment
		- collection
		- date
	"""
	def __init__ (self, data, library):
		self.library = library
		IPhotoDict.__init__ (self, data)
		self.name = ""
		self.id = ""
		self.itemIds = []
		self.comment = ""
		self.items = []
		self.date = ""
		
		self.fileNameMap = UserDict()
		self.captionMap = UserDict()

		self.start = ""
		self.end = ""
		self.size = 0

	def post_init(self):
		"""
		called after self.items is initialized
		:return:
		"""
		self.fileNameMap = UserDict()
		self.captionMap = UserDict()

		self.size = len(self.items)
		for item in self.items:
			self.fileNameMap[item.filename] = item
			self.captionMap[item.caption] = item

	def getEndDate (self):
		"""
		return the date of the last item
		"""
		id = self.itemIds[-1] # can we depend on being sorted?
		item = self.getItem(id)
		return self.getItem(id).date
			
	def getItemByFileName (self, filename):
		if self.fileNameMap.has_key(filename):
			return self.fileNameMap[filename]
		else:
			return None
	
	def getItemByCaption (self, caption):
		if self.captionMap.has_key(caption):
			return self.captionMap[caption]
		else:
			return None
			
	def getItem(self, itemId):
		return self.library.getItem(itemId)
		
	def report (self):
		verbose = 1
		print '\nRoll: %s (%s items) - %s to %s' % (self.name, len(self.itemIds), 
													self.date, self.getEndDate())
		if self.comment:
			print '\t%s ' % self.comment
		if verbose:
			for itemId in self.itemIds:
				item = self.getItem(itemId)
				item.report()

	def asTabDelimited (self):
		record = '\t'.join(map (lambda x:str(getattr(self, x)),
						 globals.ROLL_ATTRS))
		record = record.replace (chr(13), ' ').replace('\n', ' ')
		return record

	def itemsAsTabDelimited (self):
		"""
		represent the items of this role as tab-delimited
		:return:
		"""
		lines=[];add=lines.append
		attrs = globals.IPHOTO_ITEM_ATTRS
		# columns = ['id', 'date', 'caption', 'path']
		add ('\t'.join(attrs))
		for item_id in self.itemIds:
			item = self.library.getItem(item_id)
			add (item.asTabDelimited())
			# row = []
			# for attr in attrs:
			# 	row.append (str(getattr(item, attr))) or ""
			# add ('\t'.join(row))

		return '\n'.join(lines)

class Roll (Roll_API):
	"""
	use getItemByFileName to find the IPhotoItem in this Roll with the specified
	filename. ASSUMES there is only one item per roll with a give filename

	attributes include:
		- name
		- id
		- itemIds
		- comment
		- collection
		- date
	"""
	def __init__ (self, data, library):
		self.library = library
		IPhotoDict.__init__ (self, data)
		self.name = self['RollName']
		self.id = self['RollID']
		self.itemIds = self['KeyList']
		self.comment = self['Comments']
		# rollDateAsTimerInterval = self['RollDateAsTimerInterval'] or ""
		# self.date = getappletime(rollDateAsTimerInterval)

		self.date = getappletime(self['RollDateAsTimerInterval'])
		dateFormat = "%m/%d/%Y"
		self.start = time.strftime (dateFormat, self.date.timetuple())
		self.end = time.strftime (dateFormat, self.getEndDate().timetuple())

		self.items = map (lambda x:self.getItem(x), self.itemIds)
		self.size = len(self.items)
		self.post_init()


class RollItemsReader (TabDelimitedFile, Roll_API):
	"""
	reads photoItem data from tabdelimited file and returns
	list of IPhotoItemRecord instances
	"""
	def __init__ (self, data_file):

		TabDelimitedFile.__init__(self, entry_class=IPhotoItemRecord)
		# print 'about to read from "%s"' % data_file
		self.read (data_file)
		self.itemIds = map (lambda x:x.id, self.data)

		# print '- %s has %d itemIds' % (os.path.basename(data_file), len(self.data))

class RollRecord (TabDelimitedRecord, Roll_API):
	"""
	use getItemByFileName to find the IPhotoItem in this Roll with the specified
	filename. ASSUMES there is only one item per roll with a give filename

	attributes include:
		- name
		- id
		- itemIds
		- comment
		- collection
		- date
	"""
	def __init__ (self, data, library):
		"""
		library is parent (will be assigned by TabDelimitedRecord
		:param data:
		:param library:
		:return:
		"""

		# print "ROLL_RECORD"
		TabDelimitedRecord.__init__(self, data, library)
		self.library = self.parent
		for attr in globals.ROLL_ATTRS:
			setattr(self, attr, self[attr])
		self.size = int(self.size)
		self.date = globals.getTime(self.start)
		self.itemIds = []
		self.items = []
		self.fileNameMap = UserDict()
		self.captionMap = UserDict()


	def __repr__(self):
		return '%s (%s) from %s to %s - %s items' % (self.name, self.id, self.start, self.end, self.size)



if __name__ == '__main__':
	path = globals.REPO_BASE + '/jloAlbumData/rolls/42606.txt'
	reader = RollItemsReader(path)
	print '%d read' % len(reader.itemIds)
	for id in reader.itemIds:
		print id