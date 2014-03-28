from Tkinter import *
from ttk import Combobox, Notebook
from controlcenter import *
from os import startfile
from sys import platform
from subprocess import call
import tkMessageBox, tkFileDialog

from userproxy import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 600
DATABASE_FILENAME = "db.txt"
DATABASE_CONV_FILENAME ="db_conv.txt"
DATABASE_FEED_FILENAME = "db_feed.txt"
PROGRAM_VERSION = "0.9.5.4"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

font0 = ("Segoe UI", 9, "bold")
font1 = ("Segoe UI", 11, "bold")
font2 = ("Segoe UI", 11)
font21 = ("Segoe UI", 11)
font3 = ("Segoe UI", 14, "bold")
font4 = ("Segoe UI", 9)
font5 = ("Segoe UI", 11)

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
windowPanes.add(adminFrame, width=WINDOW_WIDTH*0.18)
windowPanes.add(userFrame, width=WINDOW_WIDTH*0.82)

def end():
	cc.saveDB()
	mainWindow.destroy()

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
		self.box.state("zoomed")
		self.info = dict()

		self.frame0 = Frame(self.box, relief = FLAT)
		self.frame0.pack(side = TOP)
		self.frame1 = LabelFrame(self.frame0, pady = 5, relief = FLAT)
		self.frame1.pack(side = TOP)
		self.frame2 = LabelFrame(self.frame0, pady = 5, relief = FLAT)
		self.frame2.pack(side = TOP, fill = X)
		self.frame3 = LabelFrame(self.frame0, pady = 5, relief = FLAT)
		self.frame3.pack(side = TOP, fill = X)
		self.frame35 = LabelFrame(self.frame0, pady = 5, relief = FLAT)
		self.frame35.pack(side = TOP, fill = X)
		self.frame4 = LabelFrame(self.frame0, pady = 5, relief = FLAT)
		self.frame4.pack(side = TOP, fill = X)
		self.frame5 = LabelFrame(self.frame0, pady = 5, relief = FLAT)
		self.frame5.pack(side = TOP, fill = X)
		self.frame6 = LabelFrame(self.frame0, pady = 10, relief = FLAT)
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
	ProgramInfoFrame = LabelFrame(aboutBox, text="Program Info", padx = 7, pady = 7, relief = GROOVE)
	ProgramInfoFrame.pack(side=TOP,fill=X)
	ProgramInfoLabel1 = Label(ProgramInfoFrame, text="Program Name: Tree Fort\n\nVersion: "+PROGRAM_VERSION)
	ProgramInfoLabel1.pack(side=LEFT, expand = True)
	ProgramCreditsFrame = LabelFrame(aboutBox, text="Credits", padx = 7, pady = 7, relief = GROOVE)
	ProgramCreditsFrame.pack(side=TOP,fill=X)
	ProgramCreditsLabel1 = Label(ProgramCreditsFrame, text="Copyright 2014 Vincent Paul Fiestada\nvffiestada@upd.edu.ph\n\nFarm Fresh Icons by Fat Cow Web Hosting\nfatcow.com/free-icons")
	ProgramCreditsLabel1.pack(side=LEFT, expand = True)
	aboutBox.withdraw()
	aboutBox.protocol("WM_DELETE_WINDOW", aboutBox.withdraw)

	def __init__(self):
	 	AboutWindow.aboutBox.deiconify()

class LoginWindow: ## A singleton Window class
	loginwindow = Toplevel(mainWindow, padx = 14, pady = 14)
	loginwindow.title("Log in")
	#loginwindow.maxsize(310,110)
	#loginwindow.minsize(310,110)
	loginusername = StringVar()
	loginpassword = StringVar()

	## MESSY UI STUFF! I HATE YOU TKINTER!
	loginIcon = PhotoImage(file = "img/user_login.gif")
	keyIcon = PhotoImage(file = "img/key.gif")

	frame1 = Frame(loginwindow, relief = FLAT)
	frame1.pack(side = TOP)
	loginWidgetFrame1 = LabelFrame(frame1, padx = 10, pady = 10, relief = FLAT)
	loginWidgetFrame1.pack(side = TOP, fill = X)
	loginWidgetFrame2 = LabelFrame(frame1, padx = 10, pady = 10, relief = FLAT)
	loginWidgetFrame2.pack(side = TOP, fill = X)
	loginWidgetFrame3 = LabelFrame(frame1, padx = 10, pady = 20, relief = FLAT)
	loginWidgetFrame3.pack(side = TOP, fill = X)
	loginUsernameLabelImg = Label(loginWidgetFrame1, image = loginIcon)
	loginUsernameLabelImg.pack(side = LEFT)
	loginUsernameLabelTxt = Label(loginWidgetFrame1, text = "Username: ", font=font1)
	loginUsernameLabelTxt.pack(side = LEFT)
	loginUsernameBox = Entry(loginWidgetFrame1, font=font2, textvariable = loginusername, relief = GROOVE)
	loginUsernameBox.pack(side = LEFT, fill = X)
	loginPasswordLabelImg = Label(loginWidgetFrame2, image = keyIcon)
	loginPasswordLabelImg.pack(side = LEFT)
	loginPasswordLabelTxt = Label(loginWidgetFrame2, text = "Password: ", font=font1)
	loginPasswordLabelTxt.pack(side = LEFT)
	loginPasswordBox = Entry(loginWidgetFrame2, font=font2, show = '*', textvariable = loginpassword, relief = GROOVE)
	loginPasswordBox.pack(side = LEFT, fill = X)
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
			LoginWindow.loginpassword.set("")
			LoginWindow.loginusername.set(def_input_username)

			LoginWindow.loginSubmitCredButton.bind("<ButtonRelease-1>", self.submit)
			LoginWindow.loginwindow.bind("<Return>", self.submit)

			LoginWindow.loginwindow.state("zoomed")
			LoginWindow.loginwindow.deiconify()
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

