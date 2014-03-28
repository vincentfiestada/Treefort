class Notification:
	## This class represents notification objects that inform the user when certain events occur in their network.
	## Conversations, Friendship, and Status objs generate notifications
	## See this project's class diagram for more info.

	def __init__(self, description):
		self.description = description
		self.read = False

	def isRead(self):
		return self.read
	
	def markRead(self):
		self.read = True

	def getDescription(self):
		return self.description