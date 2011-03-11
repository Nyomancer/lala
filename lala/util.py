import logging


_BOT = None

class command(object):
    """Decorator for commands"""
    def __init__(self, command):
        """docstring for __init__"""
        self.cmd = command

    def __call__(self, func):
        _BOT.register_callback(self.cmd, func)

def on_join(f):
    """Decorator for functions reacting to joins"""
    _BOT.register_join_callback(f)

def initplz(f):
    f()

def is_admin(user):
    if user in _BOT._admins:
        logging.debug("%s is an admin" % user)
        return True
    else:
        logging.debug("%s is not an admin" % user)
        return False

def msg(target, message):
    """Message wrapper"""
    _BOT.privmsg(target, message)
