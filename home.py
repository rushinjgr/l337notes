__author__ = 'Justin Rushin III'

import sys
import webapp2
import os
import glob
from google.appengine.ext.webapp import template

def render_template(handler, template_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + template_name)
    html = template.render(path, template_values)
    handler.response.out.write(html)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        notes = glob.glob('notes/*.txt')
        template_params = {
            'notes':notes
        }
        render_template(self, 'home.html', template_params)


app = webapp2.WSGIApplication([
                                  ('/', MainHandler)
                              ], debug=True)


