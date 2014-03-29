## controlcenter.py - implements the Control Center interface, Database and Concrete User Builder
## Author           - Vincent Fiestada

import os
from shutil import copy, rmtree
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
		self.Dict = list()

	def getFilename(self):
		return self.filename

	def setUpdateFilename(self, newfilename):
		self.filename = newfilename

	def getDict(self):
		return self.Dict
	
	def clearDict(self):
		del self.Dict
		self.Dict = list()

	def getEntryByID(self, uid):
		return self.Dict[uid]
	
	def insert(self, newthing):
		self.Dict.append(newthing)

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
		if self.Dict != None and self.Dict != list():
			return self.Dict[-1]['userID']
		return 0

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

class ConversationsDatabase(Database):
	def importDB(self):
		self.Dict = list()
		handle = open(self.filename, 'r')
		while(True):
			x = handle.readline().replace('\n', '').rstrip()
			if x == "":
				break
			else:
				if x[0] != "\t":
					## A new conversation
					self.Dict.append(dict(members = x.lstrip().split('|'), messages = list()))
				else:
					self.Dict[-1]['messages'].append(x.lstrip())
		handle.close()

	def insert(self, members, messages):
		self.Dict.append(dict(members = members, messages = messages))

	def exportDB(self):
		barsep = "|"
		handle = open(self.filename, 'w')
		for entry in self.Dict:
			if entry != self.Dict[0]:
				handle.write("\n")
			handle.write(barsep.join(entry['members']))
			for msg in entry['messages']:
				handle.write("\n\t" + msg)
		handle.close()

class StatusFeedDatabase(Database):
	def importDB(self):
		self.Dict = list()
		handle = open(self.filename, 'r')
		while(True):
			x = handle.readline().replace('\n', '').rstrip()
			if x == "":
				break
			else:
				if x[0] != "\t":
					## A new status post
					xstamp = x.split(">>")
					self.Dict.append(dict(poster=xstamp[0], timestamp = float(xstamp[1]), text = "", attachments = [], tags = [], comments = [], up = [], down = []))
				else:
					marker = x.lstrip().split(": ")[0]
					if marker == "Text":
						self.Dict[-1]['text'] = x.lstrip().replace("Text: ", "")
					elif marker == "Attachments":
						self.Dict[-1]['attachments'] = x.lstrip().replace("Attachments: ", "")
					elif marker == "Tagged":
						self.Dict[-1]['tags'] = list(x.lstrip().replace("Tagged: ", "").split('|'))
					elif marker == "Comments":
						self.Dict[-1]['comments'] = list(dict(commentator = y.split(": ")[0], text = y.split(": ")[1]) for y in x.lstrip().replace("Comments: ", "").split('|'))
					elif marker == "Thumbs Up":
						self.Dict[-1]['up'] = list(x.lstrip().replace("Thumbs Up: ", "").split('|'))
					elif marker == "Thumbs Down":
						self.Dict[-1]['down'] = list(x.lstrip().replace("Thumbs Down: ", "").split('|'))
		handle.close()

	def exportDB(self):
		barsep = "|"
		handle = open(self.filename, 'w')
		for item in self.Dict:
			if item != self.Dict[0]:
				handle.write("\n")
			handle.write(item['poster'] + ">>" + str(item['timestamp']) + "\n")
			handle.write("\tText: " + item['text'] + "\n")
			handle.write("\tAttachments: " + barsep.join(item['attachments']) + "\n")
			handle.write("\tTagged: " + barsep.join(item['tags']) + "\n")
			handle.write("\tComments: " + barsep.join((k['commentator'] + ": " + k['text'] for k in item['comments'])) + "\n")
			handle.write("\tThumbs Up: " + barsep.join(item['up']) + "\n")
			handle.write("\tThumbs Down: " + barsep.join(item['down']))
		handle.close()

	def insert(self, poster, timestamp, text, attachments = [], tags = [], comments = [], up = [], down = []):
		self.Dict.append(dict(poster = poster, timestamp = timestamp, text = text, attachments = attachments, tags = tags, comments = comments, up = up, down = down))
		## each item in comments list must be a dict with 'commentator' and 'text' items

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
		handle.readline()
		self.Dict['notifs'] = list()
		while True:
			x = handle.readline().lstrip().rstrip()
			if x == "":
				break
			self.Dict['notifs'].append(x)
		handle.close()

	def clearDict(self):
		self.Dict = dict()

	def exportDB(self):
		handle = open(self.filename, 'w')
		handle.write("Gender: "+self.Dict['gender']+"\n")
		handle.write("Bday-Month: "+str(self.Dict['bday']['month'])+"\n")
		handle.write("Bday-Day: "+str(self.Dict['bday']['day'])+"\n")
		handle.write("Bday-Year: "+str(self.Dict['bday']['year'])+"\n")
		separator = "|"
		handle.write("Jobs: "+separator.join(self.Dict['jobs'])+"\n")
		handle.write("Education: "+separator.join(self.Dict['education'])+"\n")
		handle.write("Notifications: \n")
		for x in self.Dict['notifs']:
			handle.write(x + "\n")
		handle.close()