class UserProfileInfoWindow:
	currentWin = None
	def __init__(self, master, user):
		if UserProfileInfoWindow.currentWin != None:
			UserProfileInfoWindow.currentWin.destroy()
		self.selectedUser = user
		if self.selectedUser == None:
			return self.close()
		self.infoIcon = PhotoImage(file = "img/info.gif")
		self.box = Toplevel(master, padx = 14, pady = 14)
		self.box.protocol("WM_DELETE_WINDOW", self.close)
		self.box.title("About - " + self.selectedUser.getUsername())
		UserProfileInfoWindow.currentWin = self.box
		self.frame0 = Frame(self.box)
		self.frame0.pack(side = TOP, fill = BOTH, expand = True)
		self.frame1 = LabelFrame(self.frame0, padx = 5, pady = 5, relief = FLAT)
		self.frame1.pack(side = TOP)
		self.frame2 = LabelFrame(self.frame0, padx = 5, pady = 5, relief = FLAT)
		self.frame2.pack(side = TOP)

		self.icon = Label(self.frame1, image = self.infoIcon)
		self.icon.pack(side = LEFT)
		self.title = Label(self.frame1, text = "About " + self.selectedUser.getUsername(), font = font3, fg = "#3197D1")
		self.title.pack(side = LEFT)
		try:
			profilepictureobj = PhotoImage(file = self.selectedUser.getProfilePic())
		except:
			profilepictureobj = PhotoImage(file = "img/defaultpic.gif")
		self.profilePic = Label(self.frame2, image = profilepictureobj, width = 128, height = 128)
		self.profilePic.pack(side = LEFT, fill = Y, expand = True)
		self.profilePic.image = profilepictureobj
		self.profileDisplayFrame1 = Frame(self.frame2)
		self.profileDisplayFrame1.pack(side = TOP, fill=X)
		self.profileName = Label(self.profileDisplayFrame1, text=self.selectedUser.getUsername(), font = font3, padx = 5)
		self.profileName.pack(side=LEFT)
		self.profileDisplayFrame2 = Frame(self.frame2)
		self.profileDisplayFrame2.pack(side = TOP, fill=X)
		self.profileSubLabel1 = Label(self.profileDisplayFrame2, font = font2, justify=LEFT, padx = 5, pady =  0.5)
		gender = self.selectedUser.getGender()
		self.profileSubLabel1.config(text = "Gender: " + gender)
		if gender == "Male":
			self.profileSubLabel1.config(fg = "#007CFF")
		elif gender == "Female":
			self.profileSubLabel1.config(fg = "#FF006E")
		else:
			self.profileSubLabel1.config(fg = "#A0A0A0")
		self.profileSubLabel1.pack(side=LEFT)
		self.profileSubLabel2 = Label(self.profileDisplayFrame2, font = font2, justify=LEFT, padx = 5, fg = "#7F006E", text = "Age: " + str(self.selectedUser.getAge()))
		self.profileSubLabel2.pack(side=LEFT)
		self.profileSubLabel3 = Label(self.profileDisplayFrame2, font = font2, justify=LEFT, padx = 5, fg = "#21007F", text = "Birthday: " + self.selectedUser.getBday())
		self.profileSubLabel3.pack(side=LEFT)
		self.profileDisplayFrame3 = Frame(self.frame2)
		self.profileDisplayFrame3.pack(side = TOP, fill=X)
		sep = "; "
		self.profileSubLabel4 = Label(self.profileDisplayFrame3, font = font2, justify=LEFT, padx = 5, fg = "#9E2400", text = "Job History: " + sep.join(self.selectedUser.getJobHistory()))
		self.profileSubLabel4.pack(side=LEFT)
		self.profileDisplayFrame4 = Frame(self.frame2)
		self.profileDisplayFrame4.pack(side = TOP, fill=X)
		self.profileSubLabel5 = Label(self.profileDisplayFrame4, font = font2, justify=LEFT, padx = 5, fg = "#004A7F", text = "Education History: " + sep.join(self.selectedUser.getEducationHistory()))
		self.profileSubLabel5.pack(side=LEFT)


		self.open()

	def open(self):
		self.box.state("zoomed")

	def close(self):
		UserProfileInfoWindow.currentWin = None
		self.box.destroy()

class NotificationsWindow:
	currentWin = None
	def __init__(self, master, user, widgetToEdit, widgetLabel = ""):
		if NotificationsWindow.currentWin != None:
			NotificationsWindow.currentWin.state("zoomed")
			return
		self.selectedUser = user
		if self.selectedUser == None:
			return self.close()
		self.unReadCount = 0
		self.widgetToEdit = widgetToEdit
		self.widgetLabel = widgetLabel
		self.bellIcon = PhotoImage(file = "img/bell.gif")
		self.box = Toplevel(master, padx = 14, pady = 14)
		self.box.protocol("WM_DELETE_WINDOW", self.close)
		self.box.title("Notifications - " + self.selectedUser.getUsername())
		NotificationsWindow.currentWin = self.box
		self.frame0 = Frame(self.box)
		self.frame0.pack(side = TOP, fill = BOTH, expand = True)
		self.frame1 = LabelFrame(self.frame0, padx = 5, pady = 5, relief = FLAT)
		self.frame1.pack(side = TOP)
		self.hint = Label(self.frame0, text = "(Click on a notification to mark it as read and discard it.)", font = font4)
		self.hint.pack(side = TOP)
		self.listbox = Listbox(self.frame0, relief = GROOVE, font = font2, selectmode = SINGLE, selectbackground = "#D5700A", selectforeground = "#FFFFFF")
		self.listbox.pack(side = TOP, fill = BOTH, expand = True)
		self.yscrollbar = Scrollbar(self.listbox, orient = VERTICAL, command = self.listbox.yview)
		self.yscrollbar.pack(side = RIGHT, fill = Y)
		self.xscrollbar = Scrollbar(self.listbox, orient = HORIZONTAL, command = self.listbox.xview)
		self.xscrollbar.pack(side = BOTTOM, fill = X)
		self.listbox.config(yscrollcommand = self.yscrollbar.set, xscrollcommand = self.xscrollbar.set)

		self.icon = Label(self.frame1, image = self.bellIcon)
		self.icon.pack(side = LEFT)
		self.title = Label(self.frame1, text = self.selectedUser.getUsername() + ": Notifications", font = font3, fg = "#D5700A")
		self.title.pack(side = LEFT)
		self.showedNotifs = list()
		for x in reversed(list(x for x in self.selectedUser.getNotifications() if not x.isRead())):
			self.listbox.insert(END, x.getDescription())
			self.showedNotifs.append(x)
			self.unReadCount += 1

		self.listbox.bind("<ButtonRelease-1>", self.changeSelectedNotification)

		self.selectedNotif = None
		self.open()

	def changeSelectedNotification(self, event = None):
		try:
			self.selectedNotif = self.showedNotifs[int(self.listbox.curselection()[0])]
		except:
			return
		self.selectedNotif.markRead()
		self.unReadCount -= 1

	def open(self):
		self.box.state("zoomed")

	def close(self):
		NotificationsWindow.currentWin = None
		self.box.destroy()
		self.widgetToEdit.config(text = self.widgetLabel + " [" + str(self.unReadCount) + "]")

