import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class useraccount(ndb.Model):
    email = ndb.StringProperty(indexed=False)
    identity = ndb.StringProperty(indexed=False)

class Thesis(ndb.Model):
    year = ndb.StringProperty(indexed=True)
    title1 = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty(indexed=True)  

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            self.redirect(url)

        template_values = {
            'user':user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

class thesisAPI(webapp2.RequestHandler):
    def get(self):  
        allthesis = Thesis.query().order(-Thesis.year)
        thesis_list = []

        for t in allthesis:
            thesis_list.append({
                'year': t.year,
                'title1': t.title1,
                'abstract': t.abstract,
                'adviser': t.adviser,
                'section': t.section
                })

        response = {
            'result': 'OK',
            'data': thesis_list
        }                           
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()

        if users.get_current_user():
            thesis.section = users.get_current_user().email()

        thesis.year = self.request.get('year')
        thesis.title1 = self.request.get('title1')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result': 'OK',
        'data': {
            'year': thesis.year,
            'title1': thesis.title1,
            'abstract': thesis.abstract,
            'adviser': thesis.adviser,
            'section': thesis.section,
            }
        }
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/api/thesis', thesisAPI),
    ('/home', MainPageHandler),
    ('/', MainPageHandler)
], debug=True)
