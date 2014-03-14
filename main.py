from Tkinter import *
from ttk import Frame, Combobox
from controlcenter import *
import tkMessageBox, tkFileDialog

from userproxy import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 600
DATABASE_FILENAME = "db.txt"
DATABASE_CONV_FILENAME ="db_conv.txt"
DATABASE_FEED_FILENAME = "db_feed.txt"
PROGRAM_VERSION = "0.8.2 Alpha"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

font0 = ("Helvetica", 9, "bold")
font1 = ("Helvetica", 11, "bold")
font2 = ("Helvetica", 11)
font21 = ("Courier New", 11)
font3 = ("Helvetica", 14, "bold")
font4 = ("Helvetica", 9)
font5 = ("Verdana", 11)

cc = IControlCenter()

resp = cc.openDB(DATABASE_FILENAME, DATABASE_CONV_FILENAME, DATABASE_FEED_FILENAME)
if resp != "SUCCESS":
	tkMessageBox.showerror("Error Opening Databases",resp)
	quit()

mainWindow = Tk()
mainWindow.title("Tree Fort")
mainWindow.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
windowPanes = PanedWindow(mainWindow)
windowPanes.pack(fill=BOTH, expand=True)
adminFrame = Frame(windowPanes, relief=FLAT)
userFrame = Frame(windowPanes, relief=FLAT)
windowPanes.add(adminFrame, width=WINDOW_WIDTH*0.2)
windowPanes.add(userFrame, width=WINDOW_WIDTH*0.8)

def menu_showinfobox():
	aboutwin = AboutWindow()
	del aboutwin

def month_num_of_days(month,year):
	if month in (0,2,4,6,7,9,11):
		return 31
	elif month == 1:
		if(year%400==0):
			return 29
		if(year%100==0):
			return 28
		if(year%4==0):
			return 29
		return 28
	else:
		return 30

def newUser(info):
	## convert month to str number
	NumericMonth = str(MONTHS.index(info['bday']['month'].get()) + 1)
	## build birthday dict
	bdayDict = dict(month = NumericMonth, day = info['bday']['day'].get(), year = info['bday']['year'].get())
	return cc.newUser(username = info['username'].get(), password = info['password'].get(), gender = info[
		'gender'].get(), bday = bdayDict)

def logInOut():
	loginoutwin = LoginWindow(cc.getSelected(), cc, updateAwesomesauceControls)
	del loginoutwin

class SignUpWindow: ##This one isn't a singleton. More than one can be opened at any time
	## preload images, so they can be shared by multiple windows
	idcardIcon = PhotoImage(file = "img/idcard.gif")
	unameIcon = PhotoImage(file = "img/user_login.gif")
	keyIcon = PhotoImage(file = "img/key.gif")
	maleIcon = PhotoImage(file = "img/male.gif")
	femaleIcon = PhotoImage(file = "img/female.gif")
	calendarIcon = PhotoImage(file = "img/calendar.gif")
	## 'savecommand' should be a method
	def __init__(self, master, title, savecommand, savecommand2 = None):
		self.master = master
		self.savecommand = savecommand
		self.savecommand2 = savecommand2
		self.box = Toplevel(self.master, padx = 14, pady = 14)
		self.box.title(title)
		self.box.minsize(500,300)
		self.box.maxsize(500,300)
		self.info = dict()

		self.frame1 = Frame(self.box)
		self.frame1.pack(side = TOP, fill = X)
		self.frame2 = Frame(self.box)
		self.frame2.pack(side = TOP, fill = X)
		self.frame3 = Frame(self.box)
		self.frame3.pack(side = TOP, fill = X)
		self.frame35 = Frame(self.box)
		self.frame35.pack(side = TOP, fill = X)
		self.frame4 = Frame(self.box)
		self.frame4.pack(side = TOP, fill = X)
		self.frame5 = Frame(self.box)
		self.frame5.pack(side = TOP, fill = X)
		self.frame6 = Frame(self.box)
		self.frame6.pack(side = BOTTOM, fill = X)
		self.signUpImg = Label(self.frame1, image = SignUpWindow.idcardIcon)
		self.signUpImg.pack(side = LEFT)
		self.signUpTitle = Label(self.frame1, text = "Sign Up", font = font3, fg = "#0094FF")
		self.signUpTitle.pack(side = LEFT)
		self.usernameImg = Label(self.frame2, image = SignUpWindow.unameIcon)
		self.usernameImg.pack(side = LEFT)
		self.usernameLabel = Label(self.frame2, text = "Username: ", font = font1)
		self.usernameLabel.pack(side = LEFT)
		self.info['username'] = StringVar()
		self.usernameEntry = Entry(self.frame2, font = font2, width = 32, textvariable = self.info['username'], relief = GROOVE)
		self.usernameEntry.pack(side = LEFT, fill = X, expand = True)
		self.passwordImg = Label(self.frame3, image = SignUpWindow.keyIcon)
		self.passwordImg.pack(side = LEFT)
		self.passwordLabel = Label(self.frame3, text = "Password: ", font = font1)
		self.passwordLabel.pack(side = LEFT)
		self.info['password'] = StringVar()
		self.passwordEntry = Entry(self.frame3, font = font2, width = 32, textvariable = self.info['password'], show = '*', relief = GROOVE)
		self.passwordEntry.pack(side = LEFT, fill = X, expand = True)
		self.passwordLabel2 = Label(self.frame35, text = "Retype Password: ", font = font1)
		self.passwordLabel2.pack(side = LEFT)
		self.info['password-2'] = StringVar()
		self.passwordEntry2 = Entry(self.frame35, font = font2, width = 32, textvariable = self.info['password-2'], show = '*', relief = GROOVE)
		self.passwordEntry2.pack(side = LEFT, fill = X, expand = True)
		self.info['gender'] = StringVar()
		self.info['gender'].set("M")
		self.genderLabel = Label(self.frame4, text = "Gender: ", font = font1)
		self.genderLabel.pack(side = LEFT)
		self.radioM = Radiobutton(self.frame4, font = font2, value = "M", variable = self.info['gender'], text = "Male")
		self.radioM.pack(side = LEFT)
		self.maleImg = Label(self.frame4, image = SignUpWindow.maleIcon)
		self.maleImg.pack(side = LEFT)
		self.radioF = Radiobutton(self.frame4, font = font2, value = "F", variable = self.info['gender'], text = "Female")
		self.radioF.pack(side = LEFT)
		self.femaleImg = Label(self.frame4, image = SignUpWindow.femaleIcon)
		self.femaleImg.pack(side = LEFT)
		self.bdayImg = Label(self.frame5, image = SignUpWindow.calendarIcon)
		self.bdayImg.pack(side = LEFT)
		self.bdayLabel = Label(self.frame5, text = "Birthday: ", font = font1)
		self.bdayLabel.pack(side = LEFT)
		self.info['bday'] = dict()
		self.info['bday']['month'] = StringVar()
		self.bdaymonthSpinner = Spinbox(self.frame5, values = MONTHS, font = font2, textvariable = self.info['bday']['month'], width=10, wrap = True, relief = GROOVE)
		self.bdaymonthSpinner.pack(side = LEFT)
		self.info['bday']['day'] = StringVar()
		self.bdaydaySpinner = Spinbox(self.frame5, from_ = 1, to=31, font = font2, textvariable = self.info['bday']['day'], width=2, wrap = True, relief = GROOVE)
		self.bdaydaySpinner.pack(side = LEFT)
		self.info['bday']['year'] = StringVar()
		## make use of tm_year, imported by the user.py file
		currentDate = localtime()
		self.bdayyearSpinner = Spinbox(self.frame5, from_ = currentDate.tm_year-150, to=currentDate.tm_year, font = font2, textvariable = self.info['bday']['year'], width=4, relief = GROOVE)
		self.bdayyearSpinner.pack(side = LEFT)
		self.info['bday']['year'].set(str(currentDate.tm_year))
		self.info['bday']['month'].set(MONTHS[currentDate.tm_mon-1])
		self.info['bday']['day'].set(str(currentDate.tm_mday))
		submitButton = Button(self.frame6, text = "Submit", fg = "#ffffff", activeforeground = "#ffffff", bg = "dark green", activebackground = "dark green", font = font1, command = self.submit, relief = GROOVE)
		cancelButton = Button(self.frame6, text = "Cancel", fg = "#ffffff", activeforeground = "#ffffff", bg = "dark red", activebackground = "dark red", font = font1, command = self.cancel, relief = GROOVE)
		cancelButton.pack(side = RIGHT)
		submitButton.pack(side = RIGHT)
		
		self.box.bind("<Return>", self.submit)

	def cancel(self):
		self.box.destroy()

	def submit(self, event = None):
		try:
			## check if password entries match
			if self.info['password'].get() != self.info['password-2'].get():
				tkMessageBox.showerror("Sign up Failed", "The passwords you entered don't match")
				self.info['password'].set("")
				self.info['password-2'].set("")
				self.box.deiconify()
				return
			currentDate = localtime()
			## fix birthdate: the year can't be > current year or < 0
			if int(self.info['bday']['year'].get()) > currentDate.tm_year:
				tkMessageBox.showerror("Sign up Failed", "Your birth year cannot be set in the future. (You entered "+self.info['bday']['year'].get()+")")
				self.info['bday']['year'].set(str(currentDate.tm_year))
				self.box.deiconify()
				return
			elif int(self.info['bday']['year'].get()) < 0:
				tkMessageBox.showerror("Sign up Failed", "Your birth year cannot be negative. (You entered "+self.info['bday']['year'].get()+")")
				self.info['bday']['year'].set("1996")
				self.box.deiconify()
				return
			## Fix bday formatting:
			## month must not be empty
			## convert month to proper format
			monthStr = self.info['bday']['month'].get().lower()
			monthStr = monthStr[0].upper() + monthStr[1:]
			## check if monthStr is a month's name
			if monthStr not in MONTHS:
				tkMessageBox.showerror("Sign up Failed", "Enter the name of a month")
				self.box.deiconify()
				return
			self.info['bday']['month'].set(monthStr)
			## check if day is in range of month
			if int(self.info['bday']['day'].get()) not in range(1, month_num_of_days(month = MONTHS.index(self.info['bday']['month'].get())+1, year = int(self.info['bday']['year'].get()))+1):
				self.info['bday']['day'].set("1")

			returned = self.savecommand(self.info)
			if returned == "SUCCESS":
				self.box.destroy()
			else:
				tkMessageBox.showerror("Sign up Failed", "Oops! We couldn't sign you up successfully.\nHere's the problem:\n" + returned)
				self.box.deiconify()
				return
			if self.savecommand2 != None:
				self.savecommand2()
				return
		except ValueError:
			tkMessageBox.showerror("Error", "You entered some non-numeric characters where only numbers are allowed.")
			self.box.deiconify()
			return
		except:
			tkMessageBox.showerror("Error", "An error occured. We cannot create a new user account at this moment.")
			self.box.deiconify()
			return

class AboutWindow:
	aboutBox = Toplevel(mainWindow, padx = 14, pady = 14)
	aboutBox.title("About Tree Fort")
	aboutBox.maxsize(500,330)
	aboutBox.minsize(500,330)
	LogoImg = PhotoImage(file = "img/logo_transparent.gif")
	LogoLabel = Label(aboutBox, image = LogoImg)
	LogoLabel.pack(side=TOP,fill=X)
	ProgramInfoFrame = LabelFrame(aboutBox, text="Program Info", padx = 7, pady = 7)
	ProgramInfoFrame.pack(side=TOP,fill=X)
	ProgramInfoLabel1 = Label(ProgramInfoFrame, text="Program Name: Tree Fort\n\nVersion: "+PROGRAM_VERSION)
	ProgramInfoLabel1.pack(side=LEFT, expand = True)
	ProgramCreditsFrame = LabelFrame(aboutBox, text="Credits", padx = 7, pady = 7)
	ProgramCreditsFrame.pack(side=TOP,fill=X)
	ProgramCreditsLabel1 = Label(ProgramCreditsFrame, text="Copyright 2014 Vincent Paul Fiestada\nvffiestada@upd.edu.ph\n\nIcons by Joseph Wain\nglyphish.com")
	ProgramCreditsLabel1.pack(side=LEFT, expand = True)
	aboutBox.withdraw()
	aboutBox.protocol("WM_DELETE_WINDOW", aboutBox.withdraw)

	def __init__(self):
	 	AboutWindow.aboutBox.deiconify()

