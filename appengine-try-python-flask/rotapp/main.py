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
<form method="post">
	Enter some text to ROT13:
	<br>
	<textarea name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
	<br>
	<input type="submit">
</form>
"""

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

def escape_html(s):
	return cgi.escape(s, quote = True)
	

class MainHandler(webapp2.RequestHandler):
	def write_form(self, text=""):
		self.response.out.write(form % {"text": text})
	
	def get(self):
		self.write_form()
			
	def post(self):
		finaltext = ''
		tex = self.request.get('text')
		finaltext = rotcipher(tex)
		
		escapedtext = ''
		escapedtext = escape_html(finaltext)
		
		self.write_form(escapedtext)
		

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