class ConcreteUserBuilder:
	## 'database' argument must be a MainDatabase object
	## 'bday' argument must be a dict with 'month', 'day', and 'year' members
	def newUser(self, database, username, password, gender, bday):
		## Trim username to remove leading whitespaces
		username = username.lstrip().rstrip()
		password = password.lstrip().rstrip()
		if username == "":
			return "The username cannot be empty or all whitespaces (Leading and trailing whitespaces are automatically removed)."
		if password == "":
			return "The password cannot be empty or all whitespaces (Leading and trailing whitespaces are automatically removed)."
		if validateUsername(username) == False:
			return "The username contains characters that are not allowed.\nYou can use A-Z, a-z, 0-9, <space>, _ and - for a username."
		# check whether the username is already in use
		if username in ActiveUser.usedNames:
			return "There is already a user with the name '" + username + "'."
		self.registerToDB(database, username, password)
		resp = self.makeFolder(user_name = username, user_gender = gender, user_bday = bday)
		if resp != "SUCCESS":
			return resp
		return "SUCCESS"

	## The following functions are to be used internally by the Builder:
	def registerToDB(self, database, username, password):
		database.insert(username = username, password = password, friends = [])

	def makeFolder(self, user_name, user_gender, user_bday):
		try:
			os.mkdir("users/"+user_name)
		except:
			return "There was an error in creating a folder and files for this user."
		configFile = open("users/"+user_name+"/info.txt", 'w')
		configFile.write("Gender: " + user_gender + "\n")
		configFile.write("Bday-Month: " + user_bday['month'] + "\n")
		configFile.write("Bday-Day: " + user_bday['day'] + "\n")
		configFile.write("Bday-Year: " + user_bday['year'] + "\n")
		configFile.write("Jobs: \n")
		configFile.write("Education: \n")
		configFile.write("Notifications: \n")
		configFile.close()
		## copy default profile picture into folder
		sourcepath = "img/defaultpic.gif"
		targetpath = "users/"+user_name+"/profile.gif"
		if not os.path.exists(targetpath):
			try:
				copy(sourcepath, targetpath)
			except:
				return "There was an error making the file."
		return "SUCCESS"

