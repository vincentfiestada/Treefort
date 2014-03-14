## controlcenter.py - implements the Control Center interface, Database and Concrete User Builder
## Author           - Vincent Fiestada

import os
from shutil import copy
from userproxy import *
from group import *

ALLOWED_USRNAME_CHARS = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789 _-"

def validateUsername(name):
	for x in name:
		if x not in ALLOWED_USRNAME_CHARS:
			return False
	return True

def parseStatusCode(name):
	return name.replace('[R]', '').replace('[C]','').replace('[H]','').replace('[B]','').replace('[P]','')
def parseRealName(name):
	n = parseStatusCode(name)
	if ">>" in n:
		return n.split(">>")[1]
	else:
		return n

class Database:
	def __init__(self, filename):
		self.filename = filename
		self.Dict = None

	def getFilename(self):
		return self.filename

	def setUpdateFilename(self, newfilename):
		self.filename = newfilename

	def getDict(self):
		return self.Dict

	def getEntryByID(self, uid):
		return self.Dict[uid]

	def editEntryByID(self, uid, newvalue):
		self.Dict[uid] = newvalue

class MainDatabase(Database):
	## 'importDB()' function builds a dictionary of user credentials	
	def importDB(self):
		self.Dict = []
		handle = open(self.filename, 'r')
		idCounter = 0
		while(True):
			x = handle.readline().replace('\n', '')
			if x == "":
				break
			if ": " in x:
				userDictItem = dict()
				x_cred = x.lstrip().rstrip().split(": ")
				userDictItem['userID'] = idCounter
				idCounter += 1
				userDictItem['username'] = x_cred[0]
				userDictItem['password'] = x_cred[1]
				userDictItem['friends'] = []
				self.Dict.append(userDictItem)
			elif x[0] == '\t':
				self.Dict[-1]['friends'].append(x.lstrip().rstrip().replace('\t',''))
		handle.close()

	def getLastID(self):
		return len(self.Dict)-1

	def editEntryByID(self, uid, username = None, password = None, friends = None):
		if username != None:
			self.Dict[uid]['username'] = username
		if password != None:
			self.Dict[uid]['password'] = password
		if friends != None:
			self.Dict[uid]['friends'] = friends

	## 'friends' argument should be a list/tuple of str
	def insert(self, username, password, friends):
		self.Dict.append(dict(userID = self.getLastID()+1, username = username, password = password, friends = friends))

	## 'exportDB()' function saves db details
	def exportDB(self):
		handle = open(self.filename, 'w')
		for y in self.Dict:
			if y != self.Dict[0]:
				handle.write("\n")
			handle.write(y['username'] + ": " + y['password'])
			for x in y['friends']:
				handle.write("\n\t" + x)
		handle.close()

	def printUserDict(self):
		for x in self.userDict:
			print str(x['userID']) + "::" + x['username'] + ": " + x['password']
			for y in x['friends']:
				print ' --- ' + y

class UserConfigDatabase(Database):
	def importDB(self):
		self.Dict = dict()
		handle = open(self.filename, 'r')
		self.Dict['gender'] = handle.readline().replace('\n','').split(': ')[1]
		self.Dict['bday'] = dict()
		self.Dict['bday']['month'] = int(handle.readline().replace('\n','').split(': ')[1])
		self.Dict['bday']['day'] = int(handle.readline().replace('\n','').split(': ')[1])
		self.Dict['bday']['year'] = int(handle.readline().replace('\n','').split(': ')[1])
		self.Dict['jobs'] = list()
		for x in handle.readline().replace('\n','').split(': ')[1].split('|'):
			self.Dict['jobs'].append(x)
		self.Dict['education'] = list()
		for x in handle.readline().replace('\n','').split(': ')[1].split('|'):
			self.Dict['education'].append(x)
		handle.close()

	def exportDB(self):
		handle = open(self.filename, 'w')
		handle.write("Gender: "+self.Dict['gender']+"\n")
		handle.write("Bday-Month: "+str(self.Dict['bday']['month'])+"\n")
		handle.write("Bday-Day: "+str(self.Dict['bday']['day'])+"\n")
		handle.write("Bday-Year: "+str(self.Dict['bday']['year'])+"\n")
		separator = "|"
		handle.write("Jobs: "+separator.join(self.Dict['jobs'])+"\n")
		handle.write("Education: "+separator.join(self.Dict['education']))
		handle.close()

