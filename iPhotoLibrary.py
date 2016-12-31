import os, sys, time
from plist import PlistParser
from iPhoto import IPhotoDict
from iPhotoItem import IPhotoItem
from album import Album
from roll import RollRecord
from iPhoto import globals, AbstractIPhotoLibrary
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from roll import RollItemsReader
import globals


class IPhotoLibrary (AbstractIPhotoLibrary, TabDelimitedFile):
	"""
	read data from spreadsheets (created by DumperIPhotoLibrary)

	self.data is tabdelimited data representing roles
	self.rolls are RollRecord instances that provide Roll_API
	self.items are IPhotoItemRecord instances

	"""
	linesep = '\n'

	def __init__ (self, data_file, entry_class=RollRecord):
		tics = time.time()
		TabDelimitedFile.__init__(self, entry_class=entry_class)
		self.data_file = data_file

		self.name = os.path.splitext(os.path.basename(data_file))[0]
		# self.plist = PlistParser(path).plist

		self.albums = None
		self.rollMap = IPhotoDict()
		self.rolls = self.read_rolls()
		self.items = self.read_items()


		print '\n%s - IPhotoLibrary instantiated in %.2f secs' % (self.name, time.time() - tics)

	def read_rolls (self):
		"""
		returns list of RollRecord instances

		intializes rollMap as side effect
		:return:
		"""
		rolls = []
		print 'reading from ', self.data_file
		self.read(self.data_file)

		print '%d rolls read' % len(self.data)
		for roll in self.data:
			# print roll
			self.rollMap[roll.id] = roll
			rolls.append(roll)
		return rolls

	def read_items (self):
		"""
		read the individual roll spreadsheets and instantiate items
		:return:
		"""
		items = []
		lib_data_dir = os.path.dirname(self.data_file)
		for roll in self.rolls:
			data_file = os.path.join (lib_data_dir,'rolls',roll.id+'.txt')
			roll_items_reader = RollItemsReader(data_file)

			## roll_items_reader
			roll_data = roll_items_reader.data
			# print '%d items read from %s' % (len(roll_data), data_file)

			if not len(roll_data) == roll.size:
				print 'Warning: %s != %s' % (len(roll_data), roll.size)

			# update roll instance
			# roll.items = {}
			# for item in roll_data:
			# 	roll.items[item.id] = items
			roll.items = roll_data;
			roll.itemIds = map (lambda x:x.id, roll_data)
			roll.post_init()

			# accumulate items list to return
			items += roll_data

		print '%d items read from %d rolls' % (len(items), len(self.rolls))

		items_map = {}
		for item in items:
			items_map[str(item.id)] = item
		return items_map

if __name__ == '__main__':

	data = 'jloAlbumData'
	# data = 'purgAlbumData'
	# data = 'mediaAlbumData'
	data_dir = '/Users/ostwald/tmp/iPhotoLibrary_XLS_Database'
	data_file = os.path.join (data_dir, data, data + '.txt')

	lib = IPhotoLibrary (data_file)
	lib.reportRolls(lib.rolls[:10])



