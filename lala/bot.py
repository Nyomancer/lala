import logging
from twisted.words.protocols.irc import IRCClient
from lala import util

class Lala(IRCClient):
    __version__ = "0.2~git"

    versionName = "lala"
    versionNum = __version__
    lineRate = 1

    def _get_nick(self):
        return self.factory.nickname


    nickname = property(_get_nick)

    def signedOn(self):
        logging.debug("Joining %s" % self.factory.channel)
        self.join(self.factory.channel)

    def joined(self, channel):
        logging.debug("Successfully joined %s" % channel)

    def userJoined(self, user, channel):
        logging.debug("%s joined %s" % (user, channel))
        util._PM.on_join(user, channel) 

    def privmsg(self, user, channel, message):
        user = user.split("!")[0]
        if channel == self.nickname:
            channel = user
        self.factory.logger.info("%s: %s" % (user, message))
        util._PM._handle_message(user, channel, message)
