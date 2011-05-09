import sqlite3
import logging
import os

from time import sleep
from lala.util import command, initplz, msg, on_join, is_admin

db_connection = None

@initplz
def setup():
    global db_connection
    db_connection =  sqlite3.connect(
                os.path.join(os.path.expanduser("~/.lala"),"quotes.sqlite3"))
    db_connection.execute("CREATE TABLE IF NOT EXISTS quotes(\
        quote TEXT);")
    db_connection.commit()
    db_connection.text_factory = sqlite3.OptimizedUnicode


@command
def getquote( user, channel, text):
    """Show the quote with a specified number"""
    s_text = text.split()
    if len(s_text) > 1:
        quotenumber = s_text[1]
        logging.debug("Trying to get quote number %s" % quotenumber)
        with db_connection:
            q = db_connection.execute("SELECT quote FROM quotes\
                WHERE rowid = ?;", [quotenumber]).fetchall()
            if len(q) > 0:
                msg(channel, "[%s] %s" % (quotenumber, q[0][0]))
            else:
                msg(channel, "%s: There's no quote #%s" % (user,
                    quotenumber))

@command
def addquote( user, channel, text):
    """Add a quote"""
    s_text = text.split()
    if len(s_text) > 1:
        text = " ".join(s_text[1:])
        logging.debug("Adding quote: %s" % text)
        with db_connection:
            c = db_connection.execute("INSERT INTO quotes (quote) values (?);",
                    [text])
            msg(channel, "New quote: %s" % c.lastrowid)
    else:
        msg(channel, "%s: You didn't give me any text to quote " % user)

@command
def delquote( user, channel, text):
    """Delete a quote with a specified number"""
    s_text = text.split()
    if is_admin(user):
        if len(s_text) > 1:
            quotenumber = s_text[1]
            logging.debug("Deleting quote: %s" % quotenumber)
            with db_connection:
                c = db_connection.execute("DELETE FROM quotes where ROWID = (?);",
                    [quotenumber]).fetchall()
                db_connection.commit()
        else:
            msg(channel, "%s: There's no quote #%s" % (user,
                quotenumber))

@command
def lastquote( user, channel, text):
    """Show the last quote"""
    with db_connection:
        try:
            (id, quote) = db_connection.execute("SELECT rowid, quote FROM quotes\
            ORDER BY rowid DESC LIMIT 1;").fetchall()[0]
        except IndexError, e:
            return
        msg(channel, "[%s] %s" % (id, quote))

@command
def randomquote( user, channel, text):
    """Show a random quote"""
    with db_connection:
        try:
            (id, quote) = db_connection.execute("SELECT rowid, quote FROM quotes ORDER\
            BY random() LIMIT 1;").fetchall()[0]
        except IndexError, e:
            return
        msg(channel, "[%s] %s" % (id, quote))

@command
def searchquote( user, channel, text):
    """Search for a quote"""
    s_text = text.split()
    logging.debug(s_text[1:])
    with db_connection:
        quotes = db_connection.execute("SELECT rowid, quote FROM quotes\
        WHERE quote LIKE (?)", [
            "".join(("%",
                    " ".join(s_text[1:]),
                    "%"))]
            ).fetchall()
        if len(quotes) > 5:
            msg(channel, "Too many results, please refine your search")
        else:
            for (id, quote) in quotes:
                msg(channel, "[%s] %s" % (id, quote))
                # TODO get rid of this ugly thing
                sleep(1)

@on_join
def join( event):
    user =  event[0][0]
    channel = event[1]
    with db_connection:
        try:
            (id, quote) = db_connection.execute("SELECT rowid, quote FROM quotes\
                WHERE quote LIKE (?) ORDER BY random() LIMIT\
                1;", ["".join(["%", user, "%"])]).fetchall()[0]
        except IndexError, e:
            # There's no matching quote,
            return
        msg(channel, "[%s] %s" % (id, quote))