class ConversationWindow:
	messageIcon = PhotoImage(file = "img/message.gif")
	box = Toplevel(mainWindow, padx = 14, pady = 14)
	box.title("Conversations")
	frame0 = Frame(box)
	frame0.pack(side = TOP)
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
	panes.add(conversationListPane, width = (1000-28)*0.3)
	panes.add(conversationDetailsPane, width = (1000-28)*0.7)
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
	messagesDisplayFrame.pack(side = BOTTOM, fill = BOTH, expand = True)
	messagesScrollBar = Scrollbar(messagesDisplayFrame)
	messagesScrollBar.pack(side = RIGHT, fill = Y)
	messagesDisplay = Text(messagesDisplayFrame, bg="#ffffff", yscrollcommand = messagesScrollBar.set, state = DISABLED, font = font5, wrap = WORD)
	messagesDisplay.pack(side = TOP, fill = BOTH, expand = True)
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
		ConversationWindow.box.state("zoomed")
		ConversationWindow.box.deiconify()
		ConversationWindow.box.protocol("WM_DELETE_WINDOW", self.close)
		ConversationWindow.newConversationBox.protocol("WM_DELETE_WINDOW", self.closeNewConvBox)
		ConversationWindow.deleteMessagesBox.protocol("WM_DELETE_WINDOW", self.closeDelMsgBox)
		ConversationWindow.title.config(text = self.selectedUser.getUsername() + ": Conversations")
		ConversationWindow.box.title("Conversations - " + self.selectedUser.getUsername())
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
		if list(f for f in self.selectedUser.getFriends() if  f.getStatus() not in ["Requested", "Pending", "Blocked"]) != list():
			ConversationWindow.newConversationButton.config(state = NORMAL)
		else:
			ConversationWindow.newConversationButton.config(state = DISABLED)
		ConversationWindow.newConversationBoxSubmitButton.bind("<ButtonRelease-1>", self.addConversation)
		ConversationWindow.newConversationBox.bind("<Return>", self.addConversation)
		ConversationWindow.deleteMessagesBoxSubmitButton.bind("<ButtonRelease-1>", self.deleteMessages)
		ConversationWindow.deleteMessagesBox.bind("<Return>", self.deleteMessages)
		ConversationWindow.inviteFriendButton.config(command = self.showInviteFriendsBox)
		ConversationWindow.deleteMessagesButton.config(command = self.showDeleteMessagesBox, state = DISABLED)

	def closeNewConvBox(self, event = None):
		ConversationWindow.newConversationBox.withdraw()
		ConversationWindow.box.deiconify()

	def closeDelMsgBox(self, event = None):
		ConversationWindow.deleteMessagesBox.withdraw()
		ConversationWindow.box.deiconify()
	
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
		ConversationWindow.inviteFriendButton.config(state = NORMAL)
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
			self.linkedCC.sendMessageByConversation(senderID = self.selectedUser.getUserID(), conversationObject = self.selectedConversation, text = msg)
		ConversationWindow.newMessageText.set("")
		self.updateMessageDisplay()

	def showNewConversationBox(self, event = None):
		ConversationWindow.newConversationBox.title("New Conversation")
		ConversationWindow.newConversationBoxSubmitButton.bind("<ButtonRelease-1>", self.addConversation)
		ConversationWindow.newConversationMembersListBox.delete(0, END)
		for friend in self.selectedUser.getFriends():
			if friend.getStatus() not in ["Requested", "Pending", "Blocked"]:
				ConversationWindow.newConversationMembersListBox.insert(END, self.linkedCC.getUserById(friend.getFriendID()).getUsername())
		if ConversationWindow.newConversationMembersListBox.get(0, END) != ():
			ConversationWindow.newConversationBox.deiconify()
		else:
			tkMessageBox.showinfo("No friends to add", "You have no friends that can be invited to a new conversation. Friends that are [Requested], [Pending], or [Blocked] cannot be invited to your conversation.")
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
			if friendID not in alreadyMembers and friend.getStatus() not in ["Requested", "Pending", "Blocked"]:
				ConversationWindow.newConversationMembersListBox.insert(END, self.linkedCC.getUserById(friendID).getUsername())
		if ConversationWindow.newConversationMembersListBox.get(0, END) != ():
			ConversationWindow.newConversationBox.deiconify()
		else:
			tkMessageBox.showinfo("No friends left to add", "You no longer have any other friends to invite to this conversation. Friends that are [Requested], [Pending], or [Blocked] cannot be invited to your conversation.")
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
	username = StringVar()
	friendrequestbox.protocol("WM_DELETE_WINDOW", friendrequestbox.withdraw)

	frame0 = Frame(friendrequestbox, relief = FLAT)
	frame0.pack(side = TOP)
	frame1 = LabelFrame(frame0, padx = 10, pady = 10, relief = FLAT)
	frame1.pack(side = TOP)
	frame2 = LabelFrame(frame0, padx = 10, pady = 10, relief = FLAT)
	frame2.pack(side = TOP, fill = X)
	frame3 = LabelFrame(frame0, padx = 10, pady = 10, relief = FLAT)
	frame3.pack(side = BOTTOM, fill = X)
	plusImg = Label(frame1, image = plusIcon)
	plusImg.pack(side = LEFT)
	addFriendTitle = Label(frame1, text = "Add a Friend", font = font3, padx = 5, fg = "#FF4263")
	addFriendTitle.pack(side = LEFT)
	usernameLabelImg = Label(frame2, image = unameIcon)
	usernameLabelImg.pack(side = LEFT)
	usernameLabelTxt = Label(frame2, text = "Username: ", font=font1)
	usernameLabelTxt.pack(side = LEFT)
	usernameBox = Entry(frame2, font=font2, relief = GROOVE, textvariable = username, width = 40)
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
		FriendAddWindow.friendrequestbox.title("Add a Friend - " + usr.getUsername())
		FriendAddWindow.addFriendTitle.config(text = usr.getUsername() + ": Add Friend")
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
	editprofilebox.title("Edit Profile Information")
	profileUsername = StringVar()
	profilePassword = StringVar()
	editprofilebox.protocol("WM_DELETE_WINDOW", editprofilebox.withdraw)
	maleIcon = PhotoImage(file = "img/male.gif")
	femaleIcon = PhotoImage(file = "img/female.gif")
	calendarIcon = PhotoImage(file = "img/calendar.gif")

	editprofileboxFrame0 = Frame(editprofilebox)
	editprofileboxFrame0.pack(side = TOP)
	editprofileboxFrame1 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame1.pack(side = TOP)
	editprofileboxFrame2 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame2.pack(side = TOP, fill = X)
	editprofileboxFrame20 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame20.pack(side = TOP, fill = X)
	editprofileboxFrame21 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame21.pack(side = TOP, fill = X)
	editprofileboxFrame22 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame22.pack(side = TOP, fill = X)
	editprofileboxFrame23 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame23.pack(side = TOP, fill = X)
	editprofileboxFrame241 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame241.pack(side = TOP, fill = X)
	editprofileboxFrame242 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame242.pack(side = TOP, fill = X)
	editprofileboxFrame251 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame251.pack(side = TOP, fill = X)
	editprofileboxFrame252 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 5)
	editprofileboxFrame252.pack(side = TOP, fill = X)
	editprofileboxFrame3 = LabelFrame(editprofileboxFrame0, relief = FLAT, pady = 20)
	editprofileboxFrame3.pack(side = BOTTOM, fill = X)
	wrenchImg = Label(editprofileboxFrame1, image = wrenchIcon)
	wrenchImg.pack(side = LEFT)
	settingsTitle = Label(editprofileboxFrame1, text = "Settings", font = font3, padx = 5, fg = "#0062A8")
	settingsTitle.pack(side = LEFT)
	usernameLabelImg = Label(editprofileboxFrame2, image = unameIcon)
	usernameLabelImg.pack(side = LEFT)
	usernameLabelTxt = Label(editprofileboxFrame2, text = "Username: ", font=font1)
	usernameLabelTxt.pack(side = LEFT)
	usernameBox = Entry(editprofileboxFrame2, font=font2, relief = GROOVE, textvariable = profileUsername)
	usernameBox.pack(side = LEFT, fill = X, expand = True)
	passwordLabelImg = Label(editprofileboxFrame20, image = keyIcon)
	passwordLabelImg.pack(side = LEFT)
	passwordLabelTxt = Label(editprofileboxFrame20, text = "Password: ", font=font1)
	passwordLabelTxt.pack(side = LEFT)
	passwordBox = Entry(editprofileboxFrame20, font=font2, relief = GROOVE, textvariable = profilePassword)
	passwordBox.pack(side = LEFT, fill = X, expand = True)
	profilepicLabelImg = Label(editprofileboxFrame21, image = photoIcon)
	profilepicLabelImg.pack(side = LEFT)
	profilepicLabelTxt = Label(editprofileboxFrame21, text = "Profile Picture: ", font=font1)
	profilepicLabelTxt.pack(side = LEFT)
	profilePicture = StringVar()
	profilepicButton = Button(editprofileboxFrame21, text = "Select File", font=font2, relief = GROOVE, fg = "#1241CE")
	profilepicButton.pack(side = LEFT)
	profilepicLabelTxt2 = Label(editprofileboxFrame21, textvariable = profilePicture, font=font4, width=50)
	profilepicLabelTxt2.pack(side = LEFT)
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
		EditProfileWindow.profilepicButton.config(command = self.getProfilepicFilename)
		EditProfileWindow.saveButton.config(command =  self.save)
		EditProfileWindow.deleteMeButton.config(command = self.DANGER_destroyUser)
		EditProfileWindow.editprofilebox.title("Edit Profile Information - " + usr.getUsername())
		EditProfileWindow.editprofilebox.state("zoomed")
		EditProfileWindow.editprofilebox.bind("<Return>", self.save)
	
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
	slidersIcon = PhotoImage(file = "img/user_edit.gif")
	personaIcon = PhotoImage(file = "img/persona.gif")
	box = Toplevel(mainWindow, padx = 14, pady = 14)
	box.title("Change Friendship Status")
	box.protocol("WM_DELETE_WINDOW", box.withdraw)
	lastsavedStatus = StringVar()

	frame0 = Frame(box)
	frame0.pack(side = TOP)
	frame1 = LabelFrame(frame0, relief = FLAT, pady = 5)
	frame1.pack(side = TOP)
	frame2 = LabelFrame(frame0, relief = FLAT, pady = 5)
	frame2.pack(side = TOP, fill = X)
	frame3 = LabelFrame(frame0, relief = FLAT, pady = 5)
	frame3.pack(side = TOP, fill = X)
	frame4 = LabelFrame(frame0, relief = FLAT, pady = 5)
	frame4.pack(side = TOP, fill = X)
	frame5 = LabelFrame(frame0, relief = FLAT, pady = 20)
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
			FriendshipEditWindow.box.title("Change Friendship Status - " + self.targetUser.getUsername())
			FriendshipEditWindow.editFriendshipTitle.config(text = self.targetUser.getUsername() + ": Change Friendship Status")
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
			if f.getStatus() != "Pending":
				f.setStatus(newstatus)
			else:
				usrID = self.targetUser.getUserID()
				for friend in self.affected:
					friend.setStatus(newstatus)
					for x in self.linkedCC.getUserById(friend.getFriendID()).getFriends():
						if x.getFriendID() == usrID:
							x.setStatus('F')
							break
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
controlBoxFrame4 = LabelFrame(adminFrame, pady = 10, relief = FLAT)
controlBoxFrame4.pack(side=TOP, fill=Y, expand = True)
autologinButton = Button(controlBoxFrame4, font = font1, text = "Auto Login", bg = "#0197D7", activebackground = "#0197D7", fg = "#000000", activeforeground = "#000000", padx = 10, relief = GROOVE, state = DISABLED)
autologinButton.pack(side = TOP, fill = X)
newUserButton = Button(controlBoxFrame4, font = font1, text = "Sign Up", bg = "#4CD701", activebackground = "#4CD701", fg = "#000000", activeforeground = "#000000", padx = 10, relief = GROOVE)
newUserButton.pack(side = TOP, fill = X)

