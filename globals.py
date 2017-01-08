__author__ = 'ostwald'

import os, sys, datetime, re
from UserDict import UserDict

# IPh0toItem MODEL - used by dumper and readers
IPHOTO_ITEM_ATTRS = ['mediaType', 'caption', 'comment', 'id', 'date', 'path', 'thumbPath', 'filename']

# Roll MODEL - used by dumper and readers
ROLL_ATTRS = ['name', 'id', 'start', 'end', 'size', 'comment']

# where we read and write iPhotoLibrary rep as tabDelimited
# REPO_BASE = '/Users/ostwald/tmp/iPhotoLibrary_XLS_Database'
REPO_BASE = '/Users/ostwald/devel/iPhoto/iPhotoLibrary_XLS_Database/'

# Source iPhotoLibrary data as XML (plist)
albumData_dir = '/Users/ostwald/devel/python/iPhoto/data/xml'

videoStorage_plist = os.path.join (albumData_dir, 'videoStorageData.xml')
mediaAlbum_1_plist = os.path.join (albumData_dir, 'mediaAlbumData_1.xml')
mediaAlbum_2_plist = os.path.join (albumData_dir, 'mediaAlbumData_2.xml')
jloAlbum_plist = os.path.join (albumData_dir, 'jloAlbumData.xml')
purgAlbum_plist = os.path.join (albumData_dir, 'purgAlbumData.xml')

JSON_DATA_DIR = '/Users/ostwald/devel/python/iPhoto/data/json/'

LIB_XLS_MAP = {
	'media_1': 'mediaAlbumData_1',
	'media_2': 'mediaAlbumData_2',
	'purg': 'purgAlbumData',
	'video': 'videoStorageData',
	'jlo': 'jloAlbumData',
    'mtSherman': 'MtShermanAlbumData',
    'pack161' : 'Pack161AlbumData'
}


def getTime(s):
	"""
	returns strings formatted as YYYY-MM-DD or mm/dd/%Y as time objects
	:param s:
	:return:
	"""
	# return time.strptime(s,"%Y-%m-%d")
	if type(s) == type(datetime.datetime.now()):
		return s
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

def sTime (date):
	"""
	return datetime formatted as "%Y-%m-%d"
	"""
	if type(date) == type(''):
		return getShortDateStr(date)
	return date.strftime("%Y-%m-%d")

shortDatePat = re.compile ("[\d]{4}-[\d]{2}-[\d]{2}")
def getShortDateStr (datestr):

	m = shortDatePat.search(datestr)
	if m:
		return m.group()

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

# print getTime('1997-01-01 00:00:00')