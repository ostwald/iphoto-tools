"""
Tools to get a handle on what is in a iPhoto Library

- list albums (rolls?)
- list items (album)


"""
__author__ = 'ostwald'

import os, sys, json
from iPhoto import IPhotoLibrary
from iPhoto import libcmp
from iPhoto import globals, DumperIPhotoLibrary
from timeline import writeLibTimelines

def updateAllTabdelimitedData ():

	for filename in os.listdir(globals.albumData_dir):
		print filename
		if filename.startswith('.') or not filename.endswith('.xml'):
			continue
		data_file = os.path.join(globals.albumData_dir, filename)
		updateTabdelimitedData(data_file)

def updateTabdelimitedData (data_file):
	filename = os.path.basename(data_file)
	print 'updating %s ...' % filename
	try:
		lib = DumperIPhotoLibrary (data_file)
		# lib.reportRolls()
		lib.dump()
	except IOError, msg:
		print 'Error dumping %s: %s' % (filename, msg)

def dumpLibRollData (lib):
	records = []
	for roll in lib.rolls:
		data = {}
		for attr in globals.ROLL_ATTRS:
			data[attr] = str(roll[attr])
		records.append(data)

	# print json.dumps(records, indent=2)

	lib_dir = os.path.join (globals.JSON_DATA_DIR, lib.name)

	if not os.path.exists(lib_dir):
		os.mkdir(lib_dir)

	outfile = os.path.join (lib_dir, 'roll-data.json')
	fp = open(outfile, 'w')
	fp.write (json.dumps(records, indent=4))
	fp.close()
	print 'wrote to ',outfile

def updateLibraryData (name):
	print 'updating from %s library ...' % name

	if 1: # update the tab delimited xls roll data
		xml_data_file = os.path.join (globals.albumData_dir, name+'.xml')
		if not os.path.exists(xml_data_file):
			raise Exception, "xml_data_file does not exist at '%s'" % xml_data_file

		try:
			updateTabdelimitedData (xml_data_file)
		except Exception, msg:
			raise Exception, 'Could not update xsl data: %s' % msg

	if 1: # create json (roll-data and timelines) files used by javascript
		xls_data_file = os.path.join (globals.REPO_BASE, name, name + '.txt')
		if not os.path.exists(xls_data_file):
			raise Exception, "xls_data_file does not exist at '%s'" % xml_data_file

		lib = IPhotoLibrary(xls_data_file)
		# dumpLibRollData(lib)

		if 1: #dump timelines
			writeLibTimelines(lib)
	print "Update of %s library data completed" % name

def dumpAllRollData():
	libs = [
		'videoStorageData',
		'jloAlbumData',
		'purgAlbumData',
		'mediaAlbumData',
		]

	for data in libs:
		data_file = os.path.join (globals.REPO_BASE, data, data + '.txt')
		lib = IPhotoLibrary(data_file)
		dumpLibRollData(lib)


if __name__ == "__main__":
	# updateAllTabdelimitedData()

	# data = 'mediaAlbumData'
	# data = 'videoStorageData'
	data = 'purgAlbumData'
	data_file = os.path.join (globals.REPO_BASE, data, data + '.txt')

	if 0:
		lib = IPhotoLibrary(data_file)
		dumpLibRollData(lib)
	elif 0:
		dumpAllRollData()
	elif 1:
		# updateLibraryData('mediaAlbumData_2')
		updateLibraryData('jloAlbumData')