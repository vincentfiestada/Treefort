from controlcenter import *

cc = IControlCenter()
cc.openDB('db.txt','db_conv.txt','db_feed.txt')

for user in cc.getUsers():
	cc.aggregateNewsfeedById(user.getUserID())

for x in cc.getUserById(2).getNewsfeed().getStatuses():
	print "="*50
	print x.getTime() + ": " + x.getText() + "\n\tPosted by " + cc.getUserById(x.getPoster()).getUsername()
	print "\t" + str(len(x.getThumbsUps())) + " Thumbs Ups | " + str(len(x.getThumbsDowns())) + " Thumbs Downs"
	print "\tComments" + "-"*20
	for comment in x.getComments():
		print "\t\t" + cc.getUserById(comment.getPoster()).getUsername() + ": " + comment.getText()

cc.saveDB()