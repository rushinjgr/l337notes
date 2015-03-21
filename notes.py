import datetime
import os

import webapp2
from google.appengine.ext.webapp import template

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
            'title':n.title,
            'notetext':n.text,
            'key':newstr
        }
        render_template(self, 'notes.html', template_params)

    def post(self,notey):
        text = self.request.get("text")
        title = self.request.get("Title")
        status = int(self.request.get("new2"))
        if(status == 1):
            n = NoteObj()
            n.title = title
            n.text=""
            n.modified = datetime.datetime.now()
            n.put()
            key=n.key().id()
            template_params = {
                'title':title,
                'notetext':text,
                'key':key
            }
            render_template(self, 'notes.html', template_params)
        else:
            autosave = bool(self.request.get("autosave"))
            if(autosave):
                key = self.request.get("key")
                n = NoteObj.get_by_id(int(key))
                n.title = title
                n.text = text
                n.modified = datetime.datetime.now()
                n.put()
                template_params = {
                    'title':n.title,
                    'notetext':n.text,
                    'key':key
                }
                self.response.write("OK")
            else:
                key = self.request.get("key")
                n = NoteObj.get_by_id(int(key))
                n.title = title
                n.text = text
                n.modified = datetime.datetime.now()
                n.put()
                template_params = {
                    'title':n.title,
                    'notetext':n.text,
                    'key':key
                }
                render_template(self, 'notes.html', template_params)


app = webapp2.WSGIApplication([
                                  ('/notes/(.*?)', MainHandler)
                              ], debug=True)
