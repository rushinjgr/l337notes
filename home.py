__author__ = 'Justin Rushin III'

import os

import webapp2
from google.appengine.ext.webapp import template
from model.NoteObj import NoteObj

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        notes = NoteObj.all()
        template_params = {
            'notes':notes.order("modified")
        }
        render_template(self, 'home.html', template_params)


app = webapp2.WSGIApplication([
                                  ('/', MainHandler)
                              ], debug=True)


