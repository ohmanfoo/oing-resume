# oingfolio.py

import os
import webapp2
import jinja2
from lib.vartools import *
from google.appengine.api import urlfetch
from google.appengine.ext import db
from models.models import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

from views.views import *

class FolioHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))



class Login(FolioHandler):
    def get(self):
        if not self.user:
            self.render('/admin/login-form.html')
        else:
            self.redirect('/')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/admin/newpost')
        else:
            msg = 'Invalid login'
            self.render('admin/login-form.html', error = msg)

class Logout(FolioHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')

class Signup(FolioHandler):
    def get(self):
        q = User.all()
        try:
            if q[0].name:
                self.redirect('/')
            else:
                self.redirect('/')
        except IndexError:
            self.render('/signup-form.html')

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')

class MainPage(FolioHandler):
    def get(self):
        posts = Post.all().order('-created')
        projects = Project.all()
        top4 = posts[0:4]
        posts = top4
        self.response.headers['Content-Type'] = 'text/html'
        self.render("content.html", posts = posts, projects = projects)

application = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),                              
                               ('/resume-bio', ResumePage),
                               ('/admin/newpost', NewPost),
                               ('/admin/newproject', NewProject),
                               ('/projects', ProjFront),
                               ('/signup-form', Register),
                               ('/admin/login-form', Login),
                               ('/logout', Logout),
                               #('/admin/register', RegisterInvite),
                               ],
                              debug=True)