class ConcreteUserBuilder:
	## 'database' argument must be a MainDatabase object
	## 'bday' argument must be a dict with 'month', 'day', and 'year' members
	def newUser(self, database, username, password, gender, bday):
		## Trim username to remove leading whitespaces
		username = username.lstrip()
		if username == "":
			return "The username cannot be empty or all whitespaces (Leading whitespaces are automatically removed)."
		if password.lstrip() == "":
			return "The password cannot be empty or all whitespaces."
		if validateUsername(username) == False:
			return "The username contains characters that are not allowed.\nYou can use A-Z, a-z, 0-9, <space>, _ and - for a username."
		# check whether the username is already in use
		if username in ActiveUser.usedNames:
			return "There is already a user with the name '" + username + "'."
		self.registerToDB(database, username, password)
		self.makeFolder(user_name = username, user_gender = gender, user_bday = bday)
		return "SUCCESS"

	## The following functions are to be used internally by the Builder:
	def registerToDB(self, database, username, password):
		database.insert(username = username, password = password, friends = [])

	def makeFolder(self, user_name, user_gender, user_bday):
		os.mkdir("users/"+user_name)
		configFile = open("users/"+user_name+"/info.txt", 'w')
		configFile.write("Gender: " + user_gender + "\n")
		configFile.write("Bday-Month: " + user_bday['month'] + "\n")
		configFile.write("Bday-Day: " + user_bday['day'] + "\n")
		configFile.write("Bday-Year: " + user_bday['year'] + "\n")
		configFile.write("Jobs: \n")
		configFile.write("Education: ")
		configFile.close()
		## copy default profile picture into folder
		sourcepath = "img/defaultpic.gif"
		targetpath = "users/"+user_name+"/profile.gif"
		copy(sourcepath, targetpath)

