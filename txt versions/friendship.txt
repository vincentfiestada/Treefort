class Friendship:
	def __init__(self, userid, status = "Friend", groups = []):
		self.friendID = userid
		self.status = status ## str
		self.groups = groups ## list of str

	def getFriendID(self):
		return self.friendID

	def getStatus(self):
		## Status can be [F]riend, [C]lose Friend, [H]idden Updates, [B]locked, [R]equested (if this is the user who sent the friend request),and [P]ending (if this is the user who 'recieves' the friend request)
		return self.status

	def getGroups(self):
		return self.groups

	def setStatus(self, newstatus):
		if newstatus == "F":
			self.status = "Friend"
		elif newstatus == "C":
			self.status = "Close Friend"
		elif newstatus == "H":
			self.status = "Hidden Updates"
		elif newstatus == "B":
			self.status = "Blocked"
		elif newstatus == "R":
			self.status = "Requested"
		elif newstatus == "P":
			self.status = "Pending"

	def addGroup(self, groupname):
		if groupname not in self.groups:
			self.groups.append(groupname)

	def removeGroup(self, groupname):
		if groupname in self.groups:
			self.groups.remove(groupname)