class LoginWindow: ## A singleton Window class
	loginwindow = Toplevel(mainWindow, padx = 14, pady = 14)
	loginwindow.title("Log in")
	loginwindow.maxsize(310,110)
	loginwindow.minsize(310,110)
	loginusername = StringVar()
	loginpassword = StringVar()

	## MESSY UI STUFF! I HATE YOU TKINTER!
	loginIcon = PhotoImage(file = "img/user_login.gif")
	keyIcon = PhotoImage(file = "img/key.gif")

	loginWidgetFrame1 = Frame(loginwindow)
	loginWidgetFrame1.pack(side = TOP, fill = X)
	loginWidgetFrame2 = Frame(loginwindow)
	loginWidgetFrame2.pack(side = TOP, fill = X)
	loginWidgetFrame3 = Frame(loginwindow)
	loginWidgetFrame3.pack(side = TOP, fill = X)
	loginUsernameLabelImg = Label(loginWidgetFrame1, image = loginIcon)
	loginUsernameLabelImg.pack(side = LEFT)
	loginUsernameLabelTxt = Label(loginWidgetFrame1, text = "Username: ", font=font1)
	loginUsernameLabelTxt.pack(side = LEFT)
	loginUsernameBox = Entry(loginWidgetFrame1, font=font2, textvariable = loginusername, relief = GROOVE)
	loginUsernameBox.pack(side = LEFT, expand = True)
	loginPasswordLabelImg = Label(loginWidgetFrame2, image = keyIcon)
	loginPasswordLabelImg.pack(side = LEFT)
	loginPasswordLabelTxt = Label(loginWidgetFrame2, text = "    Password: ", font=font1)
	loginPasswordLabelTxt.pack(side = LEFT)
	loginPasswordBox = Entry(loginWidgetFrame2, font=font2, show = '*', textvariable = loginpassword, relief = GROOVE)
	loginPasswordBox.pack(side = LEFT, expand = True)
	loginSubmitCredButton = Button(loginWidgetFrame3, text = "Submit", font=font1, bg = "dark green", fg = "#ffffff", activebackground = "dark green", activeforeground = "#ffffff", relief = GROOVE)
	loginCancelButton = Button(loginWidgetFrame3, text = "Cancel", font=font1, bg = "dark red", fg = "#ffffff", activebackground = "dark red", activeforeground = "#ffffff", command = loginwindow.withdraw, relief = GROOVE)
	loginCancelButton.pack(side = RIGHT)
	loginSubmitCredButton.pack(side = RIGHT)
	loginwindow.withdraw()
	loginwindow.protocol("WM_DELETE_WINDOW", loginwindow.withdraw)
	## 'controlcenter' argument must be a Control Center object
	def __init__(self, selectedUser, controlcenter, postcommand = None):		
		self.linkedCC = controlcenter
		self.selectedUser = selectedUser
		self.postcommand = postcommand
		if self.selectedUser == None:
			def_input_username = ""
		else:
			def_input_username = self.selectedUser.getUsername()

		if self.selectedUser == None or self.selectedUser.isLoggedIn() == False:
			if def_input_username != LoginWindow.loginusername.get():
				LoginWindow.loginpassword.set("")
			LoginWindow.loginusername.set(def_input_username)

			LoginWindow.loginSubmitCredButton.bind("<ButtonRelease-1>", self.submit)
			LoginWindow.loginwindow.bind("<Return>", self.submit)

			LoginWindow.loginwindow.deiconify()
			LoginWindow.loginwindow.mainloop()
		else:
			if selectedUser != None:
				self.linkedCC.logoutUser(self.selectedUser.getUserID())
				LoginWindow.loginwindow.withdraw()
				self.postcommand()
			else:
				tkMessageBox.showinfo("Log out Failed", "No user is selected.")

	def submit(self, event):
		LoginWindow.loginwindow.withdraw()
		resp = self.linkedCC.loginUser(LoginWindow.loginusername.get(), LoginWindow.loginpassword.get())
		if resp == "SUCCESS":
			if self.postcommand != None:
				self.postcommand()
		else:
			tkMessageBox.showinfo("Login Failed", resp)
		return

