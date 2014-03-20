class Message:
	def __init__(self, sender, text = ""):
		self.sender = sender
		self.text = text.replace("\n","").replace("\t","").replace(":","").replace("|","").lstrip().rstrip()

	def getSender(self):
		return self.sender
	
	def getText(self):
		return self.text

class Conversation:
	## members should be a list of user IDs
	def __init__(self, members):
		self.members = members
		self.messages = list()
	def getMembers(self):
		return self.members
	def getMessages(self):
		return self.messages
	def getMessageByIndex(self, index):
		return self.messages[index]
	def deleteMessageByIndex(self, index):
		self.messages.pop(index)
	## messagetodelete argument must be a Message object
	def deleteMessageByValue(self, messagetodelete):
		self.messages.remove(messagetodelete)
	## 'sender' argument must be a UserID
	def newMessage(self, sender, text):
		self.messages.append(Message(sender, text))
	def join(self, uid):
		if uid not in self.members:
			self.members.append(uid)
	def disjoin(self, uid):
		try:
			self.members.remove(uid)
		except:
			return