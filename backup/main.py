from Tkinter import *
from ttk import Frame
from tkFont import Font
from controlcenter import *
import tkMessageBox

from userproxy import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 600
WINDOW_RELIEF = "sunken"
DATABASE_FILENAME = "db.txt"
PROGRAM_VERSION = "0.2.2 Alpha"

font1 = ("Helvetica", 11, "bold")
font2 = ("Helvetica", 11)
font3 = ("Helvetica", 14, "bold")

cc = IControlCenter()
cc.openDB(DATABASE_FILENAME)

mainWindow = Tk()
mainWindow.title("Tree Fort")
mainWindow.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
windowPanes = PanedWindow(mainWindow)
windowPanes.pack(fill=BOTH, expand=True)
adminFrame = Frame(windowPanes, relief=WINDOW_RELIEF)
userFrame = Frame(windowPanes, relief=WINDOW_RELIEF)
windowPanes.add(adminFrame, width=WINDOW_WIDTH*0.2)
windowPanes.add(userFrame, width=WINDOW_WIDTH*0.8)

def menu_showinfobox():
	aboutBox = Toplevel(mainWindow, padx = 14, pady = 14)
	aboutBox.title("About Tree Fort")
	aboutBox.maxsize(500,280)
	aboutBox.minsize(500,280)
	LogoImg = PhotoImage(file = "img/logo_transparent.gif")
	LogoLabel = Label(aboutBox, image = LogoImg)
	LogoLabel.pack(side=TOP,fill=X)
	ProgramInfoFrame = LabelFrame(aboutBox, text="Program Info", padx = 7, pady = 7)
	ProgramInfoFrame.pack(side=TOP,fill=X)
	ProgramInfoLabel1 = Label(ProgramInfoFrame, text="Program Name: Tree Fort\n\nVersion: "+PROGRAM_VERSION)
	ProgramInfoLabel1.pack(side=LEFT, expand = True)
	ProgramCreditsFrame = LabelFrame(aboutBox, text="Credits", padx = 7, pady = 7)
	ProgramCreditsFrame.pack(side=TOP,fill=X)
	ProgramCreditsLabel1 = Label(ProgramCreditsFrame, text="(c) 2014 Vincent Paul Fiestada")
	ProgramCreditsLabel1.pack(side=LEFT, expand = True)

	aboutBox.mainloop()

def logInOut():
	loginoutwin = LoginWindow(cc.getSelected(), cc)
	del loginoutwin

