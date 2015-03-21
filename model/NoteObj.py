from google.appengine.ext import db

class NoteObj (db.Model):
    title = db.StringProperty()
    text = db.TextProperty()
    modified = db.DateTimeProperty()