class IControlCenter:
	database = None
	database_conversations = None
	database_feed = None
	userBuilder = ConcreteUserBuilder()
	newsfeedAggregator = NewsFeedAggregator()
	userRoster = list()
	conversationRoster = list()
	selected = None
	usersToDelete = list()

	def openDB(self, dbfilename, db_convfilename, db_feedfilename):
		## store last used database filenames
		self.dbfilename = dbfilename
		self.db_convfilename = db_convfilename
		self.db_feedfilename = db_feedfilename

		## check if the files exist
		if not os.path.exists(self.dbfilename):
			return "The file '" + self.dbfilename + "' does not exist"
		if not os.path.exists(self.db_convfilename):
			return "The file '" + self.db_convfilename + "' does not exist"
		if not os.path.exists(self.db_feedfilename):
			return "The file '" + self.db_feedfilename + "' does not exist"

		IControlCenter.lastfilename = dbfilename
		#for x in IControlCenter.userRoster:
		#	del x
		IControlCenter.userRoster = list()
		ActiveUser.usedNames = list()
		IControlCenter.database = MainDatabase(filename=self.dbfilename)
		IControlCenter.database_conversations = ConversationsDatabase(filename=self.db_convfilename)
		IControlCenter.database_feed = StatusFeedDatabase(filename = self.db_feedfilename)
		## import basic user info from file
		try:
			IControlCenter.database.importDB()
		except:
			return "The main database file ('" + self.dbfilename + "') could not be imported successfully. It might be corrupted. Please check the file's contents and see if they are consistent with the specifications of Tree Fort."
		## create list of user proxy objs
		idticker = 0
		for entry in IControlCenter.database.getDict():
			configFile = "users/" + entry['username'] + "/info.txt"
			## see if the file exists; if it doesn't make a new one
			if not os.path.exists(configFile):
				IControlCenter.userBuilder.makeFolder(user_name = entry['username'], user_gender = "U", user_bday = dict(month = "7", day = "23", year = "1996"))
			try:
				userConfig = UserConfigDatabase(filename=configFile)
				userConfig.importDB()
			except:
				return "There was an error reading the file '" + configFile + "'. Please check its contents to make sure they follow the program specifications."
			IControlCenter.userRoster.append(UserProxy(uid=idticker, username=entry['username'], password=entry['password'], configDB = userConfig))
			idticker += 1

		## After all users have been created, assign the friends and create Group objects
		for user in IControlCenter.userRoster:
			friendlist = IControlCenter.database.getDict()[user.getUserID()]['friends']
			for name in friendlist:
				try:
					friendID = self.getUserByName(parseRealName(name)).getUserID()
				except:
					return "The main database file ('" + self.dbfilename + "') might be corrupted. The name '" + name + "' is listed as a friend but is not listed as a User."
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

		## log in users in ActiveUser.activeUsers list
		for id in ActiveUser.activeUsers:
			self.getUserById(id).login()

		## Add conversation objects to users
		IControlCenter.conversationRoster = list()
		try:
			IControlCenter.database_conversations.importDB()
		except:
			return "The conversations database file ('" + self.db_convfilename + "') could not be imported successfully. It might be corrupted. Please check the file's contents and see if they are consistent with the specifications of Tree Fort."
		for entry in IControlCenter.database_conversations.getDict():
			try:
				memberIDs = list({self.getUserByName(member).getUserID() for member in entry['members']})
			except:
				return "The conversations database file ('" + self.db_convfilename + "') could not be imported successfully. It might be corrupted. Please check the file's contents and see if they are consistent with the specifications of Tree Fort."
			newConversationObject = Conversation(members = memberIDs)
			## add messages to the conversation
			for messageEntry in entry['messages']:
				messageDetails = messageEntry.split(": ")
				newConversationObject.newMessage(sender = self.getUserByName(messageDetails[0]).getUserID(), text = messageDetails[1])
			## add conversation to each member's conversations list
			for uid in newConversationObject.getMembers():
				self.getUserById(uid).addConversation(newConversationObject)
			IControlCenter.conversationRoster.append(newConversationObject)

		## Add status objects to users
		try:
			IControlCenter.database_feed.importDB()
		except:
			return "The feed/status database file ('" + self.db_feedfilename + "') could not be imported successfully. It might be corrupted. Please check the file's contents and see if they are consistent with the specifications of Tree Fort."
		for entry in IControlCenter.database_feed.getDict():
			try:
				commentObjs = list(Comment(self.getUserByName(k['commentator']).getUserID(), k['text']) for k in entry['comments'])
				newStatusObject = Status(text = entry['text'], poster = self.getUserByName(entry['poster']).getUserID(), timestamp = entry['timestamp'], attachments = entry['attachments'], tags = list(self.getUserByName(k).getUserID() for k in entry['tags']), up = list(self.getUserByName(k).getUserID() for k in entry['up']), comments = commentObjs, down = list(self.getUserByName(d).getUserID() for d in entry['down']))
			except:
				return "The feed/status database file ('" + self.db_feedfilename + "') could not be imported successfully. It might be corrupted. Please check the file's contents and see if they are consistent with the specifications of Tree Fort."
			self.getUserById(newStatusObject.getPoster()).addStatus(newStatusObject)
		return "SUCCESS"

	def newUser(self, username, password, gender, bday):
		resp = IControlCenter.userBuilder.newUser(IControlCenter.database, username, password, gender, bday)
		if resp == "SUCCESS":
			## create an object to represent the new user and add it to the user roster;
			configdb = UserConfigDatabase("users/"+username.lstrip().rstrip()+"/info.txt")
			configdb.importDB()
			IControlCenter.userRoster.append(UserProxy(IControlCenter.database.getLastID() + 1, username, password, configdb))
			self.saveDB()
			opresp = self.openDB(self.dbfilename, self.db_convfilename, self.db_feedfilename)
			if opresp != "SUCCESS":
				return opresp
			self.setSelected(IControlCenter.database.getLastID())
		return resp

	def getUsers(self):
		return IControlCenter.userRoster
		
	def getUserById(self, uid):
		return IControlCenter.userRoster[uid]

	def editUserById(self, uid, username = None, password = None, friendlist = None, profilepic = None, gender = None, bday = None, jobhistory = None, eduhistory = None):
		targetUser = self.getUserById(uid)
		oldusername = targetUser.getUsername()

		## gather list of people to be notified; users who've marked this user as a 'Close Friend'
		toBeNotified = list()
		for friendship in IControlCenter.userRoster[uid].getFriends():
			if uid in list(f.getFriendID() for f in IControlCenter.userRoster[friendship.getFriendID()].getFriends() if f.getStatus() == "Close Friend"):
				toBeNotified.append(IControlCenter.userRoster[friendship.getFriendID()])
		
		if username != None:
			username = username.lstrip().rstrip()
			## check if empty
			if username == "":
				return "Username can't be an empty string (Leading and trailing whitespace is automatically removed)."
			## check if username is already used
			if username != oldusername and username in self.getSelected().getUsedNames():
				return "The username '"+username+"' is already in use."
			## check if username is valid
			if validateUsername(username) == False:
				return "The username '"+username+"' contains invalid characters. You can use A-Z, a-z, 0-9, <space>, _ and - in your username."
		else:
			username = oldusername
		if password != None:
			password = password.lstrip().rstrip()
			## check if empty
			if password == "":
				return "Your Password can't be empty. (Leading and trailing whitespaces are automatically deleted)"
			targetUser.setPassword(password)
		if friendlist != None:
			targetUser.setFriends(friendlist)
		if gender != None:
			oldgender = targetUser.getGender()
			targetUser.setGender(gender)
			newgender = targetUser.getGender()
			if newgender != oldgender:
				targetUser.addStatus(Status(poster = uid, text = "Pay Attention! I just set my gender to " + targetUser.getGender()))
				for x in toBeNotified:
					x.addNotification("Your close friend " + IControlCenter.userRoster[uid].getUsername() + " just edited their Profile Gender to: '" + newgender + "'.")
		if bday != None:
			oldbday = targetUser.getBdayDict()
			targetUser.setBday(bday)
			if bday != oldbday:
				targetUser.addStatus(Status(poster = uid, text = "Hey, look! I've set my birthday to " + targetUser.getBday()))
				for x in toBeNotified:
					x.addNotification("Check it out! Your close friend " + IControlCenter.userRoster[uid].getUsername() + " was born on: '" + targetUser.getBday() + "'.")
		if jobhistory != None:
			oldjobhistory = list(x for x in targetUser.getJobHistory() if x != '')
			targetUser.setJobHistory(jobhistory)
			jobList = targetUser.getJobHistory()
			if jobList == list():
				jobStrList = "I don't have any jobs in my list."
			else:
				sep = "; "
				jobStrList = "I've worked in the following jobs: " + sep.join(jobList) + "."
			if jobList != oldjobhistory:
				targetUser.addStatus(Status(poster = uid, text = "Did you Know? I just edited my Job History. " + jobStrList))
				for x in toBeNotified:
					x.addNotification("Your close friend " + IControlCenter.userRoster[uid].getUsername() + " has worked as: " + jobStrList)
		if eduhistory != None:
			oldeduhistory = list(x for x in targetUser.getEducationHistory() if x != '')
			targetUser.setEducationHistory(eduhistory)
			eduList = targetUser.getEducationHistory()
			if eduList == list():
				eduStrList = "I haven't listed any schools yet."
			else:
				sep = "; "
				eduStrList = "I've studied in the following schools: " + sep.join(eduList) + "."
			if eduList != oldeduhistory:
				targetUser.addStatus(Status(poster = uid, text = "Word Up! I just edited my Education History. " + eduStrList))
				for x in toBeNotified:
					x.addNotification("Your close friend " + IControlCenter.userRoster[uid].getUsername() + " has studied as: " + eduStrList)

		if username != oldusername: ## If username must be changed, edit folder name as well
			##rename the folder of this user's settings
			os.rename("users/" + oldusername + "/", "users/" + username + "/")
			## edit this user's login credentials
			## update config database filename
			updatedConfigDB = UserConfigDatabase(filename = "users/" + username + "/info.txt")
			targetUser.editConfigDB(updatedConfigDB)
			targetUser.setUsername(username)
			IControlCenter.userRoster[uid].resetProfilePic()
			targetUser.addStatus(Status(poster = uid, text = "Notice me! I just changed my username to '" + targetUser.getUsername() + "'." ))
			for x in toBeNotified:
				x.addNotification("Your close friend " + oldusername + " is now called " + IControlCenter.userRoster[uid].getUsername())

		if profilepic != None and profilepic != "":
			## copy profile picture into folder
			sourcepath = profilepic
			targetpath = "users/" + IControlCenter.userRoster[uid].getUsername() + "/profile.gif"
			copy(sourcepath, targetpath)
			IControlCenter.userRoster[uid].resetProfilePic()
			targetUser.addStatus(Status(poster = uid, text = "See how amazing I look? I just changed my profile picture!" ))
			for x in toBeNotified:
				x.addNotification("Your close friend " + IControlCenter.userRoster[uid].getUsername() + " has a new profile picture.")

		self.setSelected(uid)

		return "SUCCESS"

	def sendMessageByConversation(self, senderID, conversationObject, text):
		conversationObject.newMessage(senderID, text)
		## send a notification to the other members
		senderName = IControlCenter.userRoster[senderID].getUsername()
		for uid in conversationObject.getMembers():
			if uid != senderID:
				IControlCenter.userRoster[uid].addNotification("Heads up: " + senderName + " just sent a new message in one of your conversations. Open up your conversations window to see.")

	def addFriendshipById(self, uid, friendID):
		## add friendship to sender ('Requested' must be approved)
		IControlCenter.userRoster[uid].addFriendship(Friendship(userid = friendID, status = "Requested"))
		## add friendship to sendee ('Pending' can approve 'Requested')
		IControlCenter.userRoster[friendID].addFriendship(Friendship(userid = uid, status = "Pending"))
		## send a notification to the requested user
		IControlCenter.userRoster[friendID].addNotification("You should check out your friends list. " + IControlCenter.userRoster[uid].getUsername() + " just sent you a friend request.")

	def unfriendById(self, uid1, uid2):
		IControlCenter.userRoster[uid1].unfriendById(uid2)
		IControlCenter.userRoster[uid2].unfriendById(uid1)
		IControlCenter.userRoster[uid1].addNotification("You and " + IControlCenter.userRoster[uid2].getUsername() + " are no longer friends.")
		IControlCenter.userRoster[uid2].addNotification("You and " + IControlCenter.userRoster[uid1].getUsername() + " are no longer friends.")

	def addStatusById(self, uid, text):
		## This function will also parse tags made inside the text of the status

		asterSep = text.split('*')
		blanksep = ""
		text = blanksep.join(asterSep)
		taggedIDs = list()
		for i in range(len(asterSep)):
			try:
				detectedID = self.getUserByName(asterSep[i]).getUserID()
				taggedIDs.append(detectedID)
				IControlCenter.userRoster[detectedID].addNotification("You were tagged in a status posted by " + IControlCenter.userRoster[uid].getUsername() + ": '" + text + "'.")
			except:
				continue

		## send notification to users who have marked this user as their close friend
		for friendship in IControlCenter.userRoster[uid].getFriends():
			if uid in list(f.getFriendID() for f in IControlCenter.userRoster[friendship.getFriendID()].getFriends() if f.getStatus() == "Close Friend"):
				IControlCenter.userRoster[friendship.getFriendID()].addNotification(IControlCenter.userRoster[uid].getUsername() + "--whom you marked as a Close Friend posted a status: '" + text + "'.")

		IControlCenter.userRoster[uid].addStatus(Status(text = text, poster = uid, tags = taggedIDs))

	## 'members' must be an iterable object (lsit/tuple) contaning User IDs
	def addConversationById(self, members):
		newConversationObject = Conversation(members)
		for x in members:
			self.getUserById(x).addConversation(newConversationObject)
		IControlCenter.conversationRoster.append(newConversationObject)

	def aggregateNewsfeedById(self, uid):
		n = IControlCenter.newsfeedAggregator.aggregate(IControlCenter.userRoster[uid], self)
		IControlCenter.userRoster[uid].setNewsfeed(n)

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
			IControlCenter.database.clearDict()
			ActiveUser.activeUsers = list()
			uidCount = 0
			for userprofile in IControlCenter.userRoster:
				if userprofile.getUserID() in IControlCenter.usersToDelete:
					continue
				if userprofile.isLoggedIn():
					ActiveUser.activeUsers.append(uidCount)
				uidCount += 1
				## update config Database
				userprofile.getConfigDB().editEntryByID('gender', newvalue = userprofile.getGender()[0])
				userprofile.getConfigDB().editEntryByID('bday', newvalue = userprofile.getBdayDict())
				userprofile.getConfigDB().editEntryByID('jobs', newvalue = userprofile.getJobHistory())
				userprofile.getConfigDB().editEntryByID('education', newvalue = userprofile.getEducationHistory())
				userprofile.getConfigDB().editEntryByID('notifs', newvalue = list(x.getDescription() for x in userprofile.getNotifications() if x.isRead() == False))
				userprofile.getConfigDB().exportDB()
				## update friends
				## first, build list of a formatted friends
				friendslist = list()
				for friendX in userprofile.getFriends():
					if friendX.getFriendID() in IControlCenter.usersToDelete:
						continue
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
					try:
						thingToAppend.append(self.getUserById(friendX.getFriendID()).getUsername())
					except:
						continue
					blanksep = ""
					friendslist.append(blanksep.join(thingToAppend))
				IControlCenter.database.insert(username = userprofile.getUsername(), password = userprofile.getPassword(), friends = friendslist)
			IControlCenter.database.exportDB()
			## reset conversations database and export conversations
			IControlCenter.database_conversations.clearDict()
			for conversation in IControlCenter.conversationRoster:
				memberslist = list()
				for m in conversation.getMembers():
					if m not in IControlCenter.usersToDelete:
						memberslist.append(IControlCenter.userRoster[m].getUsername())
				msglist = list(self.getUserById(x.getSender()).getUsername() + ": " + x.getText() for x in conversation.getMessages())
				if memberslist != list():
					IControlCenter.database_conversations.insert(members = memberslist, messages = msglist)
			IControlCenter.database_conversations.exportDB()
			## build a list of Status objects, then insert into database
			statusRoster = list()
			for user in IControlCenter.userRoster:
				if user.getUserID() in IControlCenter.usersToDelete:
					continue
				for status in user.getStatuses():
					statusRoster.append(status)
			## reset status database and export statuses
			IControlCenter.database_feed.clearDict()
			## only export the latest 10,000 statuses
			## so the file won't get too large; and to prevent the system
			## from slowing down
			exportedStatusCount = 0
			for s in reversed(statusRoster): ## so the latest will be on top of the file
				if exportedStatusCount == 10000:
					break
				try:
					IControlCenter.database_feed.insert(poster = self.getUserById(s.getPoster()).getUsername(), timestamp = str(s.getRawTime()), text = s.getText(), attachments = s.getAttachments(), tags = list(self.getUserById(k).getUsername() for k in s.getTags()), comments = list(dict(commentator = self.getUserById(c.getPoster()).getUsername(), text = c.getText()) for c in s.getComments()), up = list(self.getUserById(k).getUsername() for k in s.getThumbsUps()), down = list(self.getUserById(k).getUsername() for k in s.getThumbsDowns()))
					exportedStatusCount += 1
				except:
					continue
			IControlCenter.database_feed.exportDB()
			IControlCenter.usersToDelete = list()

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
				self.setSelected(user.getUserID())
				return "SUCCESS"
			else:
				return "Login Failed. The username and/or password was incorrect.\nTry again."
		else:
			return "Login Failed. There is currently no user with that name.\nTry again."

	## 'user' argument must be a UserProxy object
	def logoutUser(self, uid):
		self.getUserById(uid).logout()

	def deleteUserById(self, uid):
		## FIRST AND FOREMOST: IDENTIFY USER!
		try:
			target = IControlCenter.userRoster[uid]
		except IndexError:
			return "Could not find any user with ID '" + str(uid) + "'."
		except ValueError:
			return "Invalid Argument to deleteUserById(...) function. The argument must be an integer"
		except:
			return "Could not find the user you were looking for."

		## unfriend with everyone;
		for friend in target.getFriends():
			self.unfriendById(friend.getFriendID(), uid)
		## delete all messages and exit all conversations
		## delte conversations if necessary
		for user in IControlCenter.userRoster:
			for conv in user.getConversations():
				for msg in conv.getMessages():
					if msg.getSender() == uid:
						conv.deleteMessageByValue(msg)
		## delete comments, tags, thumbs ups and downs
		for user in IControlCenter.userRoster:
			for status in user.getStatuses():
				try:
					status.getThumbsDowns().remove(uid)
				except:
					pass
				try:
					status.getThumbsUps().remove(uid)
				except:
					pass
				try:
					status.getTags().remove(uid)
				except:
					pass
				for comment in status.getComments():
					if comment.getPoster() == uid:
						status.deleteCommentByValue(comment)
		target.setNewsfeed(list())
		target.setStatuses(list())
		## delete folder
		targetFolder = "users/" + target.getUsername() + "/"
		if os.path.exists(targetFolder):
			try:
				rmtree(targetFolder)
			except:
				return "Could not delete the user's folder."
		## remove from userRoster
		self.logoutUser(uid)
		IControlCenter.usersToDelete.append(uid)
		self.saveDB()
		opresp = self.openDB(self.dbfilename, self.db_convfilename, self.db_feedfilename)
		if opresp != "SUCCESS":
			return opresp
		self.setSelected(IControlCenter.userRoster[-1].getUserID())
		return "SUCCESS"