class IControlCenter:
	database = None
	userBuilder = ConcreteUserBuilder()
	userRoster = list()
	selected = None
	lastfilename = ""

	def openDB(self, dbfilename):
		IControlCenter.lastfilename = dbfilename
		for x in IControlCenter.userRoster:
			del x
		IControlCenter.userRoster = []
		ActiveUser.usedNames = []
		ActiveUser.activeUsers = []
		IControlCenter.database = MainDatabase(filename=dbfilename)
		## import basic user info from file
		IControlCenter.database.importDB()
		## create list of user proxy objs
		idticker = 0
		for entry in IControlCenter.database.getDict():
			configFile = "users/" + entry['username'] + "/info.txt"
			## see if the file exists; if it doesn't make a new one
			if not os.path.exists(configFile):
				IControlCenter.userBuilder.makeFolder(user_name = entry['username'], user_gender = "U", user_bday = dict(month = "1", day = "1", year = "1"))
			userConfig = UserConfigDatabase(filename=configFile)
			IControlCenter.userRoster.append(UserProxy(uid=idticker, username=entry['username'], password=entry['password'], configDB = userConfig))
			idticker += 1

		## After all users have been created, assign the friends and create Group objects
		for user in IControlCenter.userRoster:
			friendlist = IControlCenter.database.getDict()[user.getUserID()]['friends']
			for name in friendlist:
				friendID = self.getUserByName(parseRealName(name)).getUserID()
				## parse status
				if "[R]" in name:
					status = "Requested"
				elif "[P]" in name:
					status = "Pending"
				elif "[C]" in name:
					status = "Close Friend"
				elif "[H]" in name:
					status = "Hidden Updates"
				elif "[B]" in name:
					status = "Blocked"
				else:
					status = "Friend"
				## parse group
				if ">>" in name:
					grouplist = parseStatusCode(name).split(">>")[0]
					groups = grouplist.split("|")
				else:
					groups = list()
				user.addFriendship(Friendship(userid = friendID, status = status, groups = groups))

	def newUser(self, username, password, gender, bday):
		resp = IControlCenter.userBuilder.newUser(IControlCenter.database, username, password, gender, bday)
		self.saveDB()
		self.openDB(IControlCenter.lastfilename)
		return resp

	def getUsers(self):
		return IControlCenter.userRoster
		
	def getUserById(self, uid):
		return IControlCenter.userRoster[uid]

	def editUserById(self, uid, username = None, password = None, friendlist = None):
		if username != None:
			oldusername = self.getUserById(uid).getUsername()
			##rename the folder of this user's settings
			os.rename("users/" + oldusername, "users/" + username)
			## edit this user's login credentials
			IControlCenter.userRoster[uid].setUsername(username)
			#print IControlCenter.userRoster[uid].getUsername()
			#IControlCenter.database.editEntryByID(uid, username = username)
			#print IControlCenter.database.getEntryByID(uid)['username']
			## update config database filename
			updatedConfigDB = UserConfigDatabase(filename = "users/" + username + "/info.txt")
			IControlCenter.userRoster[uid].editConfigDB(updatedConfigDB)
		if password != None:
			IControlCenter.userRoster[uid].setPassword(password)
			IControlCenter.database.editEntryByID(uid, password = password)
		if friendlist != None:
			IControlCenter.userRoster[uid].setFriends(friendlist)
			## build list of friends' names (formatted based on groups and statuses)
			friendsnames = list()
			for friendX in friendlist:
				thingToAppend = list()
				friendstat = friendX.getStatus()
				if friendstat == "Requested":
					thingToAppend.append("[R]")
				elif friendstat == "Pending":
					thingToAppend.append("[P]")
				elif friendstat == "Close Friend":
					thingToAppend.append("[C]")
				elif friendstat == "Hidden Updates":
					thingToAppend.append("[H]")
				elif friendstat == "Blocked":
					thingToAppend.append("[B]")

				friendgroups = friendX.getGroups()
				if len(friendgroups) > 0: ## if in at least one group, append the list of groups
					barsep = "|"
					grouplist = barsep.join(friendgroups)
					thingToAppend.append(grouplist)
					thingToAppend.append(">>")
				## finally, append username
				thingToAppend.append(self.getUserById(friendX.getFriendID()).getUsername())
				blanksep = ""
				friendsnames.append(blanksep.join(thingToAppend))
			IControlCenter.database.editEntryByID(uid, friends = friendsnames)

		self.setSelected(uid)

	def addFriendshipById(self, uid, friendID):
		## add friendship to sender ('Requested' must be approved)
		IControlCenter.userRoster[uid].addFriendship(Friendship(userid = friendID, status = "Requested"))
		## add friendship to sendee ('Pending' can approve 'Requested')
		IControlCenter.userRoster[friendID].addFriendship(Friendship(userid = uid, status = "Pending"))
		## update Database
		IControlCenter.database.editEntryByID(uid, friends = IControlCenter.database.getEntryByID(uid)['friends'].append("[R]" + IControlCenter.userRoster[friendID].getUsername()))
		IControlCenter.database.editEntryByID(friendID, friends = IControlCenter.database.getEntryByID(friendID)['friends'].append("[P]" + IControlCenter.userRoster[uid].getUsername()))

	def setSelected(self, id):
		if id not in range(len(IControlCenter.userRoster)):
			IControlCenter.selected = None
		else:
			IControlCenter.selected = id

	def getSelected(self):
		if IControlCenter.selected != None:
			return IControlCenter.userRoster[IControlCenter.selected]
		else:
			return None

	def saveDB(self):
		if IControlCenter.database != None:
			for userprofile in IControlCenter.userRoster:
				## update config Database
				userprofile.configDB.editEntryByID('gender', newvalue = userprofile.getGender()[0])
				userprofile.configDB.editEntryByID('bday', newvalue = userprofile.getBdayDict())
				userprofile.configDB.editEntryByID('jobs', newvalue = userprofile.getJobHistory())
				userprofile.configDB.editEntryByID('education', newvalue = userprofile.getEducationHistory())
				## update friends
				## first, build list of friends (formatted)
				friendslist = list()
				for friendX in userprofile.getFriends():
					thingToAppend = list()
					friendstat = friendX.getStatus()
					if friendstat == "Requested":
						thingToAppend.append("[R]")
					elif friendstat == "Pending":
						thingToAppend.append("[P]")
					elif friendstat == "Close Friend":
						thingToAppend.append("[C]")
					elif friendstat == "Hidden Updates":
						thingToAppend.append("[H]")
					elif friendstat == "Blocked":
						thingToAppend.append("[B]")

					friendgroups = friendX.getGroups()
					if len(friendgroups) > 0: ## if in at least one group, append the list of groups
						barsep = "|"
						grouplist = barsep.join(friendgroups)
						thingToAppend.append(grouplist)
						thingToAppend.append(">>")
					## finally, append username
					thingToAppend.append(self.getUserById(friendX.getFriendID()).getUsername())
					blanksep = ""
					friendslist.append(blanksep.join(thingToAppend))
				IControlCenter.database.editEntryByID(userprofile.getUserID(), userprofile.getUsername(), password = userprofile.getPassword(), friends = friendslist)
				userprofile.configDB.exportDB()
			IControlCenter.database.exportDB()

	def getUserByName(self, username):
		user = None
		for profile in self.userRoster:
			if profile.getUsername() == username:
				user = profile
				break
		return user

	def loginUser(self, username, password):
		user = self.getUserByName(username)
		if user != None:
			if password == user.getPassword():	
				user.login()
				return "SUCCESS"
				self.setSelected(user.getUserID())
			else:
				return "Login Failed. The username and/or password was incorrect.\nTry again."
		else:
			return "Login Failed. There is currently no user with that name.\nTry again."

	## 'user' argument must be a UserProxy object
	def logoutUser(self, uid):
		self.getUserById(uid).logout()