profileDisplay = Frame(userFrame, relief = FLAT, height=128)
profileDisplay.pack(side=TOP, fill=X)
defphotofilename = "img/defaultpic.gif"
profilepicfile = PhotoImage(file = defphotofilename)
profilePicture = Label(profileDisplay, bg="#ffffff", height = 128, width=128, image=profilepicfile)
profilePicture.pack(side=LEFT)
profileDisplayFrame1 = Frame(profileDisplay)
profileDisplayFrame1.pack(side = TOP, fill=X)
profileName = Label(profileDisplayFrame1, text="Welcome to Treefort", font = font3, padx = 5)
profileName.pack(side=LEFT)
profileDisplayFrame2 = Frame(profileDisplay)
profileDisplayFrame2.pack(side = TOP, fill=X)
profileSubLabel1 = Label(profileDisplayFrame2, text="Select a user to change the point of view.", font = font2, justify=LEFT, padx = 5, pady =  0.5)
profileSubLabel1.pack(side=LEFT)
profileSubLabel2 = Label(profileDisplayFrame2, font = font2, justify=LEFT, padx = 5, fg = "#7F006E")
profileSubLabel2.pack(side=LEFT)
profileSubLabel3 = Label(profileDisplayFrame2, font = font2, justify=LEFT, padx = 5, fg = "#21007F")
profileSubLabel3.pack(side=LEFT)
profileDisplayFrame3 = Frame(profileDisplay)
profileDisplayFrame3.pack(side = TOP, fill=X)
profileSubLabel4 = Label(profileDisplayFrame3, font = font2, justify=LEFT, padx = 5, fg = "#9E2400")
profileSubLabel4.pack(side=LEFT)
profileDisplayFrame4 = Frame(profileDisplay)
profileDisplayFrame4.pack(side = TOP, fill=X)
profileSubLabel5 = Label(profileDisplayFrame4, font = font2, justify=LEFT, padx = 5, fg = "#004A7F")
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
	updateAwesomesauceControls()

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

def autoLogin():
	selectedUser = cc.getSelected()
	if selectedUser == None:
		return
	cc.loginUser(selectedUser.getUsername(), selectedUser.getPassword())
	updateAwesomesauceControls()

def viewnotifications():
	notifWindow = NotificationsWindow(mainWindow, cc.getSelected(), notificationsButton, "View Notifications")
	del notifWindow

newUserButton.config(command = registerNewUser)
autologinButton.config(command = autoLogin)

notificationsButton = Button(profileDisplayFrame3, text="View Notifications [0]", state=DISABLED, font=font2, bg="#C0C0C0", fg="#ffffff", activebackground = "#C0C0C0", activeforeground = "#ffffff", command = viewnotifications, relief = GROOVE, pady = 0)
notificationsButton.pack(side=LEFT)
addFriendButton = Button(profileDisplayFrame3, text="Add a Friend", state=DISABLED, font=font2, bg="#C0C0C0", fg="#ffffff", activebackground = "#C0C0C0", activeforeground = "#ffffff", command = addfriend, relief = GROOVE, pady = 0)
addFriendButton.pack(side=LEFT)
vewConversationsButton = Button(profileDisplayFrame3, text="View Conversations", state=DISABLED, font=font2, bg="#C0C0C0", fg="#ffffff", activebackground = "#C0C0C0", activeforeground = "#ffffff", command = viewConversations, relief = GROOVE, pady = 0)
vewConversationsButton.pack(side=LEFT)
profileSettingsButton = Button(profileDisplayFrame3, text="Edit Profile", state=DISABLED, font=font2, bg="#C0C0C0", fg="#ffffff", activebackground = "#C0C0C0", activeforeground = "#ffffff", command = editprofile, relief = GROOVE, pady = 0)
profileSettingsButton.pack(side=LEFT)
loginoutButton = Button(profileDisplayFrame3, text="Log In", font=font2, command=logInOut, bg="#004A7F", fg="white", activebackground = "#004A7F", activeforeground = "white", relief = GROOVE, pady = 0)
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
statusBox = Text(statusBoxSubFrame2, font = font2, height = 3, padx = 12, pady = 12, yscrollcommand = statusBoxScrollBar.set, state = DISABLED, wrap = WORD)
statusBox.pack(side = LEFT, fill = X, expand = True)
statusBoxScrollBar.config(command = statusBox.yview)
statusBoxSubFrame3 = Frame(statusBoxFrame, relief = FLAT)
statusBoxSubFrame3.pack(side = TOP, fill = X)
postStatusButton = Button(statusBoxSubFrame3, text = "Post", font = font1, fg = "#ffffff", activeforeground = "#ffffff", bg = "#C0C0C0", activebackground = "#C0C0C0", state = DISABLED, relief = GROOVE)
postStatusButton.pack(side = LEFT)
statusBoxTaggingHint = Label(statusBoxSubFrame3, text = "", font = font4, relief = FLAT)
statusBoxTaggingHint.pack(side = LEFT, fill = X)

explorationArea = Notebook(userFrame)
explorationArea.pack(side = TOP, fill = BOTH, expand = True)

newsFeedArea = Frame(explorationArea, relief = FLAT)

