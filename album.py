from iPhoto import IPhotoDict

class Album (IPhotoDict):
	
	def __init__ (self, data, library):
		self.library = library
		IPhotoDict.__init__ (self, data)
		self.name = self['AlbumName']
		self.id = self['AlbumId']
		self.itemIds = self['KeyList']
		

