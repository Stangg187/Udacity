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
import json
import logging
import hmac

import signup

from google.appengine.ext import db
from google.appengine.api import memcache

#current directory im in /templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates') 
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

secret = 'qfeion2g39024tonqeoin120923rbhj'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#base class contains template rendering functions 
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        template = jinja_env.get_template(template)
        return template.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = str(make_secure_val(val))
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

### Front Page of site

class MainPage(BaseHandler):
    def get(self):
        self.render('main-page.html')

class WikiContents(db.Model):
    wiki_id = db.StringProperty(required=True)
    content = db.TextProperty()
    author = db.StringProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)


class UserData(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty(required=False)

class EditPage(BaseHandler):
    def get(self, wiki_id):

        cookie = self.read_secure_cookie('user_id')

        wikicheck = db.GqlQuery("SELECT * from WikiContents WHERE wiki_id=:1 limit 1", wiki_id)
        wikipost = wikicheck.get()

        if cookie:
            if wikipost:
                self.response.out.write(wiki_id)
                self.render('editpage.html', subject=wiki_id, content=wikipost.content)
            else:
                self.render('editpage.html', subject=wiki_id)
        else:
            self.redirect('/login')

    def post(self, wiki_id):
        content = self.request.get('content')
        cookie = self.read_secure_cookie('user_id')

        w = WikiContents(wiki_id=wiki_id, content=content, author=cookie)
        w.put()

        self.redirect('/%s' % wiki_id)


class WikiPostHandler(BaseHandler):
    def get(self, wiki_id):

        self.response.out.write(wiki_id)

        wikicheck = db.GqlQuery("SELECT * from WikiContents WHERE wiki_id=:1 limit 1", wiki_id)
        wikipost = wikicheck.get()

        if wikipost:
            self.render('wikipost.html', subject=wiki_id, content=wikipost.content, author=wikipost.author)
        else:
            self.redirect('/_edit/%s' % wiki_id)

    def post(self, wiki_id):
        cookie = self.read_secure_cookie('user_id')

        if cookie:
            self.redirect('/_edit/%s' % wiki_id)
        else:
            self.redirect('/login')

class Signup(BaseHandler):
    def get(self):
        self.render('signup-form.html')

    def post(self):

        have_error = False
        user_name = self.request.get('username')
        user_pass = self.request.get('password')
        user_veri = self.request.get('verify')
        user_emai = self.request.get('email')

        params = dict(username=user_name,
                      email=user_emai)

        users = db.GqlQuery("SELECT * from UserData WHERE username=:1 limit 1", user_name)

        user = users.get()

        if (user_name):
            if not signup.valid_username(user_name):
                params['usererror'] = "That is not a valid username"
                have_error = True
        else:
            params['usererror'] = "That is not a valid username"
            have_error = True

        if user:
            params['usererror'] = "That username already exists"
            have_error = True

        if (user_pass):
            if not signup.valid_password(user_pass):
                params['passerror'] = "That is not a valid password"
                have_error = True
        else:
            params['passerror'] = "That is not a valid password"
            have_error = True

        if (user_pass and user_veri):
            if not signup.verify_password(user_pass, user_veri):
                params['verifyerror'] = "Those passwords do not match"
                have_error = True

        if (user_pass and not (user_veri)):
            params['verifyerror'] = "Those passwords do not match"
            have_error = True

        if (user_emai):
            if not signup.valid_email(user_emai):
                params['emailerror'] = "That is not a valid email address"
                have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            hashed_password = signup.make_pw_hash(user_pass)

            if user_emai:
                newuser = UserData(username=user_name, password=hashed_password, email=user_emai)
            else:
                newuser = UserData(username=user_name, password=hashed_password)

            newuser.put()

            self.set_secure_cookie('user_id', user_name)

            self.redirect('/welcome')


class Login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        have_error = False
        user_name = self.request.get('username')
        user_pass = self.request.get('password')

        params = dict(username=user_name)

        users = db.GqlQuery("SELECT * from UserData WHERE username=:1 limit 1", user_name)

        user = users.get()

        if user:
            checkpw = signup.valid_pw(user_pass, user.password)

        if (user_name):
            if not signup.valid_username(user_name):
                params['usererror'] = "That is not a valid username"
                have_error = True
        else:
            params['usererror'] = "That is not a valid username"
            have_error = True

        if not user:
            params['usererror'] = "That username does not exist"
            have_error = True
        elif user_pass:
            if not checkpw:
                params['passerror'] = "Invalid Password"
                have_error = True
        else:
            params['passerror'] = "Please enter a password"
            have_error = True

        if have_error:
            self.render('login.html', **params)
        else:
            self.set_secure_cookie('user_id', user_name)
            self.redirect('/welcome')

class Logout(BaseHandler):
    def get(self):
        self.response.delete_cookie('user_id')
        self.redirect('/signup')

### WSGI Handlers and URLS
PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/_edit/' + PAGE_RE, EditPage),
    ('/' + PAGE_RE, WikiPostHandler)
], debug=True)