class LoginWindow: ## A singleton Window class
	isOpen = False
	## 'controlcenter' argument must be a Control Center object
	def __init__(self, selectedUser, controlcenter):
		if LoginWindow.isOpen == False:
			LoginWindow.loginwindow = Toplevel(mainWindow, padx = 14, pady = 14)
			LoginWindow.loginwindow.title("Log in")
			LoginWindow.loginwindow.maxsize(310,110)
			LoginWindow.loginwindow.minsize(310,110)
			LoginWindow.loginwindow.protocol("WM_DELETE_WINDOW", self.windowHide)
			LoginWindow.loginusername = StringVar()
			LoginWindow.loginpassword = StringVar()

			## MESSY UI STUFF! I HATE YOU TKINTER!
			loginIcon = PhotoImage(file = "img/user_login.gif")
			keyIcon = PhotoImage(file = "img/key.gif")

			LoginWindow.loginWidgetFrame1 = Frame(LoginWindow.loginwindow)
			LoginWindow.loginWidgetFrame1.pack(side = TOP, fill = X)
			LoginWindow.loginWidgetFrame2 = Frame(LoginWindow.loginwindow)
			LoginWindow.loginWidgetFrame2.pack(side = TOP, fill = X)
			LoginWindow.loginWidgetFrame3 = Frame(LoginWindow.loginwindow)
			LoginWindow.loginWidgetFrame3.pack(side = TOP, fill = X)
			LoginWindow.loginUsernameLabelImg = Label(LoginWindow.loginWidgetFrame1, image = loginIcon)
			LoginWindow.loginUsernameLabelImg.pack(side = LEFT)
			LoginWindow.loginUsernameLabelTxt = Label(LoginWindow.loginWidgetFrame1, text = "Username: ", font=font1)
			LoginWindow.loginUsernameLabelTxt.pack(side = LEFT)
			LoginWindow.loginUsernameBox = Entry(LoginWindow.loginWidgetFrame1, font=font2, relief = WINDOW_RELIEF, textvariable = LoginWindow.loginusername)
			LoginWindow.loginUsernameBox.pack(side = LEFT, expand = True)
			LoginWindow.loginPasswordLabelImg = Label(LoginWindow.loginWidgetFrame2, image = keyIcon)
			LoginWindow.loginPasswordLabelImg.pack(side = LEFT)
			LoginWindow.loginPasswordLabelTxt = Label(LoginWindow.loginWidgetFrame2, text = "    Password: ", font=font1)
			LoginWindow.loginPasswordLabelTxt.pack(side = LEFT)
			LoginWindow.loginPasswordBox = Entry(LoginWindow.loginWidgetFrame2, font=font2, relief = WINDOW_RELIEF, show = '*', textvariable = LoginWindow.loginpassword)
			LoginWindow.loginPasswordBox.pack(side = LEFT, expand = True)
			LoginWindow.loginSubmitCredButton = Button(LoginWindow.loginWidgetFrame3, text = "Submit", font=font1, bg = "dark green", fg = "#ffffff", activebackground = "dark green", activeforeground = "#ffffff")
			LoginWindow.loginCancelButton = Button(LoginWindow.loginWidgetFrame3, text = "Cancel", font=font1, bg = "dark red", fg = "#ffffff", activebackground = "dark red", activeforeground = "#ffffff", command = LoginWindow.loginwindow.withdraw)
			LoginWindow.loginCancelButton.pack(side = RIGHT)
			LoginWindow.loginSubmitCredButton.pack(side = RIGHT)
			LoginWindow.isOpen = True
		else:
			LoginWindow.loginwindow.deiconify() 
		
		self.linkedCC = controlcenter
		self.selectedUser = selectedUser
		if self.selectedUser == None:
			def_input_username = ""
		else:
			def_input_username = self.selectedUser.getUsername()

		if self.selectedUser == None or self.selectedUser.isLoggedIn() == False:
			if def_input_username != LoginWindow.loginusername.get():
				LoginWindow.loginpassword.set("")
			LoginWindow.loginusername.set(def_input_username)

			LoginWindow.loginSubmitCredButton.bind("<ButtonRelease-1>", self.submit)

			LoginWindow.loginwindow.deiconify()
			LoginWindow.loginwindow.mainloop()
		else:
			if selectedUser != None:
				cc.logoutUser(self.selectedUser.getUserID())
				self.windowHide()
				updateAwesomesauceControls()
			else:
				tkMessageBox.showerror("Log out Failed", "No user is selected.")

	def submit(self, event):
		self.windowHide()
		opstat = self.linkedCC.loginUser(LoginWindow.loginusername.get(), LoginWindow.loginpassword.get())
		if opstat == "SUCCESS":
			self.linkedCC.setSelected(self.linkedCC.getUserByName(LoginWindow.loginusername.get()).getUserID())
			updateAwesomesauceControls()
		else:
			tkMessageBox.showerror("Login Fail", opstat)
		del LoginWindow.loginwindow
		LoginWindow.isOpen = False
		
	def windowHide(self):
		LoginWindow.loginwindow.withdraw()
		LoginWindow.isOpen = False

menubar = Menu(mainWindow, tearoff=False)
usermenu = Menu(menubar, tearoff=False)
usermenu.add_command(label="New")
usermenu.add_command(label="Select")
usermenu.add_command(label="Log in/out", command=logInOut)
usermenu.add_command(label="Delete")

menubar.add_cascade(label="User", menu=usermenu)

helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="Manual")
helpmenu.add_command(label="About", command=menu_showinfobox)

menubar.add_cascade(label="Help", menu=helpmenu)

