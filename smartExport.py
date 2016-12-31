"""
smartExport.py

iPhoto - Smart Export

for each roll:
	make rollExportDir
	for each item:
	- copy image at item.path to rollExportDir
      - set the modTime from the item.modDate
?finally, move rollExportDir to yearExportDir (as determined by roll.date)

"""
import sys, os, re, time, shutil
from libcmp import LibraryRollData, RollDataCompare
from iPhotoLibrary import IPhotoLibrary

class DupRoll (Exception):
	pass 

def getRollsToExport ():
	rolldata = 'data/xls'
	jloData = os.path.join (rolldata, 'JLO_iLibraryRolls.txt')
	mtShermanData = os.path.join (rolldata, 'MtShermanRollData.txt')
	timeMachineData = os.path.join (rolldata, 'timemachine-iPhotoRolls.txt')
	comp = RollDataCompare (jloData, timeMachineData)
	extras = comp.extras
	print "%d extras before filtering" % len(extras)
	
	# filter the ones marked skip
	extras = filter (lambda x:not x['skip'], extras)
	
	# print "%d extras AFTER filtering for skips" % len(extras)
	
	start = time.mktime(time.strptime("2005", "%Y"))
	# start = time.mktime(time.strptime("8/1/01", "%m/%d/%y"))
	extras = filter (lambda x:time.mktime(x.startDate) > start, extras)
	
	end = time.mktime(time.strptime("2006", "%Y"))
	extras = filter (lambda x:time.mktime(x.startDate) < end, extras)
	
	print "%d extras AFTER filtering" % len(extras)
	return extras

class SmartExporter:
	"""
	exports rolls per above
	"""
	dowrites = True
	strict = False
	baseExportDir = '/Volumes/Video Backup/Jlo_iPhotoLib_export/'
	slashPat = re.compile(".*[^\\\]/.*")
	
	def __init__ (self, libData, rollsToExport=None):
		self.lib = IPhotoLibrary(libData)
		self.rollsToExport = rollsToExport
		
	def export (self):
		if self.rollsToExport:
			rollIds = map (lambda x:x.id, self.rollsToExport)
		else:
			rollIds = self.lib.rollMap.keys()
			
		print 'exporting %d rolls' % len(rollIds)
		for rollId in rollIds:
			self.exportRoll(rollId)
		
	
	def quoteFileName (self, name):
		m = self.slashPat.match (name)
		if m:
			return name.replace('/', '\/', 100)
		else:
			return name
			
	def getExportDirForRoll (self, roll):
		yearDir = os.path.join (self.baseExportDir, str(roll.date.year))
		print "  export YEAR: ", roll.date.year
		if not os.path.exists(yearDir):
			os.mkdir (yearDir)
		if not os.path.exists(yearDir):
			raise IOError, "unable to create dir at %s" % yearDir
		# rollName = self.quoteFileName (roll.name)
		rollName = roll.name.replace ('/', '_', 100)
		rollDir = os.path.join (yearDir, rollName)
		
		# rollDir = os.path.join(yearDir, roll.name.replace('/', '\/'))
		
		if os.path.exists(rollDir):
			if self.strict:
				raise DupRoll, "roll already exists at %s" % rollDir
			else:
				i = 2
				while os.path.exists(rollDir):
					rollName = '%s_%d' % (rollName, i)
					rollDir = os.path.join (yearDir, rollName)
		
		os.mkdir (rollDir)
		if not os.path.exists(rollDir):
			raise IOError, "unable to create dir at %s" % rollDir
		return rollDir
		
	def exportRoll (self, rollId):
		roll = self.lib.getRollById (rollId)
		if roll is None:
			raise KeyError, 'Roll not found for ', rollId
			
		try:
			destDir = self.getExportDirForRoll(roll)
		except DupRoll:
			print "not exporting '%s' (%s)" % (roll.name, rollId)
			return
		
		print '\nExporting: "%s" (%d) - year: %d, id: %s' % (roll.name, len (roll), roll.date.year, roll.id)
		for id in roll.itemIds:
			item = roll.getItem(id)
			# print ' - %s - %s' % (item.caption, item.date)
			if self.dowrites:
				item.syncAssetDate()
				dst = os.path.join (destDir, os.path.basename(item.path))
				shutil.copyfile(item.path, dst)
				print 'copied ', dst
				creationTime = time.mktime(item.date.timetuple())
				os.utime(dst, (creationTime, creationTime))

	
# rollId: 30858 (pics mailed from ani)	- jloLib
# rollId: 222 (Pack Meeting - April 20)  -  pack161

def getRollsToExportTester():
	rolls = getRollsToExport()
	for roll in rolls:
		print '- %s - %s (%s)' % (roll.start, roll.name, roll.size)

if 1:
	libDataDir = 'data/xml'
	jloLibData = os.path.join (libDataDir, 'jloAlbumData.xml')
	exportList = getRollsToExport()
	exporter = SmartExporter(jloLibData, exportList)
	print 'Rolls to export (%d)' % len(exportList)
	for roll in exportList:
		print '- %s - %s (%s)' % (roll.start, roll.name, roll.size)
	# exporter.export()
	
if 0:
	libDataDir = 'data/xml'
	jloLibData = os.path.join (libDataDir, 'jloAlbumData.xml')
	exporter = SmartExporter(jloLibData)
	exporter.exportRoll(348)

if 0:
	pac161LibData = '/Users/ostwald/Desktop/Pack161AlbumData.xml'
	exporter = SmartExporter(pac161LibData)
	exporter.export()