class ConversationWindow:
	messageIcon = PhotoImage(file = "img/message.gif")
	box = Toplevel(mainWindow, padx = 14, pady = 14)
	box.title("Conversations")
	box.minsize(700,500)
	box.maxsize(700,500)
	frame0 = Frame(box)
	frame0.pack(side = TOP, fill = X)
	frame1 = Frame(box)
	frame1.pack(side = TOP, fill = BOTH, expand = True)
	icon = Label(frame0, image = messageIcon)
	icon.pack(side = LEFT)
	title = Label(frame0, text = "Conversations", font = font3, fg = "#2F54FF")
	title.pack(side = LEFT)
	panes = PanedWindow(frame1)
	panes.pack(side = TOP, fill = BOTH, expand = True)
	conversationListPane = Frame(panes, relief = FLAT)
	conversationDetailsPane = PanedWindow(panes, relief = FLAT)
	newConversationButton = Button(conversationListPane, text = "New Conversation", font = font2, bg = "#2F54FF", activebackground = "#2F54FF", fg = "#ffffff", activeforeground = "#ffffff", relief = GROOVE)
	newConversationButton.pack(side = TOP, fill = X)
	panes.add(conversationListPane, width = (700-28)*0.3)
	panes.add(conversationDetailsPane, width = (700-28)*0.7)
	conversationsListScrollBar = Scrollbar(conversationListPane)
	conversationsListScrollBar.pack(side = RIGHT, fill = Y)
	conversationsListBox = Listbox(conversationListPane, font = font2, yscrollcommand = conversationsListScrollBar.set, selectmode = SINGLE)
	conversationsListBox.pack(side = LEFT, fill = BOTH, expand = True)
	conversationsListScrollBar.config(command = conversationsListBox.yview)
	messagesControlFrame = Frame(conversationDetailsPane)
	messagesControlFrame.pack(side = TOP, fill = X)
	messagesControlFrame_subframe1 = Frame(messagesControlFrame)
	messagesControlFrame_subframe1.pack(side = TOP, fill = X)
	messagesControlFrame_subframe2 = Frame(messagesControlFrame)
	messagesControlFrame_subframe2.pack(side = BOTTOM, fill = X)
	conversationsControlFrame = Frame(conversationDetailsPane)
	conversationsControlFrame.pack(side = BOTTOM, fill = X)
	newMessageText = StringVar()
	newMessageLabel = Label(messagesControlFrame_subframe1, text = "New Message: ", font = font0, fg = "#FF596E")
	newMessageLabel.pack(side = LEFT)
	newMessageBox = Entry(messagesControlFrame_subframe1, font = font5, textvariable = newMessageText)
	newMessageBox.pack(side = LEFT, fill = X, expand = True)
	sendMessageButton = Button(messagesControlFrame_subframe2, text = "Send", font = font2, relief = GROOVE)
	sendMessageButton.pack(side = RIGHT)
	exitConversationButton = Button(conversationsControlFrame, text = "Exit Conversation", font = font2, fg = "#D30C2A", activeforeground = "#D30C2A", relief = GROOVE)
	exitConversationButton.pack(side = LEFT)
	deleteMessagesButton = Button(conversationsControlFrame, text = "Delete Messages", font = font2, fg = "#D30C2A", activeforeground = "#D30C2A", relief = GROOVE)
	deleteMessagesButton.pack(side = LEFT)
	inviteFriendButton = Button(conversationsControlFrame, text = "Invite Friend", font = font2, fg = "#1C3DB6", activeforeground = "#1C3DB6", relief = GROOVE)
	inviteFriendButton.pack(side = LEFT)

	messagesDisplayFrame = Frame(conversationDetailsPane)
	messagesDisplayFrame.pack(side = BOTTOM, fill = X)
	messagesScrollBar = Scrollbar(messagesDisplayFrame)
	messagesScrollBar.pack(side = RIGHT, fill = Y)
	messagesDisplay = Text(messagesDisplayFrame, bg="#ffffff", yscrollcommand = messagesScrollBar.set, state = DISABLED, font = font5, wrap = WORD)
	messagesDisplay.pack(side = TOP, fill = X)
	messagesScrollBar.config(command = messagesDisplay.yview)

	newConversationBox = Toplevel(box, padx = 10, pady = 10)
	newConversationBox.title("New Conversation")
	newConversationBox.minsize(300,300)
	newConversationBox.maxsize(300,300)
	newConversationBox.withdraw()
	newConversationBoxTitle = Label(newConversationBox, text = "Select Friends: ", font = font1, fg = "#2F54FF")
	newConversationBoxTitle.pack(side = TOP)
	newConversationBoxSubFrame = Frame(newConversationBox)
	newConversationBoxSubFrame.pack(side = TOP, fill = X)
	newConversationMembersScrollBar = Scrollbar(newConversationBoxSubFrame)
	newConversationMembersScrollBar.pack(side = RIGHT, fill = Y)
	newConversationMembersListBox = Listbox(newConversationBoxSubFrame, font = font2, selectmode = MULTIPLE, yscrollcommand = newConversationMembersScrollBar.set)
	newConversationMembersListBox.pack(side = TOP, fill = BOTH, expand = True)
	newConversationMembersScrollBar.config(command = newConversationMembersListBox.yview)
	newConversationMembersListBox.insert(END, "No friends")
	newConversationBoxSubmitButton = Button(newConversationBox, text = "Invite Friends", fg = "white", activeforeground = "white", bg = "dark green", activebackground = "dark green", font = font2, relief = GROOVE)
	newConversationBoxSubmitButton.pack(side = RIGHT, fill = X)

	deleteMessagesBox = Toplevel(box, padx = 10, pady = 10)
	deleteMessagesBox.title("Delete Messages")
	deleteMessagesBox.minsize(300,140)
	deleteMessagesBox.maxsize(300,140)
	deleteMessagesBox.withdraw()
	deleteMessagesTitle = Label(deleteMessagesBox, text = "Delete from this conversation:", font = font1, fg = "#D30C2A")
	deleteMessagesTitle.pack(side = TOP)
	deleteMessages_opt = IntVar()
	deleteMessagesR1 = Radiobutton(deleteMessagesBox, text = "Last message", variable = deleteMessages_opt, value = 1, font = font2)
	deleteMessagesR1.pack(side = TOP, fill = X)
	deleteMessagesR2 = Radiobutton(deleteMessagesBox, text = "All messages", variable = deleteMessages_opt, value = 2, font = font2)
	deleteMessagesR2.pack(side = TOP, fill = X)
	deleteMessagesBoxSubmitButton = Button(deleteMessagesBox, text = "Delete", fg = "white", activeforeground = "white", bg = "dark red", activebackground = "dark red", font = font2, relief = GROOVE)
	deleteMessagesBoxSubmitButton.pack(side = RIGHT, fill = X)

	box.withdraw()

	def __init__(self, selectedUser, linkedCC):
		self.selectedUser = selectedUser
		self.linkedCC = linkedCC
		self.selectedConversation = None
		ConversationWindow.box.deiconify()
		ConversationWindow.box.protocol("WM_DELETE_WINDOW", self.close)
		ConversationWindow.newConversationBox.protocol("WM_DELETE_WINDOW", ConversationWindow.newConversationBox.withdraw)
		ConversationWindow.deleteMessagesBox.protocol("WM_DELETE_WINDOW", ConversationWindow.deleteMessagesBox.withdraw)
		username = self.selectedUser.getUsername()
		if username[-1].lower() == "s":
			newTitle = username + "' Conversations"
		else:
			newTitle = username + "'s Conversations"
		ConversationWindow.title.config(text = newTitle)
		## reset and disable new message controls
		ConversationWindow.newMessageText.set("")
		ConversationWindow.newMessageBox.config(state = DISABLED)
		ConversationWindow.sendMessageButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", fg = "#000000", activeforeground = "#000000")
		ConversationWindow.exitConversationButton.config(state = DISABLED, text = "Exit Conversation")
		ConversationWindow.inviteFriendButton.config(state = DISABLED)
		## refresh the conversations list box
		ConversationWindow.conversationsListBox.delete(0, END)
		for conversation in self.selectedUser.getConversations():
			sep = ", "
			titleList = list({linkedCC.getUserById(uid).getUsername() for uid in conversation.getMembers() if uid != selectedUser.getUserID()})
			if titleList == []:
				conversationtitle = "Just you"
			else:
				conversationtitle = sep.join(titleList)
			ConversationWindow.conversationsListBox.insert(END, conversationtitle)
		## clear messages display
		ConversationWindow.messagesDisplay.config(state = NORMAL)
		ConversationWindow.messagesDisplay.delete(1.0, END)
		ConversationWindow.messagesDisplay.insert(END, "Select a conversation from the list on the left to see messages.")
		ConversationWindow.messagesDisplay.config(state = DISABLED)
		ConversationWindow.conversationsListBox.bind("<ButtonRelease-1>", self.updateMessageDisplay)
		ConversationWindow.sendMessageButton.bind("<ButtonRelease-1>", self.submit)
		ConversationWindow.newMessageBox.bind("<Return>", self.submit)
		ConversationWindow.newConversationButton.config(command = self.showNewConversationBox)
		if list(f for f in self.selectedUser.getFriends() if  f.getStatus() != "Requested" and f.getStatus() != "Pending") != list():
			ConversationWindow.newConversationButton.config(state = NORMAL)
		else:
			ConversationWindow.newConversationButton.config(state = DISABLED)
		ConversationWindow.newConversationBoxSubmitButton.bind("<ButtonRelease-1>", self.addConversation)
		ConversationWindow.newConversationBox.bind("<Return>", self.addConversation)
		ConversationWindow.deleteMessagesBoxSubmitButton.bind("<ButtonRelease-1>", self.deleteMessages)
		ConversationWindow.deleteMessagesBox.bind("<Return>", self.deleteMessages)
		ConversationWindow.inviteFriendButton.config(command = self.showInviteFriendsBox)
		ConversationWindow.deleteMessagesButton.config(command = self.showDeleteMessagesBox, state = DISABLED)
	
	def updateMessageDisplay(self, event = None):
		selectedID = ConversationWindow.conversationsListBox.curselection()
		if selectedID == tuple(): ## check if none is selected:
			ConversationWindow.newMessageText.set("")
			ConversationWindow.newMessageBox.config(state = DISABLED)
			ConversationWindow.sendMessageButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", fg = "#000000", activeforeground = "#000000")
			if self.selectedConversation == None:
				return
		else:
			self.selectedConversation = self.selectedUser.getConversations()[int(selectedID[0])]
		## activate new message controls
		ConversationWindow.newConversationBox.withdraw()
		ConversationWindow.deleteMessagesBox.withdraw()
		ConversationWindow.newMessageBox.config(state = NORMAL)
		ConversationWindow.sendMessageButton.config(state = NORMAL, bg = "#2F54FF", activebackground = "#2F54FF", fg = "#FFFFFF", activeforeground = "#FFFFFF")
		## clear messageDisplay and repopulate with messages
		ConversationWindow.messagesDisplay.config(state = NORMAL)
		ConversationWindow.messagesDisplay.delete(1.0, END)
		ConversationWindow.exitConversationButton.config(state = NORMAL)
		if self.selectedUser.getUserID() in {m.getSender() for m in self.selectedConversation.getMessages()}:
			ConversationWindow.deleteMessagesButton.config(state = NORMAL)
		else:
			ConversationWindow.deleteMessagesButton.config(state = DISABLED)
		if {f.getFriendID() for f in self.selectedUser.getFriends() if f.getStatus() != "Requested" and f.getStatus() != "Pending"} in {m for m in self.selectedConversation.getMembers()}:
			ConversationWindow.inviteFriendButton.config(state = NORMAL)
		else:
			ConversationWindow.inviteFriendButton.config(state = DISABLED)
		lineNum = 1
		for x in reversed(self.selectedConversation.getMessages()):
			sendername = self.linkedCC.getUserById(x.getSender()).getUsername()
			senderColor = "#00A1FF"
			messageColor = "#000000"
			if sendername == self.selectedUser.getUsername():
				sendername = "You"
				senderColor = "#FF596E"
			## Check friendhsip statuses to modify message visibility properties
			if x.getSender() not in list(f.getFriendID() for f in self.selectedUser.getFriends()) and x.getSender() != self.selectedUser.getUserID():
				messageColor = senderColor = "#C0C0C0"
				messageText = "[ This user is not in your friends list; You can only see messages from friends ]"
			elif x.getSender() == self.selectedUser.getUserID():
				messageText = x.getText()
			for f in self.selectedUser.getFriends():
				if f.getFriendID() == x.getSender():
					if f.getStatus() == "Blocked":
						messageColor = senderColor = "#C0C0C0"
						messageText = "[ You've blocked this user; unblock this friend to see messages ]"
					elif f.getStatus() == "Requested":
						messageColor = senderColor = "#4D6082"
						messageText = "[ This user hasn't approved your friend request yet; You'll be able to see messages once your friend request is approved ]"
					elif f.getStatus() == "Pending":
						messageColor = senderColor = "#4D6082"
						messageText = "[ You haven't approved this user's friend request yet ]"
					else:
						messageText = x.getText()
			ConversationWindow.messagesDisplay.insert(END, sendername + " said: " + messageText)
			senderRange = len(sendername) + 7
			senderTag = str(lineNum)+"sendername"
			messageRange = len(messageText)
			messageTag = str(lineNum)+"messagtxt"
			senderTagEnd = str(lineNum) + "." + str(senderRange)
			ConversationWindow.messagesDisplay.tag_add(senderTag, str(lineNum) + ".0", senderTagEnd)
			ConversationWindow.messagesDisplay.tag_config(senderTag, foreground = senderColor)
			ConversationWindow.messagesDisplay.tag_add(messageTag, senderTagEnd, str(lineNum) + "." + str(senderRange + messageRange))
			ConversationWindow.messagesDisplay.tag_config(messageTag, foreground = messageColor)
			lineNum += 1
			ConversationWindow.messagesDisplay.insert(END, "\n")
		ConversationWindow.messagesDisplay.config(state = DISABLED)
		## Edit control bindings based on settings:
		if len(self.selectedConversation.getMembers()) == 1:
			ConversationWindow.exitConversationButton.config(text = "Delete Conversation")
			ConversationWindow.exitConversationButton.bind("<ButtonRelease-1>", self.delConversation)
		else:
			ConversationWindow.exitConversationButton.config(text = "Exit Conversation")
			ConversationWindow.exitConversationButton.bind("<ButtonRelease-1>", self.exitConversation)

	def submit(self, event = None):
		msg = ConversationWindow.newMessageText.get().lstrip().rstrip()
		if msg == "":
			tkMessageBox.showinfo("Epic fail", "You can't send an empty message.")
			ConversationWindow.box.deiconify()
			return
		if self.selectedConversation != None:
			self.selectedConversation.newMessage(self.selectedUser.getUserID(), msg)
		ConversationWindow.newMessageText.set("")
		self.updateMessageDisplay()

	def showNewConversationBox(self, event = None):
		ConversationWindow.newConversationBox.title("New Conversation")
		ConversationWindow.newConversationBoxSubmitButton.bind("<ButtonRelease-1>", self.addConversation)
		ConversationWindow.newConversationMembersListBox.delete(0, END)
		for friend in self.selectedUser.getFriends():
			if friend.getStatus() != "Requested" and friend.getStatus() != "Pending":
				ConversationWindow.newConversationMembersListBox.insert(END, self.linkedCC.getUserById(friend.getFriendID()).getUsername())
		if ConversationWindow.newConversationMembersListBox.get(0, END) != ():
			ConversationWindow.newConversationBox.deiconify()
		else:
			tkMessageBox.showinfo("No friends to add", "You have no friends that can be invited to a new conversation. Friends that are [Requested] or [Pending] cannot be invited to your conversation.")
			ConversationWindow.box.deiconify()

	def showInviteFriendsBox(self, event = None):
		## reuses widgets used for new conversation box
		if self.selectedConversation == None:
			return
		ConversationWindow.newConversationBox.title("Invite Friends")
		ConversationWindow.newConversationBoxSubmitButton.bind("<ButtonRelease-1>", self.inviteFriendstoConversation)
		ConversationWindow.newConversationMembersListBox.delete(0, END)
		alreadyMembers = self.selectedConversation.getMembers()
		for friend in self.selectedUser.getFriends():
			friendID = friend.getFriendID()
			if friendID not in alreadyMembers and friend.getStatus() != "Requested" and friend.getStatus() != "Pending":
				ConversationWindow.newConversationMembersListBox.insert(END, self.linkedCC.getUserById(friendID).getUsername())
		if ConversationWindow.newConversationMembersListBox.get(0, END) != ():
			ConversationWindow.newConversationBox.deiconify()
		else:
			tkMessageBox.showinfo("No friends left to add", "You no longer have any other friends to invite to this conversation. Friends that are [Requested] or [Pending] cannot be invited to your conversation.")
			ConversationWindow.box.deiconify()

	def showDeleteMessagesBox(self, event = None):
		if self.selectedConversation == None:
			return
		ConversationWindow.deleteMessages_opt.set(1)
		ConversationWindow.deleteMessagesBox.deiconify()

	def addConversation(self, event = None):
		friendsPool = list(x for x in ConversationWindow.newConversationMembersListBox.get(0, END))
		selectedFriends = list(friendsPool[int(x)] for x in ConversationWindow.newConversationMembersListBox.curselection())
		members = list(self.linkedCC.getUserByName(x).getUserID() for x in selectedFriends)
		if members == []:
			tkMessageBox.showinfo("Not so fast!", "Select at least one friend to start a new conversation with.")
			ConversationWindow.newConversationBox.deiconify()
			return
		members.append(self.selectedUser.getUserID())
		self.linkedCC.addConversationById(members)
		## refresh the list of conversations:
		self.__init__(self.selectedUser, self.linkedCC)
	
	def inviteFriendstoConversation(self, event = None):
		if self.selectedConversation == None:
			return
		friendsPool = list(x for x in ConversationWindow.newConversationMembersListBox.get(0, END))
		selectedFriends = list(friendsPool[int(x)] for x in ConversationWindow.newConversationMembersListBox.curselection())
		members = list(self.linkedCC.getUserByName(x) for x in selectedFriends)
		if members == []:
			tkMessageBox.showinfo("Not so fast!", "Select at least one friend to invite into the currently selected conversation.")
			ConversationWindow.newConversationBox.deiconify()
			return
		for x in members:
			x.addConversation(self.selectedConversation)
		## refresh the list of conversations:
		self.__init__(self.selectedUser, self.linkedCC)

	def deleteMessages(self, event = None):
		if self.selectedConversation == None:
			return
		delMode = ConversationWindow.deleteMessages_opt.get()
		if delMode == 1:
			if tkMessageBox.askyesno("Delete Last Message - Confirm", "Are you sure you want to delete the last message you sent in this conversation? This cannot be undone.", default = "no") == False:
				self.close()
				ConversationWindow.box.deiconify()
				return
			self.selectedConversation.deleteMessageByIndex(-1)
		elif delMode == 2:
			if tkMessageBox.askyesno("Delete All Messages - Confirm", "Are you sure you want to delete all messages you sent in this conversation? This cannot be undone.", default = "no") == False:
				self.close()
				ConversationWindow.box.deiconify()
				return
			messagesToDelete = list(m for m in self.selectedConversation.getMessages() if m.getSender() == self.selectedUser.getUserID())
			for m in messagesToDelete:
				self.selectedConversation.deleteMessageByValue(m)
		## refresh the list of conversations:
		self.updateMessageDisplay()
		ConversationWindow.box.deiconify()

	def exitConversation(self, event = None):
		if self.selectedConversation == None:
			return
		## confirm with user
		if tkMessageBox.askyesno("Exit Conversation - Confirm", "Are you sure you want to exit the currently selected conversation? (Your messages will remain as long as your account exists, or until this conversation is deleted.)", default = "no") == False:
			ConversationWindow.box.deiconify()
			return
		self.selectedUser.exitConversation(self.selectedConversation)
		## refresh the list of conversations:
		self.__init__(self.selectedUser, self.linkedCC)

	def delConversation(self, event = None):
		if self.selectedConversation == None:
			return
		## confirm with user
		if tkMessageBox.askyesno("Delete Conversation - Confirm", "Are you sure you want to delete the currently selected conversation? This cannot be undone.", default = "no") == False:
			ConversationWindow.box.deiconify()
			return
		self.selectedUser.exitConversation(self.selectedConversation)
		## refresh the list of conversations:
		self.__init__(self.selectedUser, self.linkedCC)

	def close(self, event = None):
		ConversationWindow.newConversationBox.withdraw()
		ConversationWindow.deleteMessagesBox.withdraw()
		ConversationWindow.box.withdraw()

