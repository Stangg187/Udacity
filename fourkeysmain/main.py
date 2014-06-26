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

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

#base class contains template rendering functions 
class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		template = jinja_env.get_template(template)
		return template.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

### Front Page of site

class MainPage(BaseHandler):
	def get(self):
		self.render('main-page.html')

	def post(self):
		rot13 = self.request.get('rot13')
		shopping = self.request.get('shopping')
		fizzbuzz = self.request.get('fizzbuzz')
		signup = self.request.get('signup')
		asciichan = self.request.get('asciichan')
		blog = self.request.get('blog')

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
		elif blog:
			self.redirect('/blog')

### Rot13

class Rot13(BaseHandler):
	def get(self):
		self.render('rot13-form.html')

	def post(self):
		finaltext = ''
		tex = self.request.get('text')
		finaltext = rot13.rotcipher(tex)
		
		self.render('rot13-form.html', text = finaltext)

### Signup Form

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

### Fizzz Buzzz

class Fizzbuzz(BaseHandler):
	def get(self):
		n = self.request.get("n", 0)
		if n:
			n = int(n)
		self.render('fizzbuzz.html', n = n)

### Shopping

class Shopping(BaseHandler):
	def get(self):
		items = self.request.get_all('food')
		self.render('shopping-form.html', items = items)

#### ASCII classes

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def render(self):
		return render_str("art.html", art = self)

class asciichan(BaseHandler):
	def render_asciichan(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

		self.render('ascii.html', title=title, art=art, error=error, arts=arts)

	def get(self):
		self.render_asciichan()

	def post(self):
		title = self.request.get('title')
		art = self.request.get('art')

		if title and art:
			a = Art(title = title, art = art)
			a.put()

			self.redirect("/asciichan")
		else:
			error = "We need both a title and some artwork!"
			self.render_asciichan(error=error, title=title, art=art)

###BLOG CLASSES

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Blog(db.Model):
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now_add = True)

	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("post.html", blog = self)

class BlogHandler(BaseHandler):
	def render_blog(self):
		blogs = db.GqlQuery("SELECT * from Blog order by created desc limit 10")

		self.render('blogfront.html', blogs=blogs)

	def get(self):
		self.render_blog()

	def post(self):
		self.redirect('/blog/newpost')			

class BlogNewPostHandler(BaseHandler):
	def get(self):
		self.render('blognewpost.html')

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')
		
		if subject and content:
			b = Blog(parent = blog_key(), subject = subject, content = content)
			b.put()
			post_id = b.key().id()

			self.redirect('/blog/%d' % post_id)
		else:
			error = "We need both a subject and cotnent!"
			self.render('blognewpost.html', subject=subject, content=content, error=error)	

class BlogPostHandler(BaseHandler):
	def get(self, post_id):
		key = db.Key.from_path('Blog', int(post_id), parent=blog_key())
		post = db.get(key)

		if not post:
			self.error(404)

		self.render('blogpost.html', post=post, post_id=post_id)


### WSGI Hanlders and URLS

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13),
    ('/shopping', Shopping),
    ('/signup', Signup),
	('/welcome', Welcome),
	('/fizzbuzz', Fizzbuzz),
	('/asciichan', asciichan),
	('/blog', BlogHandler),
	('/blog/newpost', BlogNewPostHandler),
	('/blog/(\d+)', BlogPostHandler)
], debug=True)
