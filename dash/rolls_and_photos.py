"""
Tools to get a handle on what is in a iPhoto Library

- list rolls
- list items (roll)
	- roll = IPhotoLibrary.getRollById(id)
- find rolls in a given date range
	- IPhotoLibrary.getRolls(start,[end])



"""
__author__ = 'ostwald'
from tabdelimited import TabDelimitedFile, TabDelimitedRecord

import os, sys, time
from iPhoto import IPhotoLibrary
from iPhoto import libcmp
from iPhoto import globals

def getPhotosByDateRangeTester(lib, start, end=None):
	"""
	we are returning Roll instances
	:param lib:
	:param start:
	:param end:
	:return:
	"""

	print '\nGET PHOTOS - from %s to %s' % (start, end)
	start_time = globals.getTime(start)
	end_time = globals.getTime(end)

	# print "SELECTED"
	ids = []
	args = {'start':start, 'end':end}
	# selected = lib.getRolls(**args)
	# print '%d rolls selected' % len(selected)
	# for roll in selected:
	# 	# tag = roll.date < startDate and "before" or "after"
	# 	print '%s - %s - %s' % (roll.start, roll.id, roll.name)
	# 	ids += roll.itemIds
	# return ids
	return lib.getItems(**args)

def getPhotosByDateRangeTesterOFF(lib, start, end=None):

	"""
	we are returning iPhotoItem instances
	:param lib:
	:param start:
	:param end:
	:return:
	"""

	print '\nGET ROLLS - from %s to %s' % (start, end)
	ids = []

	# print "SELECTED"
	args = {'start':start, 'end':end}
	selected = lib.getRolls(**args)
	print '%d rolls selected' % len(selected)

	for roll in selected:
		# tag = roll.date < startDate and "before" or "after"
		print '%s (%s) - %s (%s items)' % (roll.start, roll.id, roll.name, roll.size)

		ids += roll.itemIds

	return ids

if __name__ == "__main__":

	data = 'jloAlbumData'
	# data = 'purgAlbumData'
	# data = 'mediaAlbumData'
	data_dir = '/Users/ostwald/tmp/iPhotoLibrary_XLS_Database'
	data_file = os.path.join (data_dir, data, data + '.txt')

	lib = IPhotoLibrary(data_file)
	start = "2006-01-01"
	end = "2006-01-27"
	# ids = getRollsByDateRangeTester(lib, start, end)
	print 'calling getPhotosByDateRangeTester'
	items = getPhotosByDateRangeTester(lib, start, end)
	print '%s items found' % len (items)

	# sort items in reverse chron
	items.sort (key=lambda x:globals.getTime(x.date), reverse=1)

	for item in items:
		print '%s (%s)' % (item.caption, item.date)