import random
from lala.util import command, msg

class revolver:
    def __init__(self):
        self.bullet = 1
	self.chamber = 1
	self.blasted = True
    

    def reload(self, user, channel, text):
        self.bullet = random.randint(1,6)
	self.chamber = 1
	self.blasted = False
	msg(channel, "Can't you see I'm reloading")

    def shoot(self, user, channel, text):
        if (self.chamber > 6) or self.blasted:
            #output "Please reload"
	    msg(channel, "Please reload")
	 
	elif (self.chamber == self.bullet):
            #ouput "BOOM"
	    msg(channel, "%s: BOOM" % user)
	    self.blasted = True
	    
	else:
	    #ouput "click"
	    msg(channel, "%s: *click*" % user)
	    self.chamber += 1
	    


knarre = revolver()

@command
def reload(user, channel, text):
    knarre.reload(user, channel, text)

@command
def shoot(user, channel, text):
    knarre.shoot(user, channel, text)
