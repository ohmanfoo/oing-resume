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

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

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
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

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
        description = self.request.get('description')
        if title and blurb and url:
            proj = Project(parent = project_key(),
                            url = url, 
                            title = title,
                            blurb = blurb,
                            description = description)
            proj.put()
            self.redirect('/')
        else:
            error = "project arguments error"
            self.render("newproject.html", url = url,
                                        title = title,
                                        blurb = blurb,
                                        description = description,
                                        error = error)

class EditPortfolio(FolioHandler):
# admin edit handler for all models
# make edits with knockout.js -> json -> unpack -> put
# changes to the model are reflected in non js frontpages
# send all data to this area with all pages/data in drop down lists.
# Handle Adding New Projects and Skills and all Edits
# need functions to validate incoming json for all models
    def get(self):
        if self.user:
            bio = Bio.all()
            projects = Project.all()
            skills = Skill.all()
            contact = Contact.all()
            self.response.headers['Content-Type'] = 'text/html'
            self.render("/admin/editportfolio.html", bio = bio,
                                            projects = projects,
                                            skills = skills,
                                            contact = contact)
        else:
            self.redirect("/admin/login-form")
    def post(self):
        if not self.user:
            self.redirect("/")
        url = self.request.get('url')
        title = self.request.get('title')
        blurb = self.request.get('blurb')
        description = self.request.get('description')
        if title and blurb and url:
            pro = Project(parent = project_key(),
                            url = url, 
                            title = title,
                            blurb = blurb,
                            description = description)
            pro.put()
            self.redirect('/')
        else:
            error = "project arguments error"
            self.render("newproject.html", url = url,
                                        title = title,
                                        blurb = blurb,
                                        error = error)


# class EditBio(FolioHandler):
#     def get(self):
#         if self.user:
#             bio = Bio.all()
#             self.render("/admin/biography.html", bio = bio)
#         else:
#             self.redirect("/admin/login-form")
#     def post(self):
#         if not self.user:
#             self.redirect('/')
#         update = self.request.get('bio')
#         old_bio = Bio.all()

# class EditContact(FolioHandler):
#     def get(self):
#         if self.user:
#             contact = Contact.all()
#             self.render("/admin/biography.html", bio = bio)
#         else:
#             self.redirect("/admin/login-form")
#     def post(self):
#         if not self.user:
#             self.redirect('/')
#         email = self.request.get('email')
#         twitter = self.request.get('twitter')
#         github = self.request.get('github')
#         linkedin = self.request.get('linkedin')

# class EditSkills(FolioHandler):
#     def get(self):
#         if self.user:
#             self.render("/admin/newskill.html")
#         else:
#             self.redirect("/admin/login-form")
#     def post(self):
#         if not self.user:
#             self.redirect("/")
#         skills = self.request.get('skills').split('')
#         if skills:
#             for i in skills:
#                 skill = Skill(parent = skill_key(), skill = i)
#                 skill.put()
#             self.redirect('/resume-bio')
#         else:
#             error = 'oops'
#             self.render('/admin/newskill.html', error=error)