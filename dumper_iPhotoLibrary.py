import os, sys, time
from plist import PlistParser
from iPhoto import IPhotoDict
from iPhotoItem import IPhotoItem
from album import Album
from roll import Roll
from iPhoto import globals, IPhotoLibrary_API

import codecs

class Dumper:

	repo_base = globals.REPO_BASE
	encoding = 'utf-8'
	dump_dir = None

	def dump(self):
		print "DUMPING - ", self.name
		tics = time.time()
		if not os.path.exists(self.repo_base):
			os.mkdir(self.repo_base)

		self.dump_dir = os.path.join (self.repo_base, self.name)
		if not os.path.exists(self.dump_dir):
			os.mkdir(self.dump_dir)

		print 'DUMP DIR: %s' % self.dump_dir

		self.dumpRollData()
		self.dumpItemDataByRoll()
		tics = time.time() - tics
		print 'elapsed time: %.2f' % tics


	def dumpRollData (self, path=None):

		if path is None:
			path = os.path.join (self.dump_dir, self.name+'.txt')
		lines=[];add=lines.append
		# columns = ['name', 'id', 'start', 'end', 'size']
		columns = globals.ROLL_ATTRS
		add ('\t'.join(columns))
		for roll in self.rolls:
			add (roll.asTabDelimited())
			# add ('\t'.join(map (str, map (lambda x:getattr(roll, x), columns))))
		fp = open(path, 'w')
		fp.write ('\n'.join (lines))
		fp.close()
		print "wrote to ", path

	def dumpItemDataByRoll (self):
		roll_dir = os.path.join (self.dump_dir, 'rolls')

		if not os.path.exists(roll_dir):
			os.mkdir(roll_dir)
		warnings = []
		for roll in self.rolls:
			# print 'ROLL_ID:', roll.id
			path = os.path.join (roll_dir, str(roll.id) + '.txt')
			try:
				# fp = open(path, 'w')
				fp = codecs.open (path, 'w', self.encoding)
				fp.write (unicode(roll.itemsAsTabDelimited()))
				fp.close()
				print "wrote roll %s - %s" % (roll.id, roll.name)
			except:
				warnings.append("could not write to %s\n - %s" % (path, sys.exc_info()[1]))
		print "dump complete - %d warnings" % len(warnings)
		if warnings:
			for w in warnings:
				print '- %s' % w


class DumperIPhotoLibrary (IPhotoLibrary_API, Dumper):
	"""
	populates  (items, albums, rolls, rollMap)
	from iPhoto source XML file (plist)
	dumps iPhotoLibrary to tab delimited thanks to Dumper
	"""
	def __init__ (self, path):
		tics = time.time()
		self.name = os.path.splitext (os.path.basename (path))[0]
		self.plist = PlistParser(path).plist
		self.items_data = IPhotoDict(self.plist['Master Image List'])
		# self.show_items_data()
		self.items = {}
		for item_id in self.items_data.keys():
			self.items[item_id] = IPhotoItem (item_id, self.items_data[item_id], self)
		self.albums = map (lambda x: Album(x, self), self.plist['List of Albums'])
		self.rolls = map (lambda x: Roll(x,self), self.plist['List of Rolls'])

		self.rollMap = IPhotoDict()
		for roll in self.rolls:
			self.rollMap[roll.id] = roll
		print '\nIPhotoLibrary instantiated - %.2f sec' % (time.time() - tics)

	def show_items_data(self):
		for key in self.items_data.keys():
			print '- %s: %s' % (key, self.items_data[key])

if __name__ == '__main__':

	# data_file = globals.videoStorage_plist
	data_file = globals.purgAlbum_plist

	lib = DumperIPhotoLibrary (data_file)
	# lib.reportRolls()
	lib.dump()

