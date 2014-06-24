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


form="""
<form method="post" action="/testform">
	<input name="q">
	<input type="submit" value="Submit to testform">
</form>

<form action="http://www.google.co.uk/search">
	<input type ="text" name="q">
	<input type="submit" value="Submit to google">
</form>

<form>
	<input type="password" name="q">
	<input type="submit" value="Submit password">
</form>

<form>
	<input type="checkbox" name="q">
	<input type="checkbox" name="r">
	<input type="checkbox" name="s">
	<br>
	<input type="submit">
</form>

<form>
	<label>
		One
		<input type="radio" name="q" value="one">
	</label>
	<label>
		Two
		<input type="radio" name="q" value="two">
	</label>
	<label>
		Three
		<input type="radio" name="q" value="three">
	</label>
	<br>
	<input type="submit">
</form>

<form>
	<select name="q">
		<option value="1">the number one</option>
		<option value="2">the number two</option>
		<option value="3">the number three</option>
	</select>
	<br>
	<input type="submit">
</form>

<form method="post">
	What is your birthday?
	<br>
	
	<label> Month
		<input type="text" name="month" value="%(month)s">
	</label>
	
	<label> Day
		<input type="text" name="day" value="%(day)s">
	</label>
	
	<label> Year
		<input type="text" name="year" value="%(year)s">
	</label>
	<div style="color: red">%(error)s</div>
	<br>
	<br>
	<input type="submit" name="bday">
</form>
"""
cipherform="""
<form method="post">
	Enter some text to ROT13:
	<br>
	<textarea name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
	<br>
	<input type="submit" name="rot">
</form>
"""
months =	['January',
			'February',
			'March',
			'April',
			'May',
			'June',
			'July',
			'August',
			'September',
			'October',
			'November',
			'December']
		  
month_abbvs = dict((m[:3].lower(), m) for m in months)

def rotcipher(text):
	output = ''
	for i in text:
		if i.isalpha():
			if ord(i)>=65 and ord(i)<=77:
				output += chr(ord(i)+13)
			elif ord(i)>=78 and ord(i)<=96:
				output += chr(ord(i)-13)
			elif ord(i)>=97 and ord(i)<=109:
				output += chr(ord(i)+13)
			else:
				output += chr(ord(i)-13)
		else:
			output += i
	return output

def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return month_abbvs.get(short_month)
		
def valid_day(day):
	if day.isdigit() and 1 <= int(day) <= 31:
		return int(day)

def valid_year(year):
	if year.isdigit() and 1900 <= int(year) <= 2020:
		return int(year)

def escape_html(s):
	return cgi.escape(s, quote = True)

class MainHandler(webapp2.RequestHandler):
	
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error": error,
										"month": escape_html(month),
										"day": escape_html(day),
										"year": escape_html(year)})
	
	def cipher_form(self, text=""):
		self.response.out.write(cipherform % {"text": text})
	
	
	def get(self):
		self.write_form()
		self.cipher_form()
					
	def post(self):
		bday = self.request.get('bday')
		rot = self.request.get('rot')
		if bday:
			user_month = self.request.get('month')
			user_day = self.request.get('day')
			user_year = self.request.get('year')
					
			month = valid_month(user_month)
			day = valid_day(user_day)
			year = valid_year(user_year)
			
			escapedtext = ''
			tex = self.request.get('text')
			escapedtext = escape_html(escapedtext)
			
			if not (month and day and year):
				self.write_form("That doesn't look valid to me, friend.",
								user_month,
								user_day,
								user_year)
				self.cipher_form(escapedtext)
			else:
				self.redirect("/thanks")
		else:
			user_month = self.request.get('month')
			user_day = self.request.get('day')
			user_year = self.request.get('year')
			
			finaltext = ''
			tex = self.request.get('text')
			finaltext = rotcipher(tex)
			
			escapedtext = ''
			escapedtext = escape_html(finaltext)
			
			self.write_form("I'll just keep this warm",
							user_month,
							user_day,
							user_year)
			self.cipher_form(escapedtext)
		
class TestHandler(webapp2.RequestHandler):
	def post(self):
		q = self.request.get("q")
		self.response.out.write(q)

		#self.response.headers['Content-Type'] = 'text/plain'
		#self.response.out.write(self.request)

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("Thanks! That's a totally valid day! :D ")
		

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/testform', TestHandler),
	('/thanks', ThanksHandler)
], debug=True)

		
		
		
		