class FriendAddWindow:
	plusIcon = PhotoImage(file = "img/plus.gif")
	unameIcon = PhotoImage(file = "img/user_login.gif")
	friendrequestbox = Toplevel(mainWindow, padx = 14, pady = 14)
	friendrequestbox.title("Add a Friend")
	friendrequestbox.maxsize(350,150)
	friendrequestbox.minsize(350,150)
	username = StringVar()
	friendrequestbox.protocol("WM_DELETE_WINDOW", friendrequestbox.withdraw)

	frame1 = Frame(friendrequestbox)
	frame1.pack(side = TOP, fill = X)
	frame2 = Frame(friendrequestbox)
	frame2.pack(side = TOP, fill = X)
	frame3 = Frame(friendrequestbox)
	frame3.pack(side = BOTTOM, fill = X)
	plusImg = Label(frame1, image = plusIcon)
	plusImg.pack(side = LEFT)
	addFriendTitle = Label(frame1, text = "Add a Friend", font = font3, padx = 5, fg = "#FF4263")
	addFriendTitle.pack(side = LEFT)
	usernameLabelImg = Label(frame2, image = unameIcon)
	usernameLabelImg.pack(side = LEFT)
	usernameLabelTxt = Label(frame2, text = "Username: ", font=font1)
	usernameLabelTxt.pack(side = LEFT)
	usernameBox = Entry(frame2, font=font2, relief = FLAT, textvariable = username)
	usernameBox.pack(side = LEFT, expand = True)
	sendButton = Button(frame3, text = "Send Request", font=font1, bg = "dark green", fg = "#ffffff", activebackground = "dark green", activeforeground = "#ffffff", relief = GROOVE)
	cancelButton = Button(frame3, text = "Cancel", font=font1, bg = "dark red", fg = "#ffffff", activebackground = "dark red", activeforeground = "#ffffff", command = friendrequestbox.withdraw, relief = GROOVE)
	cancelButton.pack(side = RIGHT)
	sendButton.pack(side = RIGHT)

	friendrequestbox.withdraw()

	## 'savecommand' argument must be a method
	def __init__(self, usr, postcommand, linkedCC):
		self.linkedCC = linkedCC
		self.requesterID = usr.getUserID()
		self.postcommand = postcommand
		FriendAddWindow.username.set("")
		FriendAddWindow.sendButton.bind("<ButtonRelease-1>", self.send)
		FriendAddWindow.friendrequestbox.bind("<Return>", self.send)

		FriendAddWindow.friendrequestbox.deiconify()

	def send(self, event):
		matchinguser = self.linkedCC.getUserByName(FriendAddWindow.username.get())
		if matchinguser == None:
			## user does not exist; wrong username
			tkMessageBox.showerror("User not found", "The user '" + FriendAddWindow.username.get() + "' does not exist.\nFriend request not sent.")
			FriendAddWindow.friendrequestbox.withdraw()
			return
		elif matchinguser.getUserID() == self.requesterID:
			## you can't add yourself as friend!
			tkMessageBox.showinfo("That's you!", "The user '" + FriendAddWindow.username.get() + "' is you.\nFriend request not sent.")
			FriendAddWindow.friendrequestbox.withdraw()
			return
		else:
			## check if already in friend list
			for friend in matchinguser.getFriends():
				if friend.getFriendID() == self.requesterID:
					tkMessageBox.showinfo("Epic fail", "The user '" + FriendAddWindow.username.get() + "' is already in your friends list.\nYou can see a list of your friends and available options to the right of the main window.")
					FriendAddWindow.friendrequestbox.withdraw()
					return
			friendID = matchinguser.getUserID()
		self.linkedCC.addFriendshipById(self.requesterID, friendID)
		self.postcommand()
		FriendAddWindow.friendrequestbox.withdraw()