newsFeedSlide = Frame(newsFeedArea, relief = SUNKEN)
newsFeedSlide.pack(side = LEFT, fill = BOTH, expand = True)
pp = PhotoImage(file = "img/defaultpic.gif")
statusPosterDetailsSubFrame0 = Frame(newsFeedSlide)
statusPosterDetailsSubFrame0.pack(side = LEFT, fill = Y)
statusPosterProfilePic = Label(statusPosterDetailsSubFrame0, image = pp, width = 128, height = 128, pady = 2, padx = 2)
statusPosterProfilePic.pack(side = TOP)
infoIcon = PhotoImage(file = "img/info.gif")
aboutPosterButton = Button(statusPosterDetailsSubFrame0, image = infoIcon, relief = GROOVE, bg = "#82B8FF", activebackground = "#82B8FF")
aboutPosterButton.pack(side = TOP, fill = X)
statusPosterDetailsFrame = Frame(newsFeedSlide)
statusPosterDetailsFrame.pack(side = TOP, fill = X)
statusPosterDetailsSubFrame1 = Frame(statusPosterDetailsFrame)
statusPosterDetailsSubFrame1.pack(side = TOP, fill = X)
statusPosterName = Label(statusPosterDetailsSubFrame1, text = "", font = font2, padx = 2)
statusPosterName.pack(side = LEFT)
statusTimestamp = Label(statusPosterDetailsSubFrame1, text = "", font = font2, fg = "#1742B7", padx = 2)
statusTimestamp.pack(side = LEFT)
statusPosterDetailsSubFrame2 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame2.pack(side = TOP, fill = X)
statusPosterDetailsSubFrame21 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame21.pack(side = TOP, fill = X)
statusThumbsUpsCount = Label(statusPosterDetailsSubFrame1, text = "", font = font2, fg = "#32B71B", padx = 2, pady = 2)
statusThumbsUpsCount.pack(side = LEFT)
nextIcon = PhotoImage(file = "img/next.gif")
prevIcon = PhotoImage(file = "img/prev.gif")
nextInFeedButton = Button(statusPosterDetailsSubFrame1, image = nextIcon, state = DISABLED, relief = GROOVE)
prevInFeedButton = Button(statusPosterDetailsSubFrame1, image = prevIcon, state = DISABLED, relief = GROOVE)
nextInFeedButton.pack(side = RIGHT)
prevInFeedButton.pack(side = RIGHT)
thumbsUpButton = Button(statusPosterDetailsSubFrame21, fg = "#32B71B", font = font4, activeforeground = "#32B71B", text = "+Thumbs Up", state = DISABLED, relief = GROOVE)
thumbsUpButton.pack(side = LEFT)
statusThumbsDownsCount = Label(statusPosterDetailsSubFrame1, text = "", font = font2, fg = "#E83759", padx = 2, pady = 2)
statusThumbsDownsCount.pack(side = LEFT)
thumbsDownButton = Button(statusPosterDetailsSubFrame21, fg = "#E83759", activeforeground = "#E83759", font = font4, text = "-Thumbs Down", state = DISABLED, relief = GROOVE)
thumbsDownButton.pack(side = LEFT)
deleteStatusButton = Button(statusPosterDetailsSubFrame21, fg = "#B5030C", activeforeground = "#B5030C", font = font4, text = "Delete Post", state = DISABLED, relief = GROOVE)
deleteStatusButton.pack(side = LEFT)
statusPosterDetailsSubFrame3 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame3.pack(side = TOP, fill = X)
statusPosterDetailsSubFrame31 = Frame(statusPosterDetailsFrame, relief = FLAT)
statusPosterDetailsSubFrame31.pack(side = TOP, fill = X)
statusTextScrollBar = Scrollbar(statusPosterDetailsSubFrame3)
statusTextScrollBar.pack(side = RIGHT, fill = Y)
statusText = Text(statusPosterDetailsSubFrame3, font = font5, yscrollcommand = statusTextScrollBar.set, height = 4, state = DISABLED, wrap = WORD, padx = 12, pady = 12)
statusTextScrollBar.config(command = statusText.yview)
statusText.pack(side = LEFT, fill = X, expand = True)
statusTaggedDisplay = Label(statusPosterDetailsSubFrame31, text = "", font = font4, pady = 2, fg = "#1241CE", relief = FLAT)
statusTaggedDisplay.pack(side = LEFT, fill = X)
commentsFrame = Frame(newsFeedSlide, relief = FLAT)
commentsFrame.pack(side = LEFT, fill = BOTH, expand = True)
commentsSubFrame1 = Frame(commentsFrame)
commentsSubFrame1.pack(side = TOP, fill = X)
commentsSubFrame2 = Frame(commentsFrame)
commentsSubFrame2.pack(side = BOTTOM, fill = X)
commentsLabel = Label(commentsSubFrame1, font = font4, justify = "left", text = "Comment: ")
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

timelinesArea = Frame(explorationArea, relief = FLAT)

timelineSlide = Frame(timelinesArea, relief = SUNKEN)
timelineSlide.pack(side = TOP, fill = BOTH, expand = True)
timelinestatusPosterDetailsSubFrame0 = Frame(timelineSlide)
timelinestatusPosterDetailsSubFrame0.pack(side = LEFT, fill = Y)
timelinestatusPosterProfilePic = Label(timelinestatusPosterDetailsSubFrame0, image = None, width = 128, height = 128, pady = 2, padx = 2)
timelinestatusPosterProfilePic.pack(side = TOP)
timelineaboutPosterButton = Button(timelinestatusPosterDetailsSubFrame0, relief = GROOVE, bg = "#82B8FF", activebackground = "#82B8FF", image = infoIcon)
timelineaboutPosterButton.pack(side = TOP, fill = X)
timelinestatusPosterDetailsFrame = Frame(timelineSlide)
timelinestatusPosterDetailsFrame.pack(side = TOP, fill = X)
timelinestatusPosterDetailsSubFrame1 = Frame(timelinestatusPosterDetailsFrame)
timelinestatusPosterDetailsSubFrame1.pack(side = TOP, fill = X)
timelinestatusPosterName = Combobox(timelinestatusPosterDetailsSubFrame1, text = "", font = font2, state = "readonly")
timelinestatusPosterName.pack(side = LEFT)
timelinestatusTimestamp = Label(timelinestatusPosterDetailsSubFrame1, text = "", font = font2, fg = "#1742B7", padx = 2)
timelinestatusTimestamp.pack(side = LEFT)
timelinestatusPosterDetailsSubFrame2 = Frame(timelinestatusPosterDetailsFrame, relief = FLAT)
timelinestatusPosterDetailsSubFrame2.pack(side = TOP, fill = X)
timelinestatusPosterDetailsSubFrame21 = Frame(timelinestatusPosterDetailsFrame, relief = FLAT)
timelinestatusPosterDetailsSubFrame21.pack(side = TOP, fill = X)
timelinestatusThumbsUpsCount = Label(timelinestatusPosterDetailsSubFrame1, text = "", font = font2, fg = "#32B71B", padx = 2, pady = 2)
timelinestatusThumbsUpsCount.pack(side = LEFT)
timelinenextInFeedButton = Button(timelinestatusPosterDetailsSubFrame1, image = nextIcon, state = DISABLED, relief = GROOVE)
timelineprevInFeedButton = Button(timelinestatusPosterDetailsSubFrame1, image = prevIcon, state = DISABLED, relief = GROOVE)
timelinenextInFeedButton.pack(side = RIGHT)
timelineprevInFeedButton.pack(side = RIGHT)
timelinethumbsUpButton = Button(timelinestatusPosterDetailsSubFrame21, fg = "#32B71B", font = font4, activeforeground = "#32B71B", text = "+Thumbs Up", state = DISABLED, relief = GROOVE)
timelinethumbsUpButton.pack(side = LEFT)
timelinestatusThumbsDownsCount = Label(timelinestatusPosterDetailsSubFrame1, text = "", font = font2, fg = "#E83759", padx = 2, pady = 2)
timelinestatusThumbsDownsCount.pack(side = LEFT)
timelinethumbsDownButton = Button(timelinestatusPosterDetailsSubFrame21, fg = "#E83759", activeforeground = "#E83759", font = font4, text = "-Thumbs Down", state = DISABLED, relief = GROOVE)
timelinethumbsDownButton.pack(side = LEFT)
timelinedeleteStatusButton = Button(timelinestatusPosterDetailsSubFrame21, fg = "#B5030C", activeforeground = "#B5030C", font = font4, text = "Delete Post", state = DISABLED, relief = GROOVE)
timelinedeleteStatusButton.pack(side = LEFT)
timelinestatusPosterDetailsSubFrame3 = Frame(timelinestatusPosterDetailsFrame, relief = FLAT)
timelinestatusPosterDetailsSubFrame3.pack(side = TOP, fill = X)
timelinestatusPosterDetailsSubFrame31 = Frame(timelinestatusPosterDetailsFrame, relief = FLAT)
timelinestatusPosterDetailsSubFrame31.pack(side = TOP, fill = X)
timelinestatusTextScrollBar = Scrollbar(timelinestatusPosterDetailsSubFrame3)
timelinestatusTextScrollBar.pack(side = RIGHT, fill = Y)
timelinestatusText = Text(timelinestatusPosterDetailsSubFrame3, font = font5, yscrollcommand = timelinestatusTextScrollBar.set, height = 4, state = DISABLED, wrap = WORD, padx = 12, pady = 12)
timelinestatusTextScrollBar.config(command = timelinestatusText.yview)
timelinestatusText.pack(side = LEFT, fill = X, expand = True)
timelinestatusTaggedDisplay = Label(timelinestatusPosterDetailsSubFrame31, text = "", font = font4, pady = 2, fg = "#1241CE", relief = FLAT)
timelinestatusTaggedDisplay.pack(side = LEFT, fill = X)
timelinecommentsFrame = Frame(timelineSlide, relief = FLAT)
timelinecommentsFrame.pack(side = LEFT, fill = BOTH, expand = True)
timelinecommentsSubFrame1 = Frame(timelinecommentsFrame)
timelinecommentsSubFrame1.pack(side = TOP, fill = X)
timelinecommentsSubFrame2 = Frame(timelinecommentsFrame)
timelinecommentsSubFrame2.pack(side = BOTTOM, fill = X)
timelinecommentsLabel = Label(timelinecommentsSubFrame1, font = font4, justify = "left", text = "Comments: ")
timelinecommentsLabel.pack(side = LEFT)
timelinecommentsScrollBar = Scrollbar(timelinecommentsFrame)
timelinecommentsScrollBar.pack(side = RIGHT, fill = Y)
timelinecommentsBox = Text(timelinecommentsFrame, font = font5, yscrollcommand = timelinecommentsScrollBar.set, height = 4, state = DISABLED, wrap = WORD)
timelinecommentsScrollBar.config(command = timelinecommentsBox.yview)
timelinecommentsBox.pack(side = LEFT, fill = BOTH, expand = True)
timelinewriteCommentBox = Entry(timelinecommentsSubFrame2, font = font2, state = DISABLED)
timelinewriteCommentBox.pack(side = LEFT, fill = X, expand = True)
timelinesubmitCommentButton = Button(timelinecommentsSubFrame2, text = "Submit Comment", font = font4, fg = "#1241CE", activeforeground = "#1241CE", state = DISABLED, relief = GROOVE)
timelinesubmitCommentButton.pack(side = LEFT)

