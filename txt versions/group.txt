## group.py - Class Definition for Group, an aggregation of Friendship objects
## Author   - Vincent Fiestada

from friendship import *

class Group:
	## 'members' argument should be iterable of Friendship objects
	def __init__(self, name, members = []):
		self.name = name
		self.members = members

	def getName(self):
		return self.name

	def setName(self, newname):
		self.name = newname

	def getMembers(self):
		return self.members

	def setMembers(self, members):
		self.members = members

	def unFriendAll(self):
		for friend in members:
			friend.unFriend()
			## del friend

	def hideAllUpdates(self):
		for friend in members:
			friend.setStatus("Hidden Updates")

	def blockAll(self):
		for friend in members:
			friend.block()