class EditProfileWindow:
	wrenchIcon = PhotoImage(file="img/wrench.gif")
	unameIcon = PhotoImage(file = "img/user_login.gif")
	keyIcon = PhotoImage(file = "img/key.gif")
	photoIcon = PhotoImage(file = "img/pictureframe.gif")
	editprofilebox = Toplevel(mainWindow, padx = 14, pady = 14)
	editprofilebox.title("Edit Profile")
	editprofilebox.maxsize(650,500)
	editprofilebox.minsize(650,500)
	profileUsername = StringVar()
	profilePassword = StringVar()
	editprofilebox.protocol("WM_DELETE_WINDOW", editprofilebox.withdraw)
	maleIcon = PhotoImage(file = "img/male.gif")
	femaleIcon = PhotoImage(file = "img/female.gif")
	calendarIcon = PhotoImage(file = "img/calendar.gif")

	editprofileboxFrame1 = Frame(editprofilebox)
	editprofileboxFrame1.pack(side = TOP, fill = X)
	editprofileboxFrame2 = Frame(editprofilebox)
	editprofileboxFrame2.pack(side = TOP, fill = X)
	editprofileboxFrame21 = Frame(editprofilebox)
	editprofileboxFrame21.pack(side = TOP, fill = X)
	editprofileboxFrame22 = Frame(editprofilebox)
	editprofileboxFrame22.pack(side = TOP, fill = X)
	editprofileboxFrame23 = Frame(editprofilebox)
	editprofileboxFrame23.pack(side = TOP, fill = X)
	editprofileboxFrame241 = Frame(editprofilebox)
	editprofileboxFrame241.pack(side = TOP, fill = X)
	editprofileboxFrame242 = Frame(editprofilebox)
	editprofileboxFrame242.pack(side = TOP, fill = X)
	editprofileboxFrame251 = Frame(editprofilebox)
	editprofileboxFrame251.pack(side = TOP, fill = X)
	editprofileboxFrame252 = Frame(editprofilebox)
	editprofileboxFrame252.pack(side = TOP, fill = X)
	editprofileboxFrame3 = Frame(editprofilebox)
	editprofileboxFrame3.pack(side = BOTTOM, fill = X)
	wrenchImg = Label(editprofileboxFrame1, image = wrenchIcon)
	wrenchImg.pack(side = LEFT)
	settingsTitle = Label(editprofileboxFrame1, text = "Settings", font = font3, padx = 5, fg = "#0062A8")
	settingsTitle.pack(side = LEFT)
	usernameLabelImg = Label(editprofileboxFrame2, image = unameIcon)
	usernameLabelImg.pack(side = LEFT)
	usernameLabelTxt = Label(editprofileboxFrame2, text = "Username: ", font=font1)
	usernameLabelTxt.pack(side = LEFT)
	usernameBox = Entry(editprofileboxFrame2, font=font2, relief = FLAT, textvariable = profileUsername)
	usernameBox.pack(side = LEFT, expand = True)
	passwordLabelImg = Label(editprofileboxFrame2, image = keyIcon)
	passwordLabelImg.pack(side = LEFT)
	passwordLabelTxt = Label(editprofileboxFrame2, text = "    Password: ", font=font1)
	passwordLabelTxt.pack(side = LEFT)
	passwordBox = Entry(editprofileboxFrame2, font=font2, relief = FLAT, textvariable = profilePassword)
	passwordBox.pack(side = LEFT, expand = True)
	profilepicLabelImg = Label(editprofileboxFrame21, image = photoIcon)
	profilepicLabelImg.pack(side = LEFT)
	profilepicLabelTxt = Label(editprofileboxFrame21, text = "Profile Picture: ", font=font1)
	profilepicLabelTxt.pack(side = LEFT)
	profilePicture = StringVar()
	profilepicLabelTxt2 = Label(editprofileboxFrame21, textvariable = profilePicture, font=font4, width=50)
	profilepicLabelTxt2.pack(side = LEFT)
	profilepicButton = Button(editprofileboxFrame21, text = "Select File", font=font2, relief = GROOVE)
	profilepicButton.pack(side = LEFT)
	gender = StringVar()
	gender.set("M")
	genderLabel = Label(editprofileboxFrame22, text = "Gender: ", font = font1)
	genderLabel.pack(side = LEFT)
	maleImg = Label(editprofileboxFrame22, image = maleIcon)
	maleImg.pack(side = LEFT)
	radioM = Radiobutton(editprofileboxFrame22, font = font2, value = "M", variable = gender, text = "Male")
	radioM.pack(side = LEFT)
	femaleImg = Label(editprofileboxFrame22, image = femaleIcon)
	femaleImg.pack(side = LEFT)
	radioF = Radiobutton(editprofileboxFrame22, font = font2, value = "F", variable = gender, text = "Female")
	radioF.pack(side = LEFT)
	bdayImg = Label(editprofileboxFrame23, image = calendarIcon)
	bdayImg.pack(side = LEFT)
	bdayLabel = Label(editprofileboxFrame23, text = "Birthday: ", font = font1)
	bdayLabel.pack(side = LEFT)
	bday_m = StringVar()
	bdaymonthSpinner = Spinbox(editprofileboxFrame23, values = MONTHS, font = font2, textvariable = bday_m, width=10, wrap = True)
	bdaymonthSpinner.pack(side = LEFT)
	bday_d = StringVar()
	bdaydaySpinner = Spinbox(editprofileboxFrame23, from_ = 1, to=31, font = font2, textvariable = bday_d, width=2, wrap = True)
	bdaydaySpinner.pack(side = LEFT)
	bday_y = StringVar()
	## make use of tm_year, imported by the user.py file
	currentDate = localtime()
	bdayyearSpinner = Spinbox(editprofileboxFrame23, from_ = currentDate.tm_year-150, to=currentDate.tm_year, font = font2, textvariable = bday_y, width=4)
	bdayyearSpinner.pack(side = LEFT)
	bday_y.set(str(currentDate.tm_year))
	bday_m.set(MONTHS[currentDate.tm_mon-1])
	bday_d.set(str(currentDate.tm_mday))
	jobHistoryLabel = Label(editprofileboxFrame241, text = "Job History (One job per line, newest first): ", font = font1)
	jobHistoryLabel.pack(side = LEFT)
	jobHistoryBoxScrollBar = Scrollbar(editprofileboxFrame242)
	jobHistoryBoxScrollBar.pack(side = RIGHT, fill = Y)
	jobHistoryBox = Text(editprofileboxFrame242, font = font21, height = 4, yscrollcommand = jobHistoryBoxScrollBar.set)
	jobHistoryBox.pack(side = LEFT, fill = X)
	jobHistoryBoxScrollBar.config(command = jobHistoryBox.yview)
	eduHistoryLabel = Label(editprofileboxFrame251, text = "Education History (One school per line, latest first): ", font = font1)
	eduHistoryLabel.pack(side = LEFT)
	eduHistoryBoxScrollBar = Scrollbar(editprofileboxFrame252)
	eduHistoryBoxScrollBar.pack(side = RIGHT, fill = Y)
	eduHistoryBox = Text(editprofileboxFrame252, font = font21, height = 4, yscrollcommand = eduHistoryBoxScrollBar.set)
	eduHistoryBox.pack(side = LEFT, fill = X)
	eduHistoryBoxScrollBar.config(command = eduHistoryBox.yview)
	saveButton = Button(editprofileboxFrame3, text = "Save", font=font1, bg = "dark green", fg = "#ffffff", activebackground = "dark green", activeforeground = "#ffffff", relief = GROOVE)
	cancelButton = Button(editprofileboxFrame3, text = "Cancel", font=font1, bg = "dark red", fg = "#ffffff", activebackground = "dark red", activeforeground = "#ffffff", command = editprofilebox.withdraw, relief = GROOVE)
	deleteMeButton = Button(editprofileboxFrame3, text = "Delete Me", font=font2, fg = "red", activeforeground = "red", relief = GROOVE)
	deleteMeButton.pack(side=LEFT)
	cancelButton.pack(side = RIGHT)
	saveButton.pack(side = RIGHT)

	editprofilebox.withdraw()

	## 'savecommand' argument must be a method
	def __init__(self, usr, DANGER_deleteusercommand, savecommand):
		self.lastsavedSettings = dict()
		self.savecommand = savecommand
		self.DANGER_deleteusercommand = DANGER_deleteusercommand
		EditProfileWindow.profileUsername.set(usr.getUsername())
		EditProfileWindow.profilePassword.set(usr.getPassword())
		EditProfileWindow.gender.set(usr.getGender()[0])
		usrBday = usr.getBdayDict()
		EditProfileWindow.bday_y.set(str(usrBday['year']))
		EditProfileWindow.bday_m.set(MONTHS[usrBday['month']-1])
		EditProfileWindow.bday_d.set(str(usrBday['day']))
		EditProfileWindow.profilePicture.set("")
		EditProfileWindow.jobHistoryBox.delete(1.0, END)
		jobhistory = usr.getJobHistory()
		for job in jobhistory:
			if job != jobhistory[0]:
				EditProfileWindow.jobHistoryBox.insert(END, "\n")
			EditProfileWindow.jobHistoryBox.insert(END, job)
		EditProfileWindow.eduHistoryBox.delete(1.0, END)
		eduhistory = usr.getEducationHistory()
		for school in eduhistory:
			if school != eduhistory[0]:
				EditProfileWindow.eduHistoryBox.insert(END, "\n")
			EditProfileWindow.eduHistoryBox.insert(END, school)
		EditProfileWindow.settingsTitle.config(text = EditProfileWindow.profileUsername.get() + " : Settings")
		EditProfileWindow.profilepicButton.bind("<ButtonRelease-1>", self.getProfilepicFilename)
		EditProfileWindow.saveButton.bind("<ButtonRelease-1>", self.save)
		EditProfileWindow.deleteMeButton.bind("<ButtonRelease-1>", self.DANGER_destroyUser)

		EditProfileWindow.editprofilebox.deiconify()
	
	def getProfilepicFilename(self, event = None):
		EditProfileWindow.profilePicture.set(tkFileDialog.askopenfilename(filetypes = [('GIF Images', '.gif')]))
		EditProfileWindow.editprofilebox.deiconify()

	def DANGER_destroyUser(self, event = None):
		resp = self.DANGER_deleteusercommand()
		if resp == "SUCCESS":
			EditProfileWindow.editprofilebox.withdraw()
		elif resp == "CANCELED":
			EditProfileWindow.editprofilebox.deiconify()
		else:
			EditProfileWindow.editprofilebox.deiconify()
			tkMessageBox.showerror("Could not delete this user", resp)
		return

	def save(self, event = None):
		currentDate = localtime()
		## fix birthdate: the year can't be > current year or < 0
		try:
			if int(EditProfileWindow.bday_y.get()) > currentDate.tm_year:
				tkMessageBox.showerror("Invalid Bday Year", "Your birth year cannot be set in the future. (You entered "+EditProfileWindow.bday_y.get()+")")
				EditProfileWindow.bday_y.set(str(currentDate.tm_year))
				EditProfileWindow.editprofilebox.deiconify()
				return
			elif int(EditProfileWindow.bday_y.get()) < 0:
				tkMessageBox.showerror("Invalid Bday Year", "Your birth year cannot be negative. (You entered "+EditProfileWindow.bday_y.get()+")")
				EditProfileWindow.bday_y.set("1996")
				EditProfileWindow.editprofilebox.deiconify()
				return
			## Fix bday formatting:
			## convert month to proper format
			monthStr = EditProfileWindow.bday_m.get().lower()
			monthStr = monthStr[0].upper() + monthStr[1:]
			## check if monthStr is a month's name
			if monthStr not in MONTHS:
				tkMessageBox.showerror("Invalid Birth Month", "Enter the name of a month")
				EditProfileWindow.editprofilebox.deiconify()
				return
			## the above check assures it is inside the MONTHS tuple
			monthIndex = MONTHS.index(monthStr)+1
			day = int(EditProfileWindow.bday_d.get())
			year = int(EditProfileWindow.bday_y.get())
			## check if day is in range of month
			if day not in range(1, month_num_of_days(month = monthIndex+1, year = year)+1):
				tkMessageBox.showerror("Invalid Birth Day", "The day you entered is not within the range of dates available to the month and year given")
				EditProfileWindow.bday_d.set("1")
				EditProfileWindow.editprofilebox.deiconify()
				return
		except ValueError:
			tkMessageBox.showerror("Error", "You entered a non-numeric character where only an integer is allowed.")
			EditProfileWindow.editprofilebox.deiconify()
			return
		except:
			tkMessageBox.showerror("Error", "There was an unknown error interpreting your input.")
			EditProfileWindow.editprofilebox.deiconify()
			return
		self.lastsavedSettings['gender'] = EditProfileWindow.gender.get()
		self.lastsavedSettings['bday'] = dict(day=day, month=monthIndex, year=year)
		self.lastsavedSettings['username'] = EditProfileWindow.profileUsername.get()
		self.lastsavedSettings['password'] = EditProfileWindow.profilePassword.get()
		self.lastsavedSettings['profilepic'] = EditProfileWindow.profilePicture.get()
		joblist = EditProfileWindow.jobHistoryBox.get(1.0, END).replace("\t","").replace(":","").replace("|","")
		edulist = EditProfileWindow.eduHistoryBox.get(1.0, END).replace("\t","").replace(":","").replace("|","")
		self.lastsavedSettings['jobhistory'] = list(j for j in joblist.split("\n") if j != "")
		self.lastsavedSettings['eduhistory'] = list(e for e in edulist.split("\n") if e != "")
		self.savecommand(self.lastsavedSettings)
		EditProfileWindow.editprofilebox.withdraw()

class FriendshipEditWindow():
	slidersIcon = PhotoImage(file = "img/sliders.gif")
	personaIcon = PhotoImage(file = "img/persona.gif")
	box = Toplevel(mainWindow, padx = 14, pady = 14)
	box.title("Change Friendship Status")
	box.maxsize(400,250)
	box.minsize(400,250)
	box.protocol("WM_DELETE_WINDOW", box.withdraw)
	lastsavedStatus = StringVar()

	frame1 = Frame(box)
	frame1.pack(side = TOP, fill = X)
	frame2 = Frame(box)
	frame2.pack(side = TOP, fill = X)
	frame3 = Frame(box)
	frame3.pack(side = TOP, fill = X)
	frame4 = Frame(box)
	frame4.pack(side = TOP, fill = X)
	frame5 = Frame(box)
	frame5.pack(side = BOTTOM, fill = X)
	plusImg = Label(frame1, image = slidersIcon)
	plusImg.pack(side = LEFT)
	editFriendshipTitle = Label(frame1, text = "Change Friendship Status", font = font3, padx = 5, fg = "#00A0A3")
	editFriendshipTitle.pack(side = LEFT)
	affectedLabelTxt = Label(frame2, text = "Affected: ", font=font2, wraplength = 370, justify = LEFT)
	affectedLabelTxt.pack(side = LEFT)
	statusLabelImg = Label(frame3, image = personaIcon)
	statusLabelImg.pack(side = LEFT)
	statusLabelTxt = Label(frame3, text = "Set Status to:", font = font2)
	statusLabelTxt.pack(side = LEFT)
	
	RadioF = Radiobutton(frame4, text="Friend", variable=lastsavedStatus, value="F", font = font2)
	RadioF.pack(side = LEFT, fill = X)
	RadioC = Radiobutton(frame4, text="Close Friend", variable=lastsavedStatus, value="C", font = font2)
	RadioC.pack(side = LEFT, fill = X)
	RadioH = Radiobutton(frame4, text="Hide Updates", variable=lastsavedStatus, value="H", font = font2)
	RadioH.pack(side = LEFT, fill = X)
	RadioB = Radiobutton(frame4, text="Block", variable=lastsavedStatus, value="B", font = font2)
	RadioB.pack(side = LEFT, fill = X)

	sendButton = Button(frame5, text = "Save Settings", font=font1, bg = "dark green", fg = "#ffffff", activebackground = "dark green", activeforeground = "#ffffff", relief = GROOVE)
	cancelButton = Button(frame5, text = "Cancel", font=font1, bg = "dark red", fg = "#ffffff", activebackground = "dark red", activeforeground = "#ffffff", command = box.withdraw, relief = GROOVE)
	cancelButton.pack(side = RIGHT)
	sendButton.pack(side = RIGHT)

	box.withdraw()

	def hide(self):
		FriendshipEditWindow.box.withdraw()

	def __init__(self, user, affected, linkedCC, savecommand):
		self.targetUser = user
		self.affected = affected
		if self.affected == list():
			return ## extra checkpoint; at least one friend must be affected
		## figure out if the user is just Approving Requests
		justapproving = True
		for x in self.affected:
			if x.getStatus() != "Pending":
				justapproving = False
				break
		self.linkedCC = linkedCC
		self.savecommand = savecommand
		FriendshipEditWindow.RadioF.select()
		if not justapproving:
			FriendshipEditWindow.box.deiconify()
			FriendshipEditWindow.sendButton.bind("<ButtonRelease-1>", self.save)
			FriendshipEditWindow.box.bind("<Return>", self.save)
			affectedNames = list()
			for x in self.affected:
				affectedNames.append(self.linkedCC.getUserById(x.getFriendID()).getUsername())
			sep = ", "
			FriendshipEditWindow.affectedLabelTxt.config(text = "Affected: " + sep.join(affectedNames))
		else:
			usrID = self.targetUser.getUserID()
			for friend in self.affected:
				friend.setStatus('F')
				for x in self.linkedCC.getUserById(friend.getFriendID()).getFriends():
					if x.getFriendID() == usrID:
						x.setStatus('F')
						break
			self.savecommand()

	def save(self, event = None):
		newstatus = FriendshipEditWindow.lastsavedStatus.get()
		for f in self.affected:
			f.setStatus(newstatus)
		FriendshipEditWindow.box.withdraw()
		self.savecommand()