feedicon = PhotoImage(file = "img/feed.gif")
timelineicon = PhotoImage(file = "img/timeline.gif")
explorationArea.add(newsFeedArea, text = "News Feed", image = feedicon, compound = LEFT, state = DISABLED)
explorationArea.add(timelinesArea, text = "Timelines", image = timelineicon, compound = LEFT, state = DISABLED)

def updateDisplayedStatus(index = 0):
	try:
		selectedUser = cc.getSelected()
		newsfeed = selectedUser.getNewsfeed().getStatuses()
		if newsfeed == []:
			## No newsfeed to display
			deleteStatusButton.config(state = DISABLED)
			statusPosterName.config(text = "")
			statusTimestamp.config(text = "")
			try:
				profilepictureobj = PhotoImage(file = selectedUser.getProfilePic())
			except:
				profilepictureobj = PhotoImage(file = "img/defaultpic.gif")
			statusPosterProfilePic.config(image = PhotoImage(file = profilepictureobj), state = DISABLED)
			statusPosterProfilePic.image = profilepictureobj
			statusThumbsUpsCount.config(text = "")
			statusThumbsDownsCount.config(text = "")
			statusTaggedDisplay.config(text = "")
			statusText.config(state = NORMAL)
			statusText.delete(1.0, END)
			statusText.insert(END, "It's lonely here.\nGet friends or post your own status updates to populate your newsfeed.")
			statusText.config(state = DISABLED)
			statusBox.config(state = NORMAL)
			statusBox.delete(1.0, END)
			commentsBox.config(state = NORMAL)
			commentsBox.delete(1.0, END)
			commentsBox.config(state = DISABLED)
			writeCommentBox.config(state = NORMAL)
			writeCommentBox.delete(0, END)
			writeCommentBox.config(state = DISABLED)
			submitCommentButton.config(state = DISABLED)
			nextInFeedButton.config(state = DISABLED)
			prevInFeedButton.config(state = DISABLED)
			thumbsUpButton.config(state = DISABLED)
			thumbsDownButton.config(state = DISABLED)
			selectedUser.getNewsfeed().setCurrent(0)
			aboutPosterButton.config(state = DISABLED)
			return
		
		displayedPost = newsfeed[index]

		poster = cc.getUserById(displayedPost.getPoster())
		if poster == selectedUser:
			deleteStatusButton.config(state = NORMAL)
		else:
			deleteStatusButton.config(state = DISABLED)
		statusPosterName.config(text = poster.getUsername())
		statusTimestamp.config(text = displayedPost.getTime())
		try:
			profilepictureobj = PhotoImage(file = poster.getProfilePic())
		except:
			profilepictureobj = PhotoImage(file = "img/defaultpic.gif")
		statusPosterProfilePic.config(image = profilepictureobj, state = NORMAL)
		statusPosterProfilePic.image = profilepictureobj
		aboutPosterButton.config(state = NORMAL)
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
		writeCommentBox.config(state = NORMAL)
		writeCommentBox.delete(0, END)
		submitCommentButton.config(state = NORMAL)
		nextInFeedButton.config(state = NORMAL)
		prevInFeedButton.config(state = NORMAL)
		statusBox.delete(1.0, END)
		statusText.insert(END, displayedPost.getFText())
		smcolsep = "; "
		taggedNames = list(cc.getUserById(x).getUsername() for x in displayedPost.getTags())
		taggedNamesLen = len(taggedNames)
		if taggedNamesLen <= 5:
			taggedList = smcolsep.join(taggedNames)
		else:
			taggedList = taggedNames[0] + " and " + str(taggedNamesLen-1) + " more..."
		if taggedList == "":
			statusTaggedDisplay.config(text = "No one is tagged")
		else:
			statusTaggedDisplay.config(text = "Tagged: " + taggedList)
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
	except:
		tkMessageBox.showerror("Epic Fail","That doesn't bode well. There was an unknown error and the status cannot be displayed.")

