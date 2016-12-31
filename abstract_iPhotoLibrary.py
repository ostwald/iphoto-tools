import os, sys, time
from plist import PlistParser
from iPhoto import IPhotoDict
from iPhotoItem import IPhotoItem
from album import Album
from roll import Roll
from iPhoto import globals


class AbstractIPhotoLibrary:

	def __init__ (self):
		self.name = None
		self.plist = None
		self.items = []
		self.albums = []
		self.rolls = []
		self.rollMap = IPhotoDict()

	def __len__ (self):
		return len(self.items)

	def findRoll (self, frag):
		for roll in self.rolls:
			if roll.name.lower().startswith(frag.lower()):
				return roll

	def getRoll (self, rollName):
		raise Exception, 'where did i come from?'
		for roll in self.rolls:
			if roll.name == rollName:
				return roll
		raise KeyError, 'Roll not found for "%s"' % roleName


	def getRollById (self, rollId):
		"""
		the rollMap keys are integers
		"""
		id = int(rollId)
		return self.rollMap[id]

	def getItem (self, key):
		# return IPhotoItem (key, self.items[key].data, self)
		if self.items.has_key(key):
			return self.items[key]

	def getItems(self, **args):
		print 'ARGS - %s' % args
		startDate = args.has_key('start') and args['start']
		if type(startDate) == type(""):
			startDate = globals.getTime(startDate)

		endDate = args.has_key('end') and args['end']
		if type(endDate) == type(""):
			endDate = globals.getTime(endDate)

		def accept (item):
			item_date = globals.getTime(item.date)
			if startDate and item_date <= startDate:
				return 0
			if endDate and item_date > endDate:
				return 0
			return 1

		selected = self.getRolls(**args)
		print '%d rolls selected' % len(selected)
		ids=[]
		items=[]
		for roll in selected:
			# tag = roll.date < startDate and "before" or "after"
			print '%s - %s - %s' % (roll.start, roll.id, roll.name)

			roll_items = filter(accept, roll.items)
			ids += map(str, roll.itemIds)
			items += roll_items

		print '%d items, %d item_ids' % (len(items), len(ids))
		return items

	def reportTopLevelKeys (self):
		print "Top Level keys"
		for key in self.plist.keys():
			obj = self.plist[key]
			print "\t%s (%s)" % (key, obj.__class__.__name__)

	def reportAlbums (self):
		print ("\nALBUMS")

		for album in self.albums:
			print '%s (%s)' % (album.name, album.id)

	def getRolls (self, **args):
		"""
		accepts either DateTime objects or strings in form "YYYY-MM-DD"
		return role that have a start date within specified range

		:param startDate:
		:param endDate:
		:return:
		"""
		print 'ARGS - %s' % args
		startDate = args.has_key('start') and args['start']
		if type(startDate) == type(""):
			startDate = globals.getTime(startDate)

		endDate = args.has_key('end') and args['end']
		if type(endDate) == type(""):
			endDate = globals.getTime(endDate)

		def accept (roll):
			if startDate and roll.date <= startDate:
				return 0
			if endDate and roll.date > endDate:
				return 0
			return 1
		if 0: # debugging
			for roll in self.rolls:
				# tag = roll.date < startDate and "before" or "after"
				tag = accept (roll) and "in" or "out"
				print '%s - %s' % (roll.date, tag)


		return filter (accept, self.rolls)

	def getRollsOFF (self, startDate, endDate=None):
		"""
		accepts either DateTime objects or strings in form "YYYY-MM-DD"
		return role that have a start date within specified range

		:param startDate:
		:param endDate:
		:return:
		"""
		if type(startDate) == type(""):
			startDate = globals.getTime(startDate)

		if type(endDate) == type(""):
			endDate = globals.getTime(endDate)

		def accept (roll):
			if roll.date <= startDate:
				return 0
			if endDate and roll.date > endDate:
				return 0
			return 1
		if 0: # debugging
			for roll in self.rolls:
				# tag = roll.date < startDate and "before" or "after"
				tag = accept (roll) and "in" or "out"
				print '%s - %s' % (roll.date, tag)

		return filter (accept, self.rolls)

	def reportRolls (self, rolls=None):
		print ("\nROLLS")
		rolls = rolls or self.rolls
		for roll in rolls:
			print '- "%s" | %s to %s | id:%s | %s items' % (roll.name,
			                                                roll.start, roll.end,
			                                                roll.id, roll.size)

			

