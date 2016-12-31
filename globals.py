__author__ = 'ostwald'

import os, sys, datetime
from UserDict import UserDict

# IPh0toItem MODEL - used by dumper and readers
IPHOTO_ITEM_ATTRS = ['mediaType', 'caption', 'comment', 'id', 'date', 'path', 'thumbPath', 'filename']

# Roll MODEL - used by dumper and readers
ROLL_ATTRS = ['name', 'id', 'start', 'end', 'size', 'comment']

# where we read and write iPhotoLibrary rep as tabDelimited
REPO_BASE = '/Users/ostwald/tmp/iPhotoLibrary_XLS_Database'

# Source iPhotoLibrary data as XML (plist)
albumData_dir = '/Users/ostwald/devel/python/iPhoto/data/xml'

videoStorage_plist = os.path.join (albumData_dir, 'videoStorageData.xml')
mediaAlbum_plist = os.path.join (albumData_dir, 'mediaAlbumData.xml')
jloAlbum_plist = os.path.join (albumData_dir, 'jloAlbumData.xml')
purgAlbum_plist = os.path.join (albumData_dir, 'purgAlbumData.xml')



def getTime(s):
	"""
	returns strings formatted as YYYY-MM-DD or mm/dd/%Y as time objects
	:param s:
	:return:
	"""
	# return time.strptime(s,"%Y-%m-%d")

	formats = [
		"%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y",
		'%Y-%m-%d %H:%M:%S' # appletime
	]

	for fmt in formats:

		try:
			return datetime.datetime.strptime(s, fmt)
		except:
			# print 'WARN: could not parse date string: %s' % s
			pass
	raise Exception, "could not parse provided data string: %s" % s

## from phoshare.applexml
APPLE_BASE = 978307200 # 2001/1/1

def getappletime(value):
	'''Converts a numeric Apple time stamp into a date and time'''
	try:
		if value is None:
			raise ValueError, "No value provided"
		return datetime.datetime.fromtimestamp(APPLE_BASE + float(value))
	except ValueError, _e:
		# bad time stamp in database, default to "now"
		return datetime.datetime.now()

class IPhotoDict (UserDict):
	"""
	Extends UserDict
	- reporting
	- safe getitem
	"""
	def __getitem__ (self, key):
		if not self.data.has_key(key):
			return None
		return self.data[key]

	def reportKeys (self):
		for key in self.keys():
			print '%s (%s)' % (key, self[key].__class__.__name__)

	def report (self):
		for key in self.keys():
			print '%s: %s (%s)' % (key, self[key], self[key].__class__.__name__)

print getTime('2006-01-04 13:16:21')