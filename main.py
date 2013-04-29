#!/usr/bin/env python
import webapp2
import os
import jinja2
import logging
from time import sleep
from google.appengine.api import taskqueue, users, channel
from google.appengine.ext import db

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            key = self.request.get('key')
            if not key:
                key = user.user_id()
            key_link = 'http://localhost:8080/?key=' + key
            token = channel.create_channel(key)
            template_values = {'token': token,
                    'me': user.user_id(),
                    'key': key,
                    'key_link': key_link,
                    'initial_message': 'Nothing to show yet'}
            template = jinja_environment.get_template('template.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        key = self.request.get('key')
        taskqueue.add(url='/sendmessages', params={'key': key})
        #self.redirect('/?key=' + key)
        self.redirect('/')

class SendMessagesHandler(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        sleep(2)
        channel.send_message(key, 'Starting to send messages...')
        logging.info('Starting to send messages...')
        i = 0
        while i < 60:
            i += 1
            logging.info('Counter incremented.')
            channel.send_message(key, 'Counter incemented ' + str(i))
            sleep(1)

jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
app = webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/sendmessages', SendMessagesHandler)
    ], debug=True)