LogoImg = PhotoImage(file = "img/logo_small.gif")
LogoLabel = Label(adminFrame, image = LogoImg, relief = FLAT)
LogoLabel.pack(side=TOP, fill=X)
userListLabel = Label(adminFrame, text="Select a User Point-of-View: ", fg="#1E996C", font=font0)
userListLabel.pack(side=TOP, fill=X)
userListFrame = Frame(adminFrame, height=200, relief = FLAT)
userListFrame.pack(side=TOP, fill=X)
adminFrameScrollBar = Scrollbar(userListFrame)
adminFrameScrollBar.pack(side=RIGHT, fill=Y)
userListBox = Listbox(userListFrame, yscrollcommand = adminFrameScrollBar.set, font=("Helvetica", 11, "normal"), selectbackground="#1E996C", selectforeground="#FFFFFF", selectmode=SINGLE, height=15)
userListBox.pack(side=TOP, fill=BOTH, expand=True)
adminFrameScrollBar.config(command = userListBox.yview)

def refreshUserListBox():
	## This function should be used when refreshing later
	userListBox.delete(0, END)
	for profile in cc.getUsers():
		userListBox.insert(END, profile.getUsername())
	userListBox.activate(cc.getSelected().getUserID())
	updateAwesomesauceControls()

## insert list of users for the first time.
for profile in cc.getUsers():
	userListBox.insert(END, profile.getUsername())

controlBoxLabel = Label(adminFrame, text="Basic Credentials: ", fg="#008FD5", font=font0)
controlBoxLabel.pack(side=TOP, fill=X)
controlBoxFrame1 = Frame(adminFrame)
controlBoxFrame1.pack(side=TOP, fill=X)
userIDLabel = Label(controlBoxFrame1, text="User ID: ", font=font1)
userIDLabel.pack(side=LEFT)
userIDBox = Label(controlBoxFrame1, font=font2)
userIDBox.pack(side=LEFT)
controlBoxFrame2 = Frame(adminFrame)
controlBoxFrame2.pack(side=TOP, fill=X)
nameBoxLabel = Label(controlBoxFrame2, text="Username: ", font=font1)
nameBoxLabel.pack(side=LEFT)
nameBox = Label(controlBoxFrame2, font=font2)
nameBox.pack(side=LEFT)
controlBoxFrame3 = Frame(adminFrame)
controlBoxFrame3.pack(side=TOP, fill=X)
passwordLabel = Label(controlBoxFrame3, text="Password: ", font=font1)
passwordLabel.pack(side=LEFT)
passwordBox = Label(controlBoxFrame3, font=font2)
passwordBox.pack(side=LEFT)
controlBoxFrame4 = Frame(adminFrame)
controlBoxFrame4.pack(side=BOTTOM, fill=X)
newUserButton = Button(controlBoxFrame4, font = font1, text = "Sign Up", bg = "#A3FF00", activebackground = "#A3FF00", fg = "#000000", activeforeground = "#000000", padx = 10, relief = GROOVE)
newUserButton.pack(side = TOP, expand = True)

profileDisplay = Frame(userFrame, relief = FLAT, height=128)
profileDisplay.pack(side=TOP, fill=X)
photofilename = "img/defaultpic.gif"
profilepicfile = PhotoImage(file = photofilename)
profilePicture = Label(profileDisplay, bg="#ffffff", height = 128, width=128, image=profilepicfile, padx = 0, pady = 0)
profilePicture.pack(side=LEFT)
profileDisplayFrame1 = Frame(profileDisplay)
profileDisplayFrame1.pack(side = TOP, fill=X)
profileName = Label(profileDisplayFrame1, text="Welcome to Treefort", font = font3, padx = 5, pady = 0.5)
profileName.pack(side=LEFT)
profileDisplayFrame2 = Frame(profileDisplay)
profileDisplayFrame2.pack(side = TOP, fill=X)
profileSubLabel1 = Label(profileDisplayFrame2, text="Select a user to change the point of view.", font = font2, justify=LEFT, padx = 5, pady =  0.5)
profileSubLabel1.pack(side=LEFT)
profileSubLabel2 = Label(profileDisplayFrame2, font = font1, justify=LEFT, padx = 5, pady =  0.5, fg = "#7F006E")
profileSubLabel2.pack(side=LEFT)
profileSubLabel3 = Label(profileDisplayFrame2, font = font1, justify=LEFT, padx = 5, pady =  0.5, fg = "#21007F")
profileSubLabel3.pack(side=LEFT)
profileDisplayFrame3 = Frame(profileDisplay)
profileDisplayFrame3.pack(side = TOP, fill=X)
profileSubLabel4 = Label(profileDisplayFrame3, font = font1, justify=LEFT, padx = 5, pady =  0.5, fg = "#9E2400")
profileSubLabel4.pack(side=LEFT)
profileDisplayFrame4 = Frame(profileDisplay)
profileDisplayFrame4.pack(side = TOP, fill=X)
profileSubLabel5 = Label(profileDisplayFrame4, font = font1, justify=LEFT, padx = 5, pady =  0.5, fg = "#004A7F")
profileSubLabel5.pack(side=LEFT)

profileDisplayFrame3 = Frame(profileDisplay)
profileDisplayFrame3.pack(side = TOP, fill=X)

def saveProfileChanges(newsettings):
	if newsettings == dict():
		return ## check if empty
	try:
		resp = cc.editUserById(uid = cc.getSelected().getUserID(), username = newsettings['username'], password = newsettings['password'], profilepic = newsettings['profilepic'], gender = newsettings['gender'], bday = newsettings['bday'], jobhistory = newsettings['jobhistory'], eduhistory = newsettings['eduhistory'])
	except IndexError:
		tkMessageBox.showerror("Error","The submitted settings were incomplete.")
		return
	if resp != "SUCCESS":
		tkMessageBox.showerror("Error","We couldn't change your user settings because:\n" + resp)
		return
	refreshUserListBox()
	updateAwesomesauceControls(None)

def deleteMe():
	if tkMessageBox.askyesno("Delete User Account - Confirm","Are you sure you want to delete the currently selected User Account? This will also delete all of this account's messages and status posts. This cannot be undone.",default="no") != True:
		return "CANCELED"
	resp = cc.deleteUserById(cc.getSelected().getUserID())
	if resp == "SUCCESS":
		refreshUserListBox()
	return resp

def editprofile():
	selectedUser = cc.getSelected()
	if selectedUser == None:
		tkMessageBox.showinfo("No User Selected","No user is currently selected. Select a user (and log in) first by clicking on one of the names in the User List Box located in the left pane.")
		return
	if selectedUser.isLoggedIn() == False:
		tkMessageBox.showinfo("User Not Logged In","The current user is not logged in. Only logged-in users can change their profile settings.")
		return
	editprofilewin = EditProfileWindow(selectedUser, deleteMe, saveProfileChanges)
	del editprofilewin

def addfriend():
	selectedUser = cc.getSelected()
	if selectedUser == None:
		return
	addfriendwin = FriendAddWindow(selectedUser, updateAwesomesauceControls, cc)
	del addfriendwin

def registerNewUser():
	signupwin = SignUpWindow(mainWindow, "Sign Up for Treefort", newUser, refreshUserListBox)
	del signupwin

def viewConversations():
	selectedUser = cc.getSelected()
	if selectedUser == None:
		return
	conversationWin = ConversationWindow(selectedUser, cc)

newUserButton.config(command = registerNewUser)

addFriendButton = Button(profileDisplayFrame3, text="Add a Friend", state=DISABLED, font=font2, bg="#C0C0C0", fg="black", activebackground = "#C0C0C0", activeforeground = "black", command = addfriend, relief = GROOVE)
addFriendButton.pack(side=LEFT)
vewConversationsButton = Button(profileDisplayFrame3, text="View Conversations", state=DISABLED, font=font2, bg="#C0C0C0", fg="black", activebackground = "#C0C0C0", activeforeground = "black", command = viewConversations, relief = GROOVE)
vewConversationsButton.pack(side=LEFT)
profileSettingsButton = Button(profileDisplayFrame3, text="Edit Profile", state=DISABLED, font=font2, bg="#C0C0C0", fg="black", activebackground = "#C0C0C0", activeforeground = "black", command = editprofile, relief = GROOVE)
profileSettingsButton.pack(side=LEFT)
loginoutButton = Button(profileDisplayFrame3, text="Log In", font=font2, command=logInOut, bg="#004A7F", fg="white", activebackground = "#004A7F", activeforeground = "white", relief = GROOVE)
loginoutButton.pack(side=LEFT)

friendsDisplay = Frame(userFrame, relief = FLAT, width = 240)
friendsDisplay.pack(side=RIGHT, fill=Y)
friendsSubFrame1 = Frame(friendsDisplay, relief = GROOVE)
friendsSubFrame1.pack(side = TOP, fill=X)
friendsListLabel = Label(friendsSubFrame1, fg="#FF7137", font=font0)
friendsListLabel.pack(side=TOP, fill=X)
friendsListScrollBar = Scrollbar(friendsSubFrame1)
friendsListScrollBar.pack(side = RIGHT, fill=Y)
friendsListBox = Listbox(friendsSubFrame1, relief = FLAT, font = font2, yscrollcommand = friendsListScrollBar.set, height = 10, selectmode = MULTIPLE, state = DISABLED, selectforeground="#ffffff", selectbackground="#FF7137")
friendsListBox.pack(side=LEFT, fill=X)
friendsListScrollBar.config(command = friendsListBox.yview)
friendsSubFrame2 = Frame(friendsDisplay, relief = GROOVE)
friendsSubFrame2.pack(side = TOP, fill=X)
friendNameLabel = Label(friendsSubFrame2, font = font0, fg = "#FF3A27", wraplength=170)
friendNameLabel.pack(side = TOP, fill=X)
friendshipStatusLabel = Label(friendsSubFrame2, font = font4, fg = "#000000", wraplength=170)
friendshipStatusLabel.pack(side = TOP, fill=X)
friendshipGroupLabel = Label(friendsSubFrame2, font = font4, fg = "#000000", wraplength=170)
friendshipGroupLabel.pack(side = TOP, fill=X)

nextIcon = PhotoImage(file = "img/next.gif")
prevIcon = PhotoImage(file = "img/prev.gif")

statusBoxFrame = Frame(userFrame, relief = FLAT)
statusBoxFrame.pack(side = TOP, fill = X)
statusBoxSubFrame1 = Frame(statusBoxFrame, relief = FLAT)
statusBoxSubFrame1.pack(side = TOP, fill = X)
statusBoxLabel = Label(statusBoxSubFrame1, text = "Post Status: ", font = font1, relief = FLAT)
statusBoxLabel.pack(side = LEFT, fill = X)
statusBoxSubFrame2 = Frame(statusBoxFrame, relief = FLAT)
statusBoxSubFrame2.pack(side = TOP, fill = X)
statusBoxScrollBar = Scrollbar(statusBoxSubFrame2)
statusBoxScrollBar.pack(side = RIGHT, fill = Y)
statusBox = Text(statusBoxSubFrame2, font = font2, height = 4, padx = 12, pady = 12, yscrollcommand = statusBoxScrollBar.set, state = DISABLED, wrap = WORD)
statusBox.pack(side = LEFT, fill = X, expand = True)
statusBoxScrollBar.config(command = statusBox.yview)
statusBoxSubFrame3 = Frame(statusBoxFrame, relief = FLAT)
statusBoxSubFrame3.pack(side = TOP, fill = X)
postStatusButton = Button(statusBoxSubFrame3, text = "Post", font = font1, fg = "#ffffff", activeforeground = "#ffffff", bg = "#C0C0C0", activebackground = "#C0C0C0", state = DISABLED, relief = GROOVE)
postStatusButton.pack(side = LEFT)