def updateDisplayedTimelineStatus(event = None, index = 0, user = None):
	try:
		if user == None:
			poster = cc.getUserByName(timelinestatusPosterName.get())
		else:
			poster = cc.getUserById(user)
		newsfeed = poster.getStatuses()
		selectedUser = cc.getSelected()
		cc.getSelected().settimeLineSelectedIndex(index)
		cc.getSelected().settimeLineSelectedFriend(poster.getUserID())
		if newsfeed == []:
			## No newsfeed to display
			timelinedeleteStatusButton.config(state = DISABLED)
			timelinestatusPosterName.config(text = "")
			timelinestatusTimestamp.config(text = "")
			try:
				profilepictureobj = PhotoImage(file = poster.getProfilePic())
			except:
				profilepictureobj = PhotoImage(file = "img/defaultpic.gif")
			timelinestatusPosterProfilePic.config(image = profilepictureobj, state = DISABLED)
			timelinestatusPosterProfilePic.image = profilepictureobj
			timelinestatusThumbsUpsCount.config(text = "")
			timelinestatusThumbsDownsCount.config(text = "")
			timelinestatusTaggedDisplay.config(text = "")
			timelinestatusText.config(state = NORMAL)
			timelinestatusText.delete(1.0, END)
			timelinestatusText.insert(END, "It's lonely here.\n"+poster.getUsername()+" hasn't posted any status updates")
			timelinestatusText.config(state = DISABLED)
			timelinecommentsBox.config(state = NORMAL)
			timelinecommentsBox.delete(1.0, END)
			timelinecommentsBox.config(state = DISABLED)
			timelinewriteCommentBox.config(state = NORMAL)
			timelinewriteCommentBox.delete(0, END)
			timelinewriteCommentBox.config(state = DISABLED)
			timelinesubmitCommentButton.config(state = DISABLED)
			timelinenextInFeedButton.config(state = DISABLED)
			timelineprevInFeedButton.config(state = DISABLED)
			timelinethumbsUpButton.config(state = DISABLED)
			timelinethumbsDownButton.config(state = DISABLED)
			poster.getNewsfeed().setCurrent(0)
			timelinestatusPosterName.set(poster.getUsername())
			return

		displayedPost = newsfeed[index]
		if poster == selectedUser:
			timelinedeleteStatusButton.config(state = NORMAL)
		else:
			timelinedeleteStatusButton.config(state = DISABLED)
		timelinestatusPosterName.config(text = poster.getUsername())
		timelinestatusTimestamp.config(text = displayedPost.getTime())
		try:
			profilepictureobj = PhotoImage(file = poster.getProfilePic())
		except:
			profilepictureobj = PhotoImage(file = "img/defaultpic.gif")
		timelinestatusPosterProfilePic.config(image = profilepictureobj, state = NORMAL)
		timelinestatusPosterProfilePic.image = profilepictureobj
		timelinestatusThumbsUpsCount.config(text = "+" + str(len(displayedPost.getThumbsUps())) + " Thumbs Ups")
		timelinestatusThumbsDownsCount.config(text = "-" + str(len(displayedPost.getThumbsDowns())) + " Thumbs Downs")
		timelinestatusText.config(state = NORMAL)
		timelinestatusText.delete(1.0, END)
		timelinecommentsBox.config(state = NORMAL)
		timelinecommentsBox.delete(1.0, END)
		lineNum = 1
		for comment in displayedPost.getComments():
			commenterID = comment.getPoster()
			if commenterID != poster.getUserID():
				commenterName = cc.getUserById(commenterID).getUsername()
			else:
				commenterName = "You"
			commenterRange = len(commenterName) + 2
			commenterTag = str(lineNum) + "commenter"
			timelinecommentsBox.insert(END, commenterName + ": " + comment.getFText() + "\n")
			timelinecommentsBox.tag_add(commenterTag, str(lineNum) + ".0", str(lineNum) + "." + str(commenterRange))
			timelinecommentsBox.tag_config(commenterTag, foreground = "#1241CE")
			lineNum += 1
		timelinecommentsBox.config(state = DISABLED)
		timelinewriteCommentBox.config(state = NORMAL)
		timelinewriteCommentBox.delete(0, END)
		timelinesubmitCommentButton.config(state = NORMAL)
		timelinenextInFeedButton.config(state = NORMAL)
		timelineprevInFeedButton.config(state = NORMAL)
		timelinestatusText.insert(END, displayedPost.getFText())
		smcolsep = "; "
		taggedNames = list(cc.getUserById(x).getUsername() for x in displayedPost.getTags())
		taggedNamesLen = len(taggedNames)
		if taggedNamesLen <= 5:
			taggedList = smcolsep.join(taggedNames)
		else:
			taggedList = taggedNames[0] + " and " + str(taggedNamesLen-1) + " more..."
		if taggedList == "":
			timelinestatusTaggedDisplay.config(text = "No one is tagged")
		else:
			timelinestatusTaggedDisplay.config(text = "Tagged: " + taggedList)
		timelinestatusText.config(state = DISABLED)
		if index <= 0:
			timelineprevInFeedButton.config(state = DISABLED)
		if index >= len(newsfeed) - 1:
			timelinenextInFeedButton.config(state = DISABLED)
		if selectedUser.getUserID() in displayedPost.getThumbsUps():
			timelinethumbsUpButton.config(state = DISABLED)
			timelinethumbsDownButton.config(state = NORMAL)
		elif selectedUser.getUserID() in displayedPost.getThumbsDowns():
			timelinethumbsDownButton.config(state = DISABLED)
			timelinethumbsUpButton.config(state = NORMAL)
		else:
			timelinethumbsUpButton.config(state = NORMAL)
			timelinethumbsDownButton.config(state = NORMAL)
		timelinestatusPosterName.set(poster.getUsername())
	except IndexError:
		tkMessageBox.showerror("Index out of Range","It looks like you are trying to display a status that is out of range of the current user's timeline.")
	except:
		tkMessageBox.showerror("Epic Fail","That doesn't bode well. There was an unknown error and the status cannot be displayed.")

def nextInTimeline():
	updateDisplayedTimelineStatus(index = cc.getSelected().gettimeLineSelectedIndex() + 1, user = cc.getSelected().gettimeLineSelectedFriend())

def prevInTimeline():
	updateDisplayedTimelineStatus(index = cc.getSelected().gettimeLineSelectedIndex() - 1, user = cc.getSelected().gettimeLineSelectedFriend())

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

def submitTimelineComment(event = None):
	commentTxt = timelinewriteCommentBox.get().lstrip().rstrip().replace("\t","<tb>").replace("\n","").replace("<br>","").replace(":","<col>").replace("|","<bar>")
	if commentTxt == "":
		return
	commentPoster = cc.getSelected().getUserID()
	cc.getUserById(cc.getSelected().gettimeLineSelectedFriend()).getStatuses()[cc.getSelected().gettimeLineSelectedIndex()].comment(commentPoster, commentTxt)
	timelinewriteCommentBox.delete(0, END)
	updateDisplayedTimelineStatus(index = cc.getSelected().gettimeLineSelectedIndex(), user = cc.getSelected().gettimeLineSelectedFriend())
	return

def giveThumbsUp():
	cc.getSelected().getNewsfeed().getCurrent().giveThumbsUp(cc.getSelected().getUserID())
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex())

def giveThumbsDown():
	cc.getSelected().getNewsfeed().getCurrent().giveThumbsDown(cc.getSelected().getUserID())
	updateDisplayedStatus(cc.getSelected().getNewsfeed().getCurrentIndex())

def giveTimelineThumbsUp():
	cc.getUserById(cc.getSelected().gettimeLineSelectedFriend()).getStatuses()[cc.getSelected().gettimeLineSelectedIndex()].giveThumbsUp(cc.getSelected().getUserID())
	updateDisplayedTimelineStatus(index = cc.getSelected().gettimeLineSelectedIndex())

def giveTimelineThumbsDown():
	cc.getUserById(cc.getSelected().gettimeLineSelectedFriend()).getStatuses()[cc.getSelected().gettimeLineSelectedIndex()].giveThumbsDown(cc.getSelected().getUserID())
	updateDisplayedTimelineStatus(index = cc.getSelected().gettimeLineSelectedIndex())

def postStatus(event = None):
	text = statusBox.get(1.0, END).lstrip().rstrip()
	if text == "":
		return
	poster = cc.getSelected()
	if poster == None:
		return
	cc.addStatusById(cc.getSelected().getUserID(), text)
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

def deleteTimelineStatus():
	if tkMessageBox.askyesno("Delete Status - Confirm","Are you sure you want to delete this status post by you? This action cannot be undone.",default = "no") != True:
		return
	currentUser = cc.getSelected()
	try:
		currentUser.deleteStatusByValue(currentUser.getStatuses()[currentUser.gettimeLineSelectedIndex()])
	except:
		tkMessageBox.showerror("Error","Could not delete the status successfully.")
	updateAwesomesauceControls()

def aboutUserInfo():
	UserProfileInfoWindow(mainWindow, cc.getUserById(cc.getSelected().getNewsfeed().getCurrent().getPoster()))

def aboutTimelineUserInfo():
	UserProfileInfoWindow(mainWindow, cc.getUserById(cc.getSelected().gettimeLineSelectedFriend()))

