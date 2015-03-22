import datetime
import os

import webapp2
from google.appengine.ext.webapp import template
#from dateutil.parser import parse

from model.NoteObj import NoteObj


def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)


class MainHandler(webapp2.RequestHandler):

    def get(self,key):
        newstr = key.replace("\"", "")
        n = NoteObj.get_by_id(int(newstr))
        template_params = {
            "note":n,
        }
        render_template(self, 'notes.html', template_params)


    #post endpoint
    #requires/accepts:
    #           bool    autosave - 0 for manual save 1 for autosave
    #           bool    newn     - 0 for old note 1 for new note from home page
    #           key     key      - retrieves note from db
    #           string  title
    #           string  content
    #           date    modified
    def post(self,notey):

        newn = bool(int(self.request.get("newn")))
        title = self.request.get("title")
        print(title)
        autosave = False
        #modified = datetime()
        n = NoteObj()
        template_params={}

        #new note from homepage
        if newn:
            #only title is valid note property
            #key is invalid
            n.title = title
            n.text = ""
            n.modified = datetime.datetime.now()
            n.put()
            key = n.key().id()
            template_params = {
                "note":n,
            }
            #key is now valid
        #manual save
        else:
            #note props (title, content, modified are all valid)
            #key is valid
            key = int(self.request.get("key"))
            n=NoteObj.get_by_id(key)
            n.title = title
            text = self.request.get("content")
            n.text = text
            autosave = bool(self.request.get("autosave"))
            n.modified = datetime.datetime.now()
            n.put()
            n=NoteObj.get_by_id(key)
            template_params = {
                "note":n,
            }

        #autosave only changes what we output
        #if it's autosave we only write "OK"
        #otherwise we render the template
        if autosave:
            self.response.write("OK")
        else:
            render_template(self, 'notes.html', template_params)


app = webapp2.WSGIApplication([
                                  ('/notes/(.*?)', MainHandler)
                              ], debug=True)