newsFeedArea = Frame(userFrame, relief = FLAT)
newsFeedArea.pack(side = TOP, fill = BOTH, expand = True)

newsFeedControls = Frame(newsFeedArea, relief = FLAT)
newsFeedControls.pack(side = TOP, fill = X)
newsFeedLabel = Label(newsFeedControls, text = "\nNews Feed: ", font = font1)
newsFeedLabel.pack(side = LEFT)
nextInFeedButton = Button(newsFeedControls, image = nextIcon, state = DISABLED, relief = GROOVE)
prevInFeedButton = Button(newsFeedControls, image = prevIcon, state = DISABLED, relief = GROOVE)
nextInFeedButton.pack(side = RIGHT)
prevInFeedButton.pack(side = RIGHT)

newsFeedSlide = Frame(newsFeedArea, relief = SUNKEN)
newsFeedSlide.pack(side = TOP, fill = BOTH, expand = True)
statusPosterDetailsFrame = Frame(newsFeedSlide)
statusPosterDetailsFrame.pack(side = TOP, fill = X)
pp = PhotoImage(file = "img/defaultpic.gif")
statusPosterProfilePic = Label(statusPosterDetailsFrame, image = pp, width = 128, height = 128, state = DISABLED, pady = 2, padx = 2)
statusPosterProfilePic.pack(side = LEFT)
statusPosterDetailsSubFrame1 = Frame(statusPosterDetailsFrame)
statusPosterDetailsSubFrame1.pack(side = TOP, fill = X)
statusPosterName = Label(statusPosterDetailsSubFrame1, text = "", font = font2, padx = 5)
statusPosterName.pack(side = LEFT)
statusTimestamp = Label(statusPosterDetailsSubFrame1, text = "", font = font2, fg = "#1742B7", padx = 5)
statusTimestamp.pack(side = LEFT)
statusPosterDetailsSubFrame2 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame2.pack(side = TOP, fill = X)
statusPosterDetailsSubFrame21 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame21.pack(side = TOP, fill = X)
statusThumbsUpsCount = Label(statusPosterDetailsSubFrame2, text = "", font = font1, fg = "#32B71B", padx = 5, pady = 5)
statusThumbsUpsCount.pack(side = LEFT)
thumbsUpButton = Button(statusPosterDetailsSubFrame21, fg = "#32B71B", font = font4, activeforeground = "#32B71B", text = "+Thumbs Up", state = DISABLED, relief = GROOVE)
thumbsUpButton.pack(side = LEFT)
statusThumbsDownsCount = Label(statusPosterDetailsSubFrame2, text = "", font = font1, fg = "#E83759", padx = 5, pady = 5)
statusThumbsDownsCount.pack(side = LEFT)
thumbsDownButton = Button(statusPosterDetailsSubFrame21, fg = "#E83759", activeforeground = "#E83759", font = font4, text = "-Thumbs Down", state = DISABLED, relief = GROOVE)
thumbsDownButton.pack(side = LEFT)
deleteStatusButton = Button(statusPosterDetailsSubFrame21, fg = "#B5030C", activeforeground = "#B5030C", font = font4, text = "Delete Post", state = DISABLED, relief = GROOVE)
deleteStatusButton.pack(side = LEFT)
statusPosterDetailsSubFrame3 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame3.pack(side = TOP, fill = X)
statusTextScrollBar = Scrollbar(statusPosterDetailsSubFrame3)
statusTextScrollBar.pack(side = RIGHT, fill = Y)
statusText = Text(statusPosterDetailsSubFrame3, font = font5, yscrollcommand = statusTextScrollBar.set, height = 4, state = DISABLED, wrap = WORD)
statusTextScrollBar.config(command = statusText.yview)
statusText.pack(side = LEFT, fill = X, expand = True)
commentsBufferFrame = Frame(newsFeedSlide, width = 132, relief = FLAT)
commentsBufferFrame.pack(side = LEFT, fill = Y)
commentsFrame = Frame(newsFeedSlide, relief = FLAT)
commentsFrame.pack(side = LEFT, fill = BOTH, expand = True)
commentsSubFrame1 = Frame(commentsFrame)
commentsSubFrame1.pack(side = TOP, fill = X)
commentsSubFrame2 = Frame(commentsFrame)
commentsSubFrame2.pack(side = BOTTOM, fill = X)
commentsLabel = Label(commentsSubFrame1, text = "", font = font4, justify = "left")
commentsLabel.pack(side = LEFT)
commentsScrollBar = Scrollbar(commentsFrame)
commentsScrollBar.pack(side = RIGHT, fill = Y)
commentsBox = Text(commentsFrame, font = font5, yscrollcommand = commentsScrollBar.set, height = 4, state = DISABLED, wrap = WORD)
commentsScrollBar.config(command = commentsBox.yview)
commentsBox.pack(side = LEFT, fill = BOTH, expand = True)
writeCommentBox = Entry(commentsSubFrame2, font = font2, state = DISABLED)
writeCommentBox.pack(side = LEFT, fill = X, expand = True)
submitCommentButton = Button(commentsSubFrame2, text = "Submit Comment", font = font4, fg = "#1241CE", activeforeground = "#1241CE", state = DISABLED, relief = GROOVE)
submitCommentButton.pack(side = LEFT)

def updateDisplayedStatus(index = 0):
	try:
		selectedUser = cc.getSelected()
		newsfeed = selectedUser.getNewsfeed().getStatuses()
		if newsfeed == []:
			## No newsfeed to display
			deleteStatusButton.config(state = DISABLED)
			statusPosterName.config(text = "")
			statusTimestamp.config(text = "")
			statusPosterProfilePic.config(image = selectedUser.getProfilePic(), state = DISABLED)
			statusThumbsUpsCount.config(text = "")
			statusThumbsDownsCount.config(text = "")
			statusText.config(state = NORMAL)
			statusText.delete(1.0, END)
			statusText.insert(END, "It's lonely here.\nGet friends or post your own status updates to populate your newsfeed.")
			statusText.config(state = DISABLED)
			statusBox.config(state = NORMAL)
			statusBox.delete(1.0, END)
			commentsBox.config(state = NORMAL)
			commentsBox.delete(1.0, END)
			commentsBox.config(state = DISABLED)
			nextInFeedButton.config(state = DISABLED)
			prevInFeedButton.config(state = DISABLED)
			thumbsUpButton.config(state = DISABLED)
			thumbsDownButton.config(state = DISABLED)
			selectedUser.getNewsfeed().setCurrent(0)
			return

		displayedPost = newsfeed[index]
		poster = cc.getUserById(displayedPost.getPoster())
		if poster == selectedUser:
			deleteStatusButton.config(state = NORMAL)
		else:
			deleteStatusButton.config(state = DISABLED)
		statusPosterName.config(text = poster.getUsername())
		statusTimestamp.config(text = displayedPost.getTime())
		statusPosterProfilePic.config(image = poster.getProfilePic(), state = NORMAL)
		statusThumbsUpsCount.config(text = "+" + str(len(displayedPost.getThumbsUps())) + " Thumbs Ups")
		statusThumbsDownsCount.config(text = "-" + str(len(displayedPost.getThumbsDowns())) + " Thumbs Downs")
		statusText.config(state = NORMAL)
		statusText.delete(1.0, END)
		statusBox.config(state = NORMAL)
		commentsBox.config(state = NORMAL)
		commentsBox.delete(1.0, END)
		lineNum = 1
		for comment in displayedPost.getComments():
			commenterID = comment.getPoster()
			if commenterID != selectedUser.getUserID():
				commenterName = cc.getUserById(commenterID).getUsername()
			else:
				commenterName = "You"
			commenterRange = len(commenterName) + 2
			commenterTag = str(lineNum) + "commenter"
			commentsBox.insert(END, commenterName + ": " + comment.getFText() + "\n")
			commentsBox.tag_add(commenterTag, str(lineNum) + ".0", str(lineNum) + "." + str(commenterRange))
			commentsBox.tag_config(commenterTag, foreground = "#1241CE")
			lineNum += 1
		commentsBox.config(state = DISABLED)
		nextInFeedButton.config(state = NORMAL)
		prevInFeedButton.config(state = NORMAL)
		statusBox.delete(1.0, END)
		statusText.insert(END, displayedPost.getFText())
		statusText.config(state = DISABLED)
		selectedUser.getNewsfeed().setCurrent(index)
		if index <= 0:
			prevInFeedButton.config(state = DISABLED)
		if index >= len(newsfeed) - 1:
			nextInFeedButton.config(state = DISABLED)
		if selectedUser.getUserID() in displayedPost.getThumbsUps():
			thumbsUpButton.config(state = DISABLED)
			thumbsDownButton.config(state = NORMAL)
		elif selectedUser.getUserID() in displayedPost.getThumbsDowns():
			thumbsDownButton.config(state = DISABLED)
			thumbsUpButton.config(state = NORMAL)
		else:
			thumbsUpButton.config(state = NORMAL)
			thumbsDownButton.config(state = NORMAL)
	except IndexError:
		tkMessageBox.showerror("Index out of Range","It looks like you are trying to display a status that is out of range of the current user's newsfeed.")

def nextInNewsfeed():
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex() + 1)

def prevInNewsfeed():
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex() - 1)

def submitComment(event = None):
	commentTxt = writeCommentBox.get().lstrip().rstrip().replace("\t","<tb>").replace("\n","").replace("<br>","").replace(":","<col>").replace("|","<bar>")
	if commentTxt == "":
		return
	commentPoster = cc.getSelected().getUserID()
	cc.getSelected().getNewsfeed().getCurrent().comment(commentPoster, commentTxt)
	writeCommentBox.delete(0, END)
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex())
	return

def giveThumbsUp():
	cc.getSelected().getNewsfeed().getCurrent().giveThumbsUp(cc.getSelected().getUserID())
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex())

def giveThumbsDown():
	cc.getSelected().getNewsfeed().getCurrent().giveThumbsDown(cc.getSelected().getUserID())
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex())

def postStatus(event = None):
	text = statusBox.get(1.0, END).lstrip().rstrip()
	if text == "":
		return
	poster = cc.getSelected()
	poster.addStatus(Status(text = text, poster = poster.getUserID()))
	statusBox.delete(1.0, END)
	updateAwesomesauceControls()

def deleteStatus():
	if tkMessageBox.askyesno("Delete Status - Confirm","Are you sure you want to delete this status post by you? This action cannot be undone.",default = "no") != True:
		return
	currentUser = cc.getSelected()
	try:
		currentUser.deleteStatusByValue(currentUser.getNewsfeed().getCurrent())
	except:
		tkMessageBox.showerror("Error","Could not delete the status successfully.")
	updateAwesomesauceControls()

nextInFeedButton.config(command = nextInNewsfeed)
prevInFeedButton.config(command = prevInNewsfeed)
submitCommentButton.config(command = submitComment)
writeCommentBox.bind("<Return>", submitComment)
thumbsUpButton.config(command = giveThumbsUp)
thumbsDownButton.config(command = giveThumbsDown)
postStatusButton.config(command = postStatus)
deleteStatusButton.config(command = deleteStatus)

