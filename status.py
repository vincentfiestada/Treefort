from time import time, ctime, mktime
from datetime import datetime, timedelta
from math import log

EPOCH = datetime(2009, 7, 23)

class Comment:
	def __init__(self, poster, text):
		## newlines are not allowed in comments since they mess up the tag_config in the Text Box
		self.text = text.lstrip().rstrip().replace("\t","<tb>").replace("\n","").replace("<br>","").replace(":","<col>").replace("|","<bar>")
		self.poster = poster

	def getText(self):
		return self.text

	def getFText(self):
		return self.text.replace("<tb>","\t").replace("<col>",":").replace("<bar>","|")

	def getPoster(self):
		return self.poster

class Status:
	## 'poster' argument must be the User ID of the user who posted this status
	def __init__(self, text, poster, timestamp = None, attachments = [], up = [], down = [], comments = []):
		## some characters are changed to '?escape codes?' and can be retrieved in their original form using getFtext()
		## applies to comments as well
		self.text = text.lstrip().rstrip().replace("\t","<tb>").replace("\n","<br>").replace(":","<col>").replace("|","<bar>")
		self.poster = poster
		self.attachments = attachments
		if timestamp == None:
			self.time = time()
		else:
			self.time = timestamp
		self.ctime = ctime(self.time)
		self.comments = comments ## A list of comment objects
		self.thumbsups = up ## A list of user ids
		self.thumbsdowns = down ## list of user ids
		self.rank = 0.0
		## the following details will be used to determine if the rank needs to be updated
		self.rankLastUpdate = (0.0, len(self.thumbsups), len(self.thumbsdowns))

	def getFText(self):
		return self.text.replace("<tb>","\t").replace("<br>","\n").replace("<col>",":").replace("<bar>","|")

	def getText(self):
		return self.text

	def getPoster(self):
		return self.poster

	def getComments(self):
		return self.comments

	## 'commentodelete' argument must be a Comment object in self.comments
	def deleteCommentByValue(self, commentodelete):
		self.comments.remove(commentodelete)

	def getAttachments(self):
		return self.attachments

	def getThumbsUps(self):
		return self.thumbsups
	
	def getThumbsDowns(self):
		return self.thumbsdowns

	def getRawTime(self):
		return self.time

	def getTime(self):
		return self.ctime
	
	def getRank(self):
		## Computing the rank every time is expensive;
		## use three values:
		## --- Thumbs Ups count differed
		## --- Thumbs Downs count differed
		## --- time difference between last rank update is greater than 24 Hrs

		currentSecs = time()
		if self.rankLastUpdate[1] == len(self.thumbsups) and self.rankLastUpdate[2] == len(self.thumbsdowns) and currentSecs - self.time < 86400:
			return self.rank

		## Ranking algorithm is based on Reddit's ranking system, as described by:
		## Amir Salihefendic on (www.amix.dk/blog/post/19588) Original concept (c) Reddit and Randall Munroe
		today = datetime.fromtimestamp(currentSecs)
		timediff = today - EPOCH
		epoch_seconds = timediff.days * 86400 + timediff.seconds + (float(timediff.microseconds) / 1000000)
		thumbsupscount = len(self.thumbsups)
		thumbsdowncount = len(self.thumbsdowns)
		score = thumbsupscount - thumbsdowncount
		order = log(max(abs(score), 1), 10)
		sign = 1 if score > 0 else -1 if score < 0 else 0
		self.rankLastUpdate = (currentSecs, thumbsupscount, thumbsdowncount)
		self.rank = round(order + sign * epoch_seconds / 45000, 7)
		return self.rank
	
	def comment(self, uid, text):
		self.comments.append(Comment(uid, text))

	def giveThumbsUp(self, uid):
		if uid not in self.thumbsups:
			self.thumbsups.append(uid)
			if uid in self.thumbsdowns:
				self.thumbsdowns.remove(uid)

	def giveThumbsDown(self, uid):
		if uid not in self.thumbsdowns:
			self.thumbsdowns.append(uid)
			if uid in self.thumbsups:
				self.thumbsups.remove(uid)

class NewsFeed:
	## 'statuses' argument must be a list of Status objects
	def __init__(self, statuses):
		self.statuses = statuses
		self.current = 0

	def getStatuses(self):
		return self.statuses

	def setStatuses(self, statuses):
		self.statuses = statuses

	def getCurrent(self):
		return self.statuses[self.current]

	def setCurrent(self, index):
		self.current = index

	def getCurrentIndex(self):
		return self.current

class FriendsStrategy:
	def aggregate(self, user, linkedCC):
		raise NotImplementedError

class FewFriendsStrategy(FriendsStrategy):
	def aggregate(self, user, linkedCC):
		currentSecs = time()
		friendIDs = list(f.getFriendID() for f in user.getFriends() if f.getStatus() != "Hidden Updates" and f.getStatus() != "Blocked" and f.getStatus() != "Requested" and f.getStatus() != "Pending")
		friendIDs.append(user.getUserID())
		newsfeed = list()
		for friend in friendIDs:
			friendStats = linkedCC.getUserById(friend).getStatuses()
			for status in list(s for s in friendStats if currentSecs - s.getRawTime() < 2592000):
				newsfeed.append(status)
		return sorted(newsfeed, key = Status.getRawTime, reverse = True)


## The ManyFriendsStrategy is based on the Ranking system of Reddit by Randall Munroe
class ManyFriendsStrategy(FriendsStrategy):
	def aggregate(self, user, linkedCC):
		currentSecs = time()
		newsfeed = list()
		friendIDs = list(f.getFriendID() for f in user.getFriends() if f.getStatus() != "Hidden Updates" and f.getStatus() != "Blocked" and f.getStatus() != "Requested" and f.getStatus() != "Pending")
		friendIDs.append(user.getUserID())
		for friend in friendIDs:
			friendStats = linkedCC.getUserById(friend).getStatuses()
			for status in list(s for s in friendStats if currentSecs - s.getRawTime() < 2592000):
				newsfeed.append(status)
		return sorted(newsfeed, key = Status.getRank, reverse = True)

class NewsFeedAggregator: ## StrategyInContext class
	## 'user' must be a User Object reference and 'linkedCC' a ControlCenter obj ref
	def aggregate(self, user, linkedCC):
		if len(user.getFriends()) < 10:
			strategy = FewFriendsStrategy()
		else:
			strategy = ManyFriendsStrategy()
		return strategy.aggregate(user, linkedCC)