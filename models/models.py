# models.py

from google.appengine.ext import db
from lib.vartools import *

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def project_key(project = 'default'):
    return db.Key.from_path('projects', project)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty(required = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())
    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u
    @classmethod
    def register(cls, name, pw, email):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class Project(db.Model):
    url = db.StringProperty(required = True)
    #img = 
    title = db.StringProperty(required = True)
    blurb = db.StringProperty(multiline = True)
    description = db.TextProperty()
    last_modified = db.DateTimeProperty(auto_now = True)
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render("project.html", app = self)
    def as_dict(self):
        time_fmt = '%c'
        d = {'title': self.title,
             'url': self.url,
             'description': self.description,
             'blurb': self.blurb,
             'last_modified': self.last_modified}
        return d

class Bio(db.Model):
    fname = db.StringProperty(required = True)
    lname = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
    def as_dict(self):
        time_fmt = '%c'
        d={ 'fullname' : self.fullname,
            'blurb': self.blurb,
            'last_modified': self.last_modified}
        return d

class Skill(db.Model):
    skill = db.StringProperty(required = True)
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
    def as_dict(self):
        time_fmt = '%c'
        d = {'skill': self.skill}
        return d

class Contact(db.Model):
    email = db.StringProperty(required = True)
    twitter = db.StringProperty(required = True)
    linkedin = db.StringProperty(required = True)
    github = db.StringProperty(required = True)    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
    def as_dict(self):
        time_fmt = '%c'
        d = {'email': self.email,
             'twitter': self.twitter,
             'linkedin': self.linkedin,
             'github': self.github}
        return d