LogoImg = PhotoImage(file = "img/logo_small.gif")
LogoLabel = Label(adminFrame, image = LogoImg, relief = "flat")
LogoLabel.pack(side=TOP, fill=X)
userListLabel = Label(adminFrame, text="User Profiles: ", fg="#1E996C", font=("Helvetica", 9, "bold"))
userListLabel.pack(side=TOP, fill=X)
userListFrame = Frame(adminFrame, height=200, relief=WINDOW_RELIEF)
userListFrame.pack(side=TOP, fill=X)
adminFrameScrollBar = Scrollbar(userListFrame)
adminFrameScrollBar.pack(side=RIGHT, fill=Y)
userListBox = Listbox(userListFrame, yscrollcommand = adminFrameScrollBar.set, font=("Helvetica", 11, "normal"), selectbackground="#1E996C", selectforeground="#FFFFFF", selectmode=SINGLE, height=7)
userListBox.pack(side=TOP, fill=BOTH, expand=True)
adminFrameScrollBar.config(command = userListBox.yview)

for profile in cc.getUsers():
	userListBox.insert(END, profile.getUsername())

controlBoxLabel = Label(adminFrame, text="Basic Credentials: ", fg="#008FD5", font=("Helvetica", 9, "bold"))
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

profileDisplay = Frame(userFrame, relief = WINDOW_RELIEF, height=128)
profileDisplay.pack(side=TOP, fill=X)
photofilename = "img/defaultpic.gif"
profilepicfile = PhotoImage(file = photofilename)
profilePicture = Label(profileDisplay, bg="#ffffff", height = 128, width=128, image=profilepicfile, padx = 0, pady = 0)
profilePicture.pack(side=LEFT)
profileDisplayFrame1 = Frame(profileDisplay)
profileDisplayFrame1.pack(side = TOP, fill=X)
profileName = Label(profileDisplayFrame1, text="Welcome to Treefort", font = font3)
profileName.pack(side=LEFT)
profileDisplayFrame2 = Frame(profileDisplay)
profileDisplayFrame2.pack(side = TOP, fill=X)
profileSubLabel1 = Label(profileDisplayFrame2, text="Select a user to change the point of view.", font = font2, justify=LEFT, padx = 3, pady = 3)
profileSubLabel1.pack(side=LEFT)
profileSubLabel2 = Label(profileDisplayFrame2, font = font1, justify=LEFT, padx = 3, pady = 3)
profileSubLabel2.pack(side=LEFT)

profileDisplayFrame3 = Frame(profileDisplay)
profileDisplayFrame3.pack(side = TOP, fill=X)
loginoutButton = Button(profileDisplayFrame3, text="Log In", state=DISABLED, font=font2, command=logInOut, bg="#A0A0A0", fg="white", activebackground = "#A0A0A0", activeforeground = "white")
loginoutButton.pack(side=LEFT)

## Event Handlers

def updateAwesomesauceControlsRedir(event):
	curselected = userListBox.curselection()
	if curselected != tuple():
		curselected = int(curselected[0])
		cc.setSelected(curselected)
	else:
		cc.setSelected(-1)
	updateAwesomesauceControls()

def updateAwesomesauceControls():
	selectedUser = cc.getSelected()
	if selectedUser == None:
		return
	userListBox.activate(selectedUser.getUserID())

	userIDBox.config(text = selectedUser.getUserID())
	nameBox.config(text = selectedUser.getUsername())
	passwordBox.config(text = selectedUser.getPassword())

	profilePicture.config(image = selectedUser.getProfilePic())
	profileName.config(text = selectedUser.getUsername())
	if selectedUser.isLoggedIn() == False:
		profileSubLabel1.config(text = "Log in to your account below.", font = font2, fg = "black")
		profileSubLabel2.config(text = "")
		loginoutButton.config(text = "Log In", state=NORMAL, activebackground = "#004A7F", bg = "#004A7F")
	else:
		gender = selectedUser.getGender()
		profileSubLabel1.config(text = "Gender: " + gender, font = font1)
		if gender == "Male":
			profileSubLabel1.config(fg = "#007CFF")
		elif gender == "Female":
			profileSubLabel1.config(fg = "#FF006E")
		else:
			profileSubLabel1.config(fg = "#A0A0A0")
		
		profileSubLabel2.config(text = "Age: " + str(selectedUser.getAge()), fg = "#007F46")
		
		loginoutButton.config(text = "Log Out", state=NORMAL, activebackground = "dark red", bg = "dark red")

## Event Bindings

userListBox.bind("<ButtonRelease-1>", updateAwesomesauceControlsRedir)

mainWindow.config(menu = menubar)
mainWindow.mainloop()

cc.saveDB()