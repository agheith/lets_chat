from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
Password_Regex = re.compile(r'^[A-Za-z]+$')
import datetime

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append('Name must be more than 3 characters')
        if len(postData['username']) < 3:
            errors.append('Usernmane must be more than 3 characters')
        if not Password_Regex.match(postData['password']):
            errors.append('Password should be at least characters')
        if postData['password'] != postData ['confirm_password']:
            errors.append('Passwords must match')
        if len(User.objects.filter(username=postData['username']))>0:
            errors.append('Username already exists')
        if len(postData['password'])<8:
            errors.append('Password must be more than 8 characters')
        if len(errors) == 0: #If there are no errors in the form, lets creater the user..
            newuser = User.objects.create(name= postData['name'], username= postData['username'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

    def login(self, postedName):
        try:
            founduser = self.get(username=postedName)
            return(True, founduser)
        except:
            return(False, "Username was not found in our database")


class SecretManager(models.Manager):
    def validate(self, postedSecret, userid):
        # all posted secrets should have more than 3 characters
        if len(postedSecret)<4:
            return(False, "Secrets must be at least four characters long")
        try:
            currentuser = User.objects.get(id=userid)
            self.create(secret=postedSecret, author=currentuser)
            return(True, "Your secret is safe with us")
        except:
            return(False, "We could not create this secret")
    def newlike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "This secret is not found in our database")
        user = User.objects.get(id=userid)
        if secret.author == user:
            return(False, "Shame on you, you shouldn't like your own secrets")
        secret.likers.add(user)
        return(True, "You liked this secret!")
    def deleteLike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "This secret is not found in our database")
        user = User.objects.get(id=userid)
        if secret.author != user:
            return(False, "Shame on you, you shouldn't delete secrets that aren't your own")
        secret.delete()
        return(True, "Secret deleted")

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Secret(models.Model):
    secret = models.CharField(max_length=400)
    author = models.ForeignKey(User)
    likers = models.ManyToManyField(User, related_name="likedsecrets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SecretManager()
