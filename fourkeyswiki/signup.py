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
import re
import hashlib
import random
import string

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
	return not email or EMAIL_RE.match(email)	

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(15))

def make_pw_hash(pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(pw + salt).hexdigest()
	return '%s,%s' % (h, salt)

def valid_pw(pw, h):
	salt = h.split(',')[1]
	test = hashlib.sha256(pw + salt).hexdigest()
	return test == h.split(',')[0]
