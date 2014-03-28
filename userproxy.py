## userproxy.py - Class Definition for UserProxy, a proxy class for ActiveUser that handles it before the user logs in.
## Author       - Vincent Fiestada

from user import *
from friendship import *
from controlcenter import *

class UserProxy:
	def __init__(self, uid, username, password, configDB):
		self.actualuser = None
		## The following variables may be accessed readily even
		## before the ActiveUser object is created:
		self.userID = uid
		self.login_username = username
		self.login_password = password
		self.profilePic = None
		## Used to keep track of whether the ActiveUser object has been created
		self.loggedIn = False

		##configDB is the database that contains additional details about the user
		##the UserProxy will use it to initialize the actual User object
		self.configDB = configDB

	def isLoggedIn(self):
		return self.loggedIn

	def login(self):
		## Abort if already logged in
		if self.isLoggedIn():
			return True
		if self.actualuser == None:
			self.createActiveUser()
		self.loggedIn = True
		ActiveUser.activeUsers.append(self.userID)
		return True

	def logout(self):
		## Abort if not logged in
		if self.isLoggedIn():
			self.actualuser.logout()
			self.loggedIn = False

	def getUsedNames(self):
		return ActiveUser.usedNames

	def getActiveUsers(self):
		return ActiveUser.activeUsers

	def getUserID(self):
		return self.userID

	def getGender(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getGender()

	def setGender(self, newgender):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setGender(newgender)

	def getAge(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getAge()

	def getBday(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getBday()

	def getBdayDict(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getBdayDict()

	def setBday(self, newbday):
		if self.actualuser == None:
			self.createActiveUser()
		## newbday must be a dictionary with entries year, month, and day
		self.actualuser.setBday(newbday)

	def getProfilePic(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getProfilePic()

	def getUsername(self):
		if self.actualuser == None:
			return self.login_username
		return self.actualuser.getUsername()

	def setUsername(self, newname):
		if self.actualuser == None:
			self.createActiveUser()
		resp = self.actualuser.setUsername(newname)
		if resp == "SUCCESS":
			self.login_username = newname

	def resetProfilePic(self):
		if self.actualuser != None:
			self.actualuser.resetProfilePic()

	def getPassword(self):
		if self.actualuser == None:
			return self.login_password
		return self.actualuser.getPassword()

	def setPassword(self, newpass):
		if self.actualuser != None:
			self.actualuser.setPassword(newpass)
		self.login_password = newpass

	def getJobHistory(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getJobHistory()

	def setJobHistory(self, joblist):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setJobHistory(joblist)

	def getEducationHistory(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getEducationHistory()

	def setEducationHistory(self, edulist):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setEducationHistory(edulist)

	def getFriends(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getFriends()

	def addFriendship(self, friendship):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.addFriendship(friendship)

	def setFriends(self, newfriendlist):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setFriends(newfriendlist)

	def unfriendById(self, uid):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.unfriendById(uid)

	def getConversations(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getConversations()

	def addConversation(self, conversation):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.addConversation(conversation)

	def setConversations(self, newconversationslist):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setConversations(newconversationslist)

	def exitConversation(self, conversationtoexit):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.exitConversation(conversationtoexit)

	def getNotifications(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getNotifications()
	
	def addNotification(self, text):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.addNotification(text)

	def getNotificationByIndex(self, index):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getNotificationByIndex(index)

	def getStatuses(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getStatuses()

	def getNewsfeed(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.getNewsfeed()

	def addStatus(self, status):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.addStatus(status)

	def deleteStatusByValue(self, todelete):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.deleteStatusByValue(todelete)

	def setStatuses(self, statuslist):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setStatuses(statuslist)

	def setNewsfeed(self, newsfeed):
		if self.actualuser == None:
			self.createActiveUser()
		self.actualuser.setNewsfeed(newsfeed)

	def getConfigDB(self):
		return self.configDB

	def editConfigDB(self, newDB):
		self.configDB = newDB
		self.configDB.importDB()

	def gettimeLineSelectedFriend(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.gettimeLineSelectedFriend()
	
	def gettimeLineSelectedIndex(self):
		if self.actualuser == None:
			self.createActiveUser()
		return self.actualuser.gettimeLineSelectedIndex()
	
	def settimeLineSelectedFriend(self, uid):
		if self.isLoggedIn() != False:
			self.actualuser.settimeLineSelectedFriend(uid)
	
	def settimeLineSelectedIndex(self, index):
		if self.isLoggedIn() != False:
			self.actualuser.settimeLineSelectedIndex(index)

	def createActiveUser(self):
		if self.configDB.getDict() == dict():
			self.configDB.importDB()
		configDetails = self.configDB.getDict()
		self.actualuser = ActiveUser(uid=self.userID ,username=self.login_username, password=self.login_password, gender=configDetails['gender'], bday=configDetails['bday'], jobs=configDetails['jobs'], edu=configDetails['education'], notifs = configDetails['notifs'])