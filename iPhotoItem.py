"""
iPhotoItem - wrapper for xml representation of an item (photo) in iPhoto

Backed by IPhotoDict

exposes:
	exposes iPhoto metadata
	note: metadata contains path to photo, but file size not included
"""
import os, sys, time, datetime, re

from iPhoto import APPLE_BASE, getappletime, IPhotoDict
from tabdelimited import TabDelimitedRecord

import globals


class IPhotoItem_API (IPhotoDict):
	"""
	exposes the following from iPhoto metadata
		mediaType
		caption
		comment
		GUID
		aspectRatio
		rating
		date
		modDate
		metaModDate
		path
		thumbPath
		keywords
	
	"""

	attrs = globals.IPHOTO_ITEM_ATTRS

	def __init__ (self):
		for attr in self.attrs:
			setattr(self, attr, None)
		self.filename = None

	def __init__OFF (self, id, data, library):
		self.id = id
		self.library = library
		IPhotoDict.__init__ (self, data)
		self.mediaType = self['MediaType']
		self.caption = self['Caption']
		self.comment = self['Comment']
		self.GUID = self['GUID']
		self.aspectRatio = self['Aspect Ratio']
		self.rating = self['Rating']
		self.date = getappletime(self['DateAsTimerInterval'])
		self.modDate = getappletime(self['ModDateAsTimerInterval'])
		self.metaModDate = getappletime(self['MetaModDateAsTimerInterval'])
		self.path = self['ImagePath']
		self.thumbPath = self['ThumbPath']
		self.keywords = self['Keywords']
		
		self.filename = self.path and os.path.basename(self.path)
		if not self.filename:
			print "no filename for ", self.caption, self.GUID
			
	def report_verbose (self):
		
		print self.caption
		# for attr in ['caption', 'comment', 'date', 'modDate', 'metaModDate', 'path']:
		if 0:
			# for attr in ['caption', 'comment', 'date', 'modDate', 'metaModDate', 'path', 'keywords', 'thumbPath']:
			for attr in ['caption', 'comment', 'date', 'aspectRatio', 'thumbPath']:
				print "- %s: %s" % (attr, getattr(self, attr))
		else:
			print ''
			for key in self.keys():
				print "- %s: %s" % (key, self[key])
				
	def report (self):
		print ''
		for attr in ['path', 'caption', 'comment', 'date']:
			if getattr(self, attr):
				print '%s: %s' % (attr, getattr(self, attr))

	def file_exists(self):
		return os.path.exists(self.path)

	def syncAssetDate (self):
		# print '\nsyncAssetDate()'
		# print ' - date', self.date
		# print ' - modDate', self.modDate
		dateFormat = '%m/%d/%y'
		
		# print ' - FILE creation Date', time.ctime(os.path.getctime(self.path))
		# print ' - FILE mod Date', time.ctime(os.path.getmtime(self.path))
		
		# file creation time
		c_struct = self.date.timetuple()
		creationTime = time.mktime(c_struct)
		# print "\n timestamps for utime"
		
		# print "iPhoto Creation TIME: ", creationTime
		# print 'creationTime: %s (%s)' % (creationTime, time.asctime(c_struct))
		
		# mod time
		
		# m_struct = self.modDate.timetuple()
		# modTime = time.mktime(m_struct)
		# 
		# print "iPhoto MOD TIME: ", modTime
		# print 'modTime: %s (%s)' % (modTime, time.asctime(m_struct))		
		
		
		os.utime(self.path, (creationTime, creationTime))
		# print 'synced ', self.path

	def asTabDelimited (self):

		record = '\t'.join(map (lambda x:unicode(getattr(self, x)),
		                        globals.IPHOTO_ITEM_ATTRS))
		record = record.replace (chr(13), ' ').replace('\n', ' ')
		return record

class  IPhotoItem (IPhotoItem_API):

	def __init__ (self, id, data, library):
		self.id = id
		self.library = library
		IPhotoDict.__init__ (self, data)
		self.mediaType = self['MediaType']
		self.caption = self['Caption']
		self.comment = self['Comment']
		self.GUID = self['GUID']
		self.aspectRatio = self['Aspect Ratio']
		self.rating = self['Rating']
		self.date = getappletime(self['DateAsTimerInterval'])
		self.modDate = getappletime(self['ModDateAsTimerInterval'])
		self.metaModDate = getappletime(self['MetaModDateAsTimerInterval'])
		self.path = self['ImagePath']
		self.thumbPath = self['ThumbPath']
		self.keywords = self['Keywords']

		self.filename = self.path and os.path.basename(self.path)
		if not self.filename:
			print "no filename for ", self.caption, self.GUID


class IPhotoItemRecord (TabDelimitedRecord, IPhotoItem_API):
	def __init__ (self, data, library):
		"""
		library is parent (will be assigned by TabDelimitedRecord
		:param data:
		:param library:
		:return:
		"""

		# print "IPhotoItemRecord"
		TabDelimitedRecord.__init__(self, data, library)
		self.library = self.parent
		for attr in globals.IPHOTO_ITEM_ATTRS:
			setattr(self, attr, self[attr])



if __name__ == '__main__':
	pass