nextInFeedButton.config(command = nextInNewsfeed)
prevInFeedButton.config(command = prevInNewsfeed)
timelinenextInFeedButton.config(command = nextInTimeline)
timelineprevInFeedButton.config(command = prevInTimeline)
submitCommentButton.config(command = submitComment)
writeCommentBox.bind("<Return>", submitComment)
thumbsUpButton.config(command = giveThumbsUp)
thumbsDownButton.config(command = giveThumbsDown)
postStatusButton.config(command = postStatus)
deleteStatusButton.config(command = deleteStatus)
timelinestatusPosterName.bind("<<ComboboxSelected>>", updateDisplayedTimelineStatus)
timelinewriteCommentBox.bind("<Return>", submitTimelineComment)
timelinethumbsUpButton.config(command = giveTimelineThumbsUp)
timelinethumbsDownButton.config(command = giveTimelineThumbsDown)
timelinedeleteStatusButton.config(command = deleteTimelineStatus)
aboutPosterButton.config(command = aboutUserInfo)
timelineaboutPosterButton.config(command = aboutTimelineUserInfo)

def changefriendshipstatus():
	friendsListBoxSelectedIndices = friendsListBox.curselection()
	friendsListBoxSelectedNames = list(friendsListBox.get(int(x)) for x in friendsListBoxSelectedIndices)
	selectedUser = cc.getSelected()
	selectedUserFriends = selectedUser.getFriends()
	friendsListBoxSelectedObjs = list()
	for name in friendsListBoxSelectedNames:
		for friend in selectedUserFriends:
			if cc.getUserById(friend.getFriendID()).getUsername() == name:
				if friend.getStatus() != "Requested":
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
	## some windows must be withdrawn to avoid the Admin's confusion and mixing up stuff
	## >>>>>>>>>>>>>>>>>>>> CAUTION ! >>>>>>>>>>>>>>>>>>>>>>>
	## >>>>>>>>>>>>>>>>>> Encapsulation overridden >>>>>>>>>>
	LoginWindow.loginwindow.withdraw()
	FriendshipEditWindow.box.withdraw()
	EditProfileWindow.editprofilebox.withdraw()
	FriendAddWindow.friendrequestbox.withdraw()
	ConversationWindow.box.withdraw()
	ConversationWindow.newConversationBox.withdraw()
	if NotificationsWindow.currentWin != None:
		NotificationsWindow.currentWin.destroy()
		NotificationsWindow.currentWin = None
	if UserProfileInfoWindow.currentWin != None:
		UserProfileInfoWindow.currentWin.destroy()
		UserProfileInfoWindow.currentWin = None
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

	try:
		profilepictureobj = PhotoImage(file = selectedUser.getProfilePic())
	except:
		profilepictureobj = PhotoImage(file = "img/defaultpic.gif")
	profilePicture.config(image = profilepictureobj)
	profilePicture.image = profilepictureobj
	profileName.config(text = selectedUser.getUsername())
	changeFriendshipStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Change Status")
	unfriendButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Unfriend")
	if selectedUser.isLoggedIn() == False:
		profileSubLabel1.config(text = "Log in to your account below.", font = font2, fg = "black")
		statusBoxTaggingHint.config(text = "")
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
		friendNameLabel.config(text = "")
		autologinButton.config(state = NORMAL)
		explorationArea.tab(0, state = DISABLED)
		explorationArea.tab(1, state = DISABLED)
		postStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		loginoutButton.config(text = "Log In", state=NORMAL, activebackground = "#004A7F", bg = "#004A7F")
		profileSettingsButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		addFriendButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		vewConversationsButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0")
		notificationsButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "View Notifications [0]")
	else:
		gender = selectedUser.getGender()
		profileSubLabel1.config(text = "Gender: " + gender)
		if gender == "Male":
			profileSubLabel1.config(fg = "#007CFF")
		elif gender == "Female":
			profileSubLabel1.config(fg = "#FF006E")
		else:
			profileSubLabel1.config(fg = "#A0A0A0")
		
		separator = "; "
		profileSubLabel2.config(text = "Age: " + str(selectedUser.getAge()))
		profileSubLabel3.config(text = "Birthday: " + str(selectedUser.getBday()))
		profileSubLabel4.config(text = "Job History: " + separator.join(selectedUser.getJobHistory()))
		profileSubLabel5.config(text = "Education: " + separator.join(selectedUser.getEducationHistory()))
		friendsListLabel.config(text = "Your Friends:")
		statusBoxTaggingHint.config(text = "(To tag a user, surround their username with asterisks. Ex. 'Hello, *Luke*')")
		friendNameLabel.config(text = "Hint: Select a Friend above")
		profileSettingsButton.config(state = NORMAL, bg = "#215CFF", activebackground = "#215CFF")
		addFriendButton.config(state = NORMAL, bg = "#215CFF", activebackground = "#215CFF")
		vewConversationsButton.config(state = NORMAL, bg = "#215CFF", activebackground = "#215CFF")
		notificationsButton.config(state = NORMAL, bg = "#215CFF", activebackground = "#215CFF", text = "View Notifications [" + str(len(list(x for x in selectedUser.getNotifications() if x.isRead() == False))) + "]")
		friendshipStatusLabel.config(text = "")
		friendsListBox.config(state = NORMAL)
		autologinButton.config(state = DISABLED)
		## clear the friend list box first
		friendsListBox.delete(0, END)
		flist = [] ## save for later use
		for friend in selectedUser.getFriends():
			fname = cc.getUserById(friend.getFriendID()).getUsername()
			friendsListBox.insert(END, fname)
			if friend.getStatus() not in ["Pending", "Requested", "Hidden Updates"]:
				flist.append(fname)
		timelinestatusPosterName.config(values = [selectedUser.getUsername()] + flist)
		timelinestatusPosterName.set(selectedUser.getUsername())
		loginoutButton.config(text = "Log Out", state=NORMAL, activebackground = "#FA6900", bg = "#FA6900")
		## display newsfeed
		cc.aggregateNewsfeedById(selectedUser.getUserID())
		updateDisplayedStatus(0)
		postStatusButton.config(state = NORMAL, bg = "#215CFF", activebackground = "#215CFF")
		explorationArea.tab(0, state = NORMAL)
		explorationArea.tab(1, state = NORMAL)
		explorationArea.select(0)
		timelinestatusPosterName.set(selectedUser.getUsername())
		updateDisplayedTimelineStatus()

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
		## The statuses, etc. are all the same if they are all equal to the first one
		for x in friendsListBoxSelected:
			if x.getStatus() != firstStat:
				samestatuses = False
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
		if stat == "Pending":
			changeFriendshipStatusButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Approve")
			unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Deny")
		elif stat == "Requested":
			changeFriendshipStatusButton.config(state = DISABLED, bg = "#C0C0C0", activebackground = "#C0C0C0", text = "Awaiting Approval")
			unfriendButton.config(state = NORMAL, bg = "#FF9B63", activebackground = "#FF9B63", text = "Cancel Request")


## Citation:
## The openManual() function below is based on an answer on StackOverflow posted by Stack Exchange user
## 'user4815162342'. It was retrieved from the page http://stackoverflow.com/questions/17317219/is-there-an-platform-independent-equivalent-of-os-startfile
## The function uses standard Python modules and has been modified here as seen appropriate

def openManual():
	filename = "docs\user_manual.pdf"
	try:
		if sys.platform == "win32":
			os.startfile(filename)
		else:
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, filename])
	except WindowsError:
		tkMessageBox.showerror("404 - Manual Not Available","The User Manual could not be opened successfully. The file might have been deleted or has been placed under restricted persmission access. You can still email the developer at vffiestada@upd.edu.ph for questions.")
	except:
		tkMessageBox.showerror("Epic Fail","The User Manual could not be opened successfully due to an unknown error. You can still email the developer at vffiestada@upd.edu.ph for questions.")

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
helpmenu.add_command(label="Manual", command = openManual)
helpmenu.add_command(label="About", command=menu_showinfobox)

menubar.add_cascade(label="Help", menu=helpmenu)

mainWindow.config(menu = menubar)
mainWindow.state("zoomed")
mainWindow.protocol("WM_DELETE_WINDOW", end)
mainWindow.mainloop()