def changefriendshipstatus():
	friendsListBoxSelectedIndices = friendsListBox.curselection()
	friendsListBoxSelectedNames = list(friendsListBox.get(int(x)) for x in friendsListBoxSelectedIndices)
	selectedUser = cc.getSelected()
	selectedUserFriends = selectedUser.getFriends()
	friendsListBoxSelectedObjs = list()
	for name in friendsListBoxSelectedNames:
		for friend in selectedUserFriends:
			if cc.getUserById(friend.getFriendID()).getUsername() == name:
				friendsListBoxSelectedObjs.append(friend)
				break
	editwin = FriendshipEditWindow(selectedUser, friendsListBoxSelectedObjs, cc, updateAwesomesauceControls)
	del editwin

def unfriend():
	friendsListBoxSelectedIndices = friendsListBox.curselection()
	friendsListBoxSelectedNames = list(friendsListBox.get(int(x)) for x in friendsListBoxSelectedIndices)
	selectedUser = cc.getSelected()
	selectedUserFriends = selectedUser.getFriends()
	friendsListBoxSelectedObjs = list()
	affectedNames = list()
	for name in friendsListBoxSelectedNames:
		for friend in selectedUserFriends:
			if cc.getUserById(friend.getFriendID()).getUsername() == name:
				friendsListBoxSelectedObjs.append(friend)
				break
	commaSep = ", "
	if tkMessageBox.askyesno("Unfriend - Confirm", "Are you sure you want to unfriend the following users? \n" + commaSep.join(friendsListBoxSelectedNames), default = "no") == True:
		uid1 = selectedUser.getUserID()
		for friend in friendsListBoxSelectedObjs:
			cc.unfriendById(uid1, friend.getFriendID())
		updateAwesomesauceControls()

changeFriendshipStatusButton = Button(friendsSubFrame2, font = font4, bg = "#C0C0C0", activebackground = "#C0C0C0", fg = "#000000", activeforeground = "#000000", state = DISABLED, text = "Change Status", command = changefriendshipstatus, relief = GROOVE)
changeFriendshipStatusButton.pack(side = TOP, fill = X)
unfriendButton = Button(friendsSubFrame2, font = font4, bg = "#C0C0C0", activebackground = "#C0C0C0", fg = "#000000", activeforeground = "#000000", state = DISABLED, text = "Unfriend", command = unfriend, relief = GROOVE)
unfriendButton.pack(side = TOP, fill = X)

#newsFeedDisplay = Frame(userFrame, relief = FLAT, width = WINDOW_WIDTH - 240)
#newsFeedDisplay.pack(side=LEFT, fill=Y)

def updateAwesomesauceControls(event = None):
	## some windows must be withdrawn to avoid the Admin mixing up stuff
	## >>>>>>>>>>>>>>>>>>>> CAUTION ! >>>>>>>>>>>>>>>>>>>>>>>
	## >>>>>>>>>>>>>>>>>> Encapsulation overridden >>>>>>>>>>
	LoginWindow.loginwindow.withdraw()
	FriendshipEditWindow.box.withdraw()
	EditProfileWindow.editprofilebox.withdraw()
	FriendAddWindow.friendrequestbox.withdraw()
	ConversationWindow.box.withdraw()
	ConversationWindow.newConversationBox.withdraw()
	## >>>>>>>>>>>>>>>>>> Encapsulation overridden >>>>>>>>>>
	## >>>>>>>>>>>>>>>>>>>> END BLOCK ! >>>>>>>>>>>>>>>>>>>>>
	
	curselected = userListBox.curselection()
	if curselected != tuple():
		cc.setSelected(int(curselected[0]))

	selectedUser = cc.getSelected()
	if selectedUser == None:
		return
	userListBox.activate(selectedUser.getUserID())

	userIDBox.config(text = selectedUser.getUserID())
	nameBox.config(text = selectedUser.getUsername())
	passwordBox.config(text = selectedUser.getPassword())

	profilePicture.config(image = selectedUser.getProfilePic())
	profileName.config(text = selectedUser.getUsername())
	changeFriendshipStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Change Status")
	unfriendButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Unfriend")
	if selectedUser.isLoggedIn() == False:
		profileSubLabel1.config(text = "Log in to your account below.", font = font2, fg = "black")
		profileSubLabel2.config(text = "")
		profileSubLabel3.config(text = "")
		profileSubLabel4.config(text = "")
		profileSubLabel5.config(text = "")
		friendsListLabel.config(text = "")
		friendsListBox.delete(0, END)
		friendsListBox.config(state = DISABLED)
		nextInFeedButton.config(state = DISABLED)
		prevInFeedButton.config(state = DISABLED)
		friendshipStatusLabel.config(text = "")
		friendshipGroupLabel.config(text = "")
		friendNameLabel.config(text = "")
		statusPosterName.config(text = "")
		commentsLabel.config(text = "")
		statusTimestamp.config(text = "")
		statusPosterProfilePic.config(image = selectedUser.getProfilePic(), state = DISABLED)
		statusThumbsUpsCount.config(text = "")
		statusThumbsDownsCount.config(text = "")
		statusText.config(state = NORMAL)
		statusBox.config(state = NORMAL)
		statusText.delete(1.0, END)
		statusBox.delete(1.0, END)
		statusText.config(state = DISABLED)
		statusBox.config(state = DISABLED)
		commentsBox.config(state = NORMAL)
		commentsBox.delete(1.0, END)
		commentsBox.config(state = DISABLED)
		writeCommentBox.config(state = NORMAL)
		writeCommentBox.delete(0, END)
		writeCommentBox.config(state = DISABLED)
		submitCommentButton.config(state = DISABLED)
		thumbsUpButton.config(state = DISABLED)
		thumbsDownButton.config(state = DISABLED)
		deleteStatusButton.config(state = DISABLED)
		postStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		loginoutButton.config(text = "Log In", state=NORMAL, activebackground = "#004A7F", bg = "#004A7F")
		profileSettingsButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		addFriendButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		vewConversationsButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
	else:
		gender = selectedUser.getGender()
		profileSubLabel1.config(text = "Gender: " + gender, font = font1)
		if gender == "Male":
			profileSubLabel1.config(fg = "#007CFF")
		elif gender == "Female":
			profileSubLabel1.config(fg = "#FF006E")
		else:
			profileSubLabel1.config(fg = "#A0A0A0")
		
		separator = " // "
		profileSubLabel2.config(text = "Age: " + str(selectedUser.getAge()))
		profileSubLabel3.config(text = "Birthday: " + str(selectedUser.getBday()))
		profileSubLabel4.config(text = "Job History: " + separator.join(selectedUser.getJobHistory()))
		profileSubLabel5.config(text = "Education: " + separator.join(selectedUser.getEducationHistory()))
		friendsListLabel.config(text = "Your Friends:")
		friendNameLabel.config(text = "Hint: Select a Friend above")
		profileSettingsButton.config(state = NORMAL, bg = "#00A0EA", activebackground = "#00A0EA")
		addFriendButton.config(state = NORMAL, bg = "#00A0EA", activebackground = "#00A0EA")
		vewConversationsButton.config(state = NORMAL, bg = "#00A0EA", activebackground = "#00A0EA")
		commentsLabel.config(text = "Comments: ")
		friendshipStatusLabel.config(text = "")
		friendshipGroupLabel.config(text = "")
		friendsListBox.config(state = NORMAL)
		## clear the friend list box first
		friendsListBox.delete(0, END)
		for friend in selectedUser.getFriends():
			friendsListBox.insert(END, cc.getUserById(friend.getFriendID()).getUsername())
		loginoutButton.config(text = "Log Out", state=NORMAL, activebackground = "dark red", bg = "dark red")
		## display newsfeed
		cc.aggregateNewsfeedById(selectedUser.getUserID())
		updateDisplayedStatus(0)
		writeCommentBox.config(state = NORMAL)
		writeCommentBox.delete(0, END)
		submitCommentButton.config(state = NORMAL)
		postStatusButton.config(state = NORMAL, bg = "#215CFF", activebackground = "#215CFF")

def updateFriendshipControls(event = None):
	## get currently selected POV user
	selectedUser = cc.getSelected()
	if selectedUser == None:
		return ## extra check only
	## get currently selected friends
	curselected = friendsListBox.curselection()
	if curselected == tuple():
		return ## no point in continuing; extra check only
	separator = " // "
	## get corresponding Friendship objects
	friendsListBoxSelected = list()
	usrFriends = selectedUser.getFriends()
	for x in curselected:
		friendsListBoxSelected.append(usrFriends[int(x)])

	friendsListBoxSelected

	selectedFriendsLen = len(friendsListBoxSelected)
	changeFriendshipStatusButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Change Status")
	unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Unfriend")
	if selectedFriendsLen > 1:
		samestatuses = True
		samegroups = True
		## More than one friend is selected;
		## see if their statuses, etc. are all the same
		firstStat = friendsListBoxSelected[0].getStatus()
		firstGroup = friendsListBoxSelected[0].getGroups()
		## The statuses, etc. are all the same if they are all equal to the first one
		for x in friendsListBoxSelected:
			if x.getStatus() != firstStat:
				samestatuses = False
				break
			else:
				continue
		for x in friendsListBoxSelected:
			if x.getGroups() != firstGroup:
				samegroups = False
				break
			else:
				continue

		friendNameLabel.config(text = cc.getUserById(friendsListBoxSelected[0].getFriendID()).getUsername() + " + " + str(selectedFriendsLen-1) + " more...")
		if samestatuses == True:
			stat = friendsListBoxSelected[0].getStatus()
			friendshipStatusLabel.config(text = "Status: (All) " + stat)
			if stat == "Pending":
				changeFriendshipStatusButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Approve")
				unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Deny")
			elif stat == "Requested":
				changeFriendshipStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Awaiting Approval")
				unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Cancel Request")
		else:
			friendshipStatusLabel.config(text = "Status: (Several)")
		if samegroups == True:
			grouplist = friendsListBoxSelected[0].getGroups()
			if grouplist != list():
				groups = separator.join(grouplist)
			else:
				groups = "<None>"
			friendshipGroupLabel.config(text = "Groups: (All) " + groups)
		else:
			friendshipGroupLabel.config(text = "Groups: (Several)")
	else:
		## Only one user is selected
		grouplist = friendsListBoxSelected[0].getGroups()
		if grouplist != list():
			groups = separator.join(grouplist)
		else:
			groups = "<None>"
		friendNameLabel.config(text = cc.getUserById(friendsListBoxSelected[0].getFriendID()).getUsername())
		stat = friendsListBoxSelected[0].getStatus()
		friendshipStatusLabel.config(text = "Status: " + stat)
		friendshipGroupLabel.config(text = "Groups: " + groups)
		if stat == "Pending":
			changeFriendshipStatusButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Approve")
			unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Deny")
		elif stat == "Requested":
			changeFriendshipStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Awaiting Approval")
			unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Cancel Request")

## NOTE: WHEN CHANGING FRIENDSHIP STATUS, IGNORE [Requested] Types

## Event Bindings

userListBox.bind("<ButtonRelease-1>", updateAwesomesauceControls)
friendsListBox.bind("<ButtonRelease-1>", updateFriendshipControls)

menubar = Menu(mainWindow, tearoff=False)
usermenu = Menu(menubar, tearoff=False)
usermenu.add_command(label="New", command=registerNewUser)
usermenu.add_command(label="Edit Profile", command=editprofile)
usermenu.add_command(label="Log in/out", command=logInOut)

menubar.add_cascade(label="User", menu=usermenu)

helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="Manual")
helpmenu.add_command(label="About", command=menu_showinfobox)

menubar.add_cascade(label="Help", menu=helpmenu)

mainWindow.config(menu = menubar)
mainWindow.mainloop()

cc.saveDB()