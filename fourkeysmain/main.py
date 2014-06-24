#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import re

import rot13
import signup

from google.appengine.ext import db

#current directory im in /templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates') 
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#base class contains template rendering functions 
class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		template = jinja_env.get_template(template)
		return template.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(BaseHandler):
	def get(self):
		self.render('main-page.html')

	def post(self):
		rot13 = self.request.get('rot13')
		shopping = self.request.get('shopping')
		fizzbuzz = self.request.get('fizzbuzz')
		signup = self.request.get('signup')
		asciichan = self.request.get('asciichan')

		if rot13:
			self.redirect('/rot13')
		elif shopping:
			self.redirect('/shopping')
		elif signup:
			self.redirect('/signup')
		elif fizzbuzz:
			self.redirect('/fizzbuzz')
		elif asciichan:
			self.redirect('/asciichan')

class Rot13(BaseHandler):
	def get(self):
		self.render('rot13-form.html')

	def post(self):
		finaltext = ''
		tex = self.request.get('text')
		finaltext = rot13.rotcipher(tex)
		
		self.render('rot13-form.html', text = finaltext)

class Signup(BaseHandler):
	def get(self):
		self.render('signup-form.html')
	
	def post(self):
		
		have_error = False	
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_veri = self.request.get('verify')
		user_emai = self.request.get('email')

		params = dict(username = user_name,
						email = user_emai)
		
		if(user_name):
			if not signup.valid_username(user_name):
				params['usererror'] = "That is not a valid username"
				have_error = True
		else:
			params['usererror'] = "That is not a valid username"
			have_error = True
		
		if(user_pass):
			if not signup.valid_password(user_pass):
				params['passerror'] = "That is not a valid password"
				have_error = True
		else:
			params['passerror'] = "That is not a valid password"
			have_error = True				
			
		if(user_pass and user_veri):
			if not signup.verify_password(user_pass, user_veri):
				params['verifyerror'] = "Those passwords do not match"
				have_error = True
				
		if(user_pass and not(user_veri)):
			params['verifyerror'] = "Those passwords do not match"
			have_error = True
					
		if(user_emai):
			if not signup.valid_email(user_emai):
				params['emailerror'] = "That is not a valid email address"
				have_error = True
					
		if have_error:
			self.render('signup-form.html', **params)
		else:
			self.redirect('/welcome?username=' + user_name)


class Welcome(BaseHandler):
	def get(self):
		username = self.request.get('username')
		if signup.valid_username(username):
			self.render('welcome.html', username = username)
		else:
			self.redirect('/signup')

class Fizzbuzz(BaseHandler):
	def get(self):
		n = self.request.get("n", 0)
		if n:
			n = int(n)
		self.render('fizzbuzz.html', n = n)

class Shopping(BaseHandler):
	def get(self):
		items = self.request.get_all('food')
		self.render('shopping-form.html', items = items)

class asciichan(BaseHandler):
	def render_asciichan(self, title="", art="", error=""):
		self.render('ascii.html', title=title, art=art, error=error)

	def get(self):
		self.render_asciichan()

	def post(self):
		title = self.request.get('title')
		art = self.request.get('art')

		if title and art:
			self.write("Thanks")
		else:
			error = "We need both a title and some artwork!"
			self.render_asciichan(error=error, title=title, art=art)






app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13),
    ('/shopping', Shopping),
    ('/signup', Signup),
	('/welcome', Welcome),
	('/fizzbuzz', Fizzbuzz),
	('/asciichan', asciichan)
], debug=True)
