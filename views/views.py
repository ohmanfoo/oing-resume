# views.py

import os
import webapp2
from google.appengine.ext import db
import jinja2
from lib.vartools import *
from models.models import *
from oingfolio import jinja_env
from oingfolio import render_str
from oingfolio import *

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

class ProjFront(FolioHandler):
    def get(self):
        projects = Project.all()
        self.render('projects.html', projects = projects)

class BlogFront(FolioHandler):
    def get(self):
        posts = Post.all().order('-created')
        self.render('blog.html', posts = posts)

class ResumePage(FolioHandler):
    def get(self):
        skills = Skill.all()
        bio = Bio.all()
        jobs = Job.all()
        education = Edu.all()
        projects = Project.all()
        self.render('workandedu.html', bio = bio,
            skills = skills,
            jobs = jobs,
            education = education,
            projects = projects)

class ProjPage(FolioHandler):
    def get(self, proj_id):
        key = db.Key.from_path('Proj', int(proj_id), parent = proj_key())
        proj = db.get(key)

        if not proj:
            self.error(404)
            return
        self.render("permalink.html", post = proj)

class PostPage(FolioHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewProject(FolioHandler):
    def get(self):
        if self.user:
            self.render("/admin/newproject.html")
        else:
            self.redirect("/admin/login-form")

    def post(self):
        if not self.user:
            self.redirect("/")

        url = self.request.get('url')
        title = self.request.get('title')
        blurb = self.request.get('blurb')

        if title and blurb and url:
            pro = Project(parent = project_key(),
                            url = url, 
                            title = title,
                            blurb = blurb)
            pro.put()
            self.redirect('/')
        else:
            error = "project arguments error"
            self.render("newproject.html", url = url,
                                            title = title,
                                            blurb = blurb,
                                            error = error)

class NewPost(FolioHandler):
    def get(self):
        if self.user:
            self.render("/admin/newpost.html")
        else:
            self.redirect("/admin/login-form")

    def post(self):
        if not self.user:
            self.redirect("/")

        subject = self.request.get('subject')
        content = self.request.get('content')
    	val = self.request.cookies.get('user_id').split('|')[0]
        createdby = User.by_id(int(val)).name

        if subject and content and createdby:
            p = Post(parent = blog_key(), subject = subject, 
            			content = content, 
            			createdby = createdby)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'subject and content are both required'
            self.render('/admin/newpost.html', subject=subject, 
            			content=content, 
            			error=error)

class NewJob(FolioHandler):
    def get(self):
        if self.user:
            self.render("/admin/newjob.html")
        else:
            self.redirect("/admin/login-form")

    def post(self):
        if not self.user:
            self.redirect("/")

        subject = self.request.get('subject')
        content = self.request.get('content')
        val = self.request.cookies.get('user_id').split('|')[0]
        createdby = User.by_id(int(val)).name

        if subject and content and createdby:
            p = Post(parent = blog_key(), subject = subject, 
                        content = content, 
                        createdby = createdby)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'subject and content are both required'
            self.render('/admin/newpost.html', subject=subject, 
                        content=content, 
                        error=error)

class NewEdu(FolioHandler):
    def get(self):
        if self.user:
            self.render("/admin/newedu.html")
        else:
            self.redirect("/admin/login-form")

    def post(self):
        if not self.user:
            self.redirect("/")

        subject = self.request.get('subject')
        content = self.request.get('content')
        val = self.request.cookies.get('user_id').split('|')[0]
        createdby = User.by_id(int(val)).name

        if subject and content and createdby:
            p = Post(parent = blog_key(), subject = subject, 
                        content = content, 
                        createdby = createdby)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'subject and content are both required'
            self.render('/admin/newpost.html', subject=subject, 
                        content=content, 
                        error=error)

class EditSkills(FolioHandler):
    def get(self):
        if self.user:
            self.render("/admin/newskill.html")
        else:
            self.redirect("/admin/login-form")

    def post(self):
        if not self.user:
            self.redirect("/")

        skills = self.request.get('skills').split('')

        if skills:
            for i in skills:
                skill = Skill(parent = skill_key(), skill = i)
                skill.put()
            self.redirect('/resume-bio')
        else:
            error = 'oops'
            self.render('/admin/newskill.html', error=error)

class UpdateBio(FolioHandler):
    def get(self):
        if self.user:
            bio = Bio.all()
            self.render("/admin/biography.html", bio = bio)
        else:
            self.redirect("/admin/login-form")
    def post(self):
        if not self.user:
            self.redirect('/')
        update = self.request.get('bio')
        old_bio = Bio.all()
        #update bio




application = webapp2.WSGIApplication([('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/admin/newpost', NewPost),
                               ('/admin/newproject', NewProject),
                               # ('/admin/signup-form', Register),
                               #('/admin/login-form', Login),
                               #('/logout', Logout),

                               #('/admin/register', RegisterInvite),
                               ],
                              debug=True)
