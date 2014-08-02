#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
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
import hmac
import random
import string
import urllib2
import json
import logging
import time

import rot13
import signup

from xml.dom import minidom
from google.appengine.ext import db
from google.appengine.api import memcache

#current directory im in /templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

secret = 'feqw98wef98wegqf89efgyj12asccb'

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

    def set_secure_cookie(self, name, val):
        cookie_val = str(make_secure_val(val))
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json_txt)


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
        login = self.request.get('login')
        robot = self.request.get('robot')

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
        elif login:
            self.redirect('/login')
        elif robot:
            self.redirect('/robot')


### Rot13

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        finaltext = ''
        tex = self.request.get('text')
        finaltext = rot13.rotcipher(tex)

        self.render('rot13-form.html', text=finaltext)


### Signup Form
class UserData(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty(required=False)


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
            hashed_password = signup.make_pw_hash(user_pass, user.password.split(',')[1])
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


class Welcome(BaseHandler):
    def get(self):
        cookie = self.read_secure_cookie('user_id')

        if cookie:
            self.render('welcome.html', username=cookie)
        else:
            self.redirect('/signup')

    def post(self):
        logout = self.request.get('Logout')

        if logout:
            self.response.delete_cookie('user_id')
            self.redirect('/logout')


class Logout(BaseHandler):
    def get(self):
        self.response.delete_cookie('user_id')
        self.redirect('/signup')


### Fizzz Buzzz

class Fizzbuzz(BaseHandler):
    def get(self):
        n = self.request.get("n", 0)
        if n:
            n = int(n)
        self.render('fizzbuzz.html', n=n)


### Shopping

class Shopping(BaseHandler):
    def get(self):
        items = self.request.get_all('food')
        self.render('shopping-form.html', items=items)

#### ASCII classes
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=280x190&sensor=false&"


def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers


IP_URL = "http://api.hostip.info/?ip="


def get_coords(ip):
    ip = "4.2.2.2"
    ip = "23.24.209.141"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return

    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)  #google datatype for latitude and longitutde


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    coords = db.GeoPtProperty()

    def render(self):
        return render_str("art.html", art=self)


def art_key(name='default'):
    return db.Key.from_path('arts', name)


def top_arts(update=False):
    key = 'top'

    arts = memcache.get(key)

    if arts is None or update:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * "
                           "FROM Art "
                           "WHERE ANCESTOR IS :1 "
                           "ORDER BY created DESC "
                           "LIMIT 10",
                           art_key())

        # prevent query from running multiple times (also called in html)
        arts = list(arts)

        memcache.set(key, arts)

    return arts


class asciichan(BaseHandler):
    def render_asciichan(self, title="", art="", error=""):
        arts = top_arts()

        points = filter(None, (a.coords for a in arts))
        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render('ascii.html', title=title, art=art, error=error, arts=arts, img_url=img_url)

    def get(self):
        self.render_asciichan()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(parent=art_key(), title=title, art=art)
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords

            a.put()
            # return the query and update the cache
            top_arts(True)

            self.redirect("/asciichan")
        else:
            error = "We need both a title and some artwork!"
            self.render_asciichan(error=error, title=title, art=art)


###BLOG CLASSES
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", blog=self)


def top_posts(update=False):
    key = 'topposts'

    blogs = memcache.get(key)

    if blogs is None or update:
        logging.error("DB QUERY")
        blogs = db.GqlQuery("SELECT * "
                            "from Blog "
                            "WHERE ANCESTOR IS :1 "
                            "order by created desc "
                            "limit 10",
                            blog_key())

        blogs = list(blogs)
        timeran = time.time()

        memcache.set(key, blogs)
        memcache.set('age', timeran)
    return blogs


class BlogHandler(BaseHandler):
    def get(self):
        blogs = top_posts()

        lastqueried = time.time() - memcache.get('age')

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

        if self.format == 'html':
            self.render('blogfront.html', blogs=blogs)
            self.response.out.write('Queried %d seconds ago' % lastqueried)
        else:
            json = []
            for p in blogs:
                time_fmt = '%c'
                d = {'subject': p.subject, 'content': p.content, 'created': p.created.strftime(time_fmt),
                     'last_modified': p.last_modified.strftime(time_fmt)}
                json.append(d)
            self.render_json(json)

    def post(self):
        self.redirect('/blog/newpost')


class BlogNewPostHandler(BaseHandler):
    def get(self):
        self.render('blognewpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            b = Blog(parent=blog_key(), subject=subject, content=content)
            b.put()

            top_posts(True)

            post_id = b.key().id()

            self.redirect('/blog/%d' % post_id)
        else:
            error = "We need both a subject and content!"
            self.render('blognewpost.html', subject=subject, content=content, error=error)


def perma_post(post_id):
    postkey = str(post_id)
    post = memcache.get(postkey)

    if post is None:
        logging.error("DB QUERY")

        key = db.Key.from_path('Blog', int(post_id), parent=blog_key())
        post = db.get(key)

        agekey = str(post_id) + 'age'
        age = time.time()

        memcache.set(postkey, post)
        memcache.set(agekey, age)
    return post


class BlogPostHandler(BaseHandler):
    def get(self, post_id):

        post = perma_post(post_id)
        agekey = str(post_id) + 'age'

        lastqueried = time.time() - memcache.get(agekey)

        if not post:
            self.error(404)
            return

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

        if self.format == 'html':
            self.render('blogpost.html', post=post, post_id=post_id)
            self.response.out.write('Queried %d seconds ago' % lastqueried)
        else:
            time_fmt = '%c'
            d = {'subject': post.subject, 'content': post.content, 'created': post.created.strftime(time_fmt),
                 'last_modified': post.last_modified.strftime(time_fmt)}
            self.render_json([d])


class Flush(BaseHandler):
    def get(self):
        memcache.flush_all()
        self.redirect('/blog')


### Robot
class Robot(BaseHandler):
    def get(self):
        self.render('robot.html')


### WSGI Hanlders and URLS

app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/rot13/?', Rot13),
                                  ('/shopping/?', Shopping),
                                  ('/?(?:blog)?/signup/?', Signup),
                                  ('/?(?:blog)?/welcome/?', Welcome),
                                  ('/fizzbuzz/?', Fizzbuzz),
                                  ('/asciichan/?', asciichan),
                                  ('/blog/?(?:\.json)?', BlogHandler),
                                  ('/blog/newpost/?', BlogNewPostHandler),
                                  ('/blog/(\d+)/?(?:\.json)?', BlogPostHandler),
                                  ('/?(?:blog)?/login/?', Login),
                                  ('/?(?:blog)?/logout/?', Logout),
                                  ('/robot/?', Robot),
                                  ('/?(?:blog)?/flush', Flush)
                              ], debug=True)
