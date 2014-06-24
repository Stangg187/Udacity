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
import webapp2
import cgi
import re
 
form="""
<form method="post">
	Please enter your user details:
	<br>
	<label> Username
		<input type="text" name="username" value="%(username)s">
		<div style="color: red">%(usererror)s</div>
	</label>
	<br>
	<label> Password
		<input type="password" name="password" value="">
		<div style="color: red">%(passerror)s</div>
	</label>
	<br>
	<label> Verify Password
		<input type="password" name="verify" value="">
		<div style="color: red">%(verifyerror)s</div>
	</label>
	<br>
	<label> Email (Optional)
		<input type="text" name="email" value="%(email)s">
		<div style="color: red">%(emailerror)s</div>
	</label>
	<br>
	<br>
	<input type="submit">
</form>
"""

welcome="""
<div>Welcome to the website, %(username)s</div>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile("^.{3,20}$")
EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)
	
def valid_password(password):
	return PASS_RE.match(password)
	
def verify_password(password, verify):
	if password == verify:
		return verify

def valid_email(email):
	return EMAIL_RE.match(email)	

def escape_html(s):
	return cgi.escape(s, quote = True)

class MainHandler(webapp2.RequestHandler):
	def write_form(self, 
					username="", 
					usererror="", 
					passerror="", 
					verifyerror="", 
					email="", 
					emailerror=""):
		self.response.out.write(form % {"username": escape_html(username),
										"usererror": usererror,
										"passerror": passerror,
										"verifyerror": verifyerror,
										"email": escape_html(email),
										"emailerror": emailerror})
	
	def get(self):
		self.write_form()
		
	def post(self):
	
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_veri = self.request.get('verify')
		user_emai = self.request.get('email')
		
		uname = valid_username(user_name)
		passw = valid_password(user_pass)
		verif = verify_password(user_pass, user_veri)
		email = valid_email(user_emai)
		
		usererror = ""
		passerror = ""
		verifyerror = ""
		emailerror = ""
		
		if(user_name):
			if not(uname):
				usererror = "That is not a valid username"
		else:
			usererror = "That is not a valid username"
		
		if(user_pass):
			if not(passw):
				passerror = "That is not a valid password"
		else:
			passerror = "That is not a valid password"
				
			
		if(user_pass and user_veri):
			if not(verif):
				verifyerror = "Those passwords do not match"
				
		
		if(user_pass and not(user_veri)):
			verifyerror = "Those passwords do not match"
			
			
		if(user_emai):
			if not(email):
				emailerror = "That is not a valid email address"
				
		if not(usererror or passerror or verifyerror or emailerror):
			username = self.request.get('username')
			user = escape_html(username)
			self.redirect("/validated?username=%(user)s" % {"user": user})
		else:
			self.write_form(user_name,
							usererror,
							passerror,
							verifyerror,
							user_emai,
							emailerror)


class ValidHandler(webapp2.RequestHandler):
	def get(self, username=""):
		username = self.request.get('username')
		self.response.write(welcome % {"username": username})
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/validated', ValidHandler)
], debug=True)
