"""
Timespan compare:

get the photo itmes for a given span

we want a report of phototos that are in one lib but not in another.

e.g., lib_1, and lib_2
we don't care about what items are in lib_1 but not in lib_2.
we only care about items that are in lib2 but not in lib one


"""
import sys, os
from iPhoto import globals, IPhotoLibrary

__author__ = 'ostwald'

class TimeCompare():
	def __init__ (self, lib1, lib2, start, end):
		self.lib1 = lib1
		self.library1 = self.get_library(self.lib1)
		self.lib2 = lib2
		self.library2 = self.get_library(self.lib2)

		self.start = globals.getTime(start)
		self.end = globals.getTime(end)

		self.lib1_items = self.get_items (self.library1, start, end)
		self.lib2_items = self.get_items (self.library2, start, end)

	def report (self):
		print "REPORT"
		print ' - start: %s' % globals.sTime(start)
		print ' - end: %s' % globals.sTime(end)
		print '1 - %s (%s)' % (self.library1.name, len(self.lib1_items))
		print '2 - %s (%s)' % (self.library2.name, len(self.lib2_items))

	def get_library (self, lib):
		lib_name = globals.LIB_XLS_MAP[lib]
		data_file = os.path.join (globals.REPO_BASE, lib_name, lib_name + '.txt')
		return IPhotoLibrary(data_file)

	def get_items (self, library, start, end):
		return library.getItems(start=self.start, end=self.end)


if __name__ == '__main__':
	# lib1 = "purg"
	# lib2 = 'media_2'

	lib1 = "jlo"
	lib2 = 'video'

	start = '2010-09-01'
	end = '2010-09-30'

	tc = TimeCompare(lib1, lib2, start, end)
	tc.report()