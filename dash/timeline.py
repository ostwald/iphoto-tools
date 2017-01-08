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

import os, sys, datetime, codecs
from iPhoto import IPhotoLibrary
from iPhoto import libcmp
from iPhoto import globals
import json

def timeLine(lib, start, end=None):
	"""
	we are returning Roll instances
	:param lib:
	:param start:
	:param end:
	:return:
	"""

	print 'TIMELINE - from %s to %s' % (start, end)
	items = lib.getItems(start=start, end=end)
	item_attrs =  ['id', 'caption', 'date', 'filename']
	date_map = {}
	for item in items:
		# print '- %s (%s)' % (item.caption, item.date)

		keyDate = globals.getShortDateStr(item.date)

		vals = date_map.has_key(keyDate) and date_map[keyDate] or []
		# vals.append(item.id)

		vals.append(item.asJson(item_attrs))
		date_map[keyDate] = vals

	return date_map

def writeTimeLine(lib, start, end=None):
	dowrites = 1
	name = lib.name
	print "\nLIB_NAME:", name

	timeline = timeLine(lib, start, end)

	timeline_json = json.dumps(timeline, indent=4, separators=(',', ': '))

	print 'timeline has %s' % len(timeline.keys())

	lib_dir = os.path.join (globals.JSON_DATA_DIR, name)

	if not os.path.exists(lib_dir):
		os.mkdir(lib_dir)

	outfile = os.path.join (lib_dir, globals.sTime(start)+'.json')
	content = ' var %s_%s = %s' %(name, globals.getTime(start).year, timeline_json)

	# content = ' var ' + name + '_' + global.getTime(start).year + ' = ' \
	#             + json.dumps(timeline, indent=4, separators=(',', ': '))
	if dowrites:
		# fp = open(outfile, 'w')
		fp = codecs.open (outfile, 'w', 'utf8')

		# fp.write (content)
		# fp.write (json.dumps(timeline))
		fp.write (unicode(json.dumps(timeline)))
		fp.close()
		print 'wrote to ', outfile
	else:
		print json.dumps(content)
		print 'WOULD HAVE written to ', outfile


def writeLibTimelines (lib):
	start = globals.getTime("1997-01-01")
	while start < datetime.datetime.now():
		end = datetime.datetime(start.year, 12, 31)
		writeTimeLine(lib, start, end)
		start = start.replace(year=start.year+1)



if __name__ == "__main__":

	if 0:
		# data = 'videoStorageData'
		data = 'jloAlbumData'
		# data = 'purgAlbumData'
		# data = 'mediaAlbumData'
		data_file = os.path.join (globals.REPO_BASE, data, data + '.txt')
		writeLibTimelines (IPhotoLibrary(data_file))

	if 1:
		libs = [
			# 'videoStorageData',
			# 'jloAlbumData',
			# 'purgAlbumData',
			# 'mediaAlbumData',
			'mediaAlbumData_1',
			'mediaAlbumData_2',
			]

		for data in libs:
			data_file = os.path.join (globals.REPO_BASE, data, data + '.txt')
			writeLibTimelines (IPhotoLibrary(data_file))



