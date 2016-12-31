"""
Tools to get a handle on what is in a iPhoto Library

- list albums (rolls?)
- list items (album)


"""
__author__ = 'ostwald'

import os, sys
from iPhoto import IPhotoLibrary
from iPhoto import libcmp
from iPhoto import globals


def report (path):
	lib = IPhotoLibrary (path)
	lib.reportRolls()
	lib.reportAlbums()



if __name__ == "__main__":

	# files to us as input to comparison tools
	# rolldata = 'data/xls'

	if 0:
		rolls = libcmp.CompositeRollData (purgData, mtShermanData)
	if 0:
		rolls = libcmp.LibraryRollData (mediaAlbumDataShort)
		rolls.report()
	if 0:
		comp = libcmp.RollDataCompare (purgData, mediaAlbumData)
		comp.report()
	if 1:
		comp = libcmp.RollDataCompareUsingComposite (purgData, mediaAlbumData)
		comp.compare()
	# rolls.compare()
	# print '%d rolls read' % len(rolls)
	# rolls.report()


	# write spreadsheet data to disk


	print('done')