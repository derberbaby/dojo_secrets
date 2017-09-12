from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self,data):
        errors=[]
        if not data['first_name'].isalpha():
            errors.append("First name may only be letters")
        if len(data['first_name']) < 2:
            errors.append("First name must be more than 2 letters")
        if not data['last_name'].isalpha():
            errors.append("Last name may only be letters")
        if len(data['last_name']) < 2:
            errors.append("Last name must be more than 2 letters")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Invalid email")
        try:
            User.objects.get(email=data['email'])
            errors.append("Email already registered")
        except:
            pass
        if len(data['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if data['password'] != data['confirm']:
            errors.append("Passwords do not match")
        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = data['first_name'], last_name = data['last_name'], email = data['email'], hashed_pw = hashed_pw)
            return user.id
        else:
            return errors

    def login(self,data):
        errors=[]
        try:
            current_user = User.objects.get(email = data['email'])
            encrypted_pw = bcrypt.hashpw(data['password'].encode(), current_user.hashed_pw.encode())
            if current_user.hashed_pw != encrypted_pw:
                errors.append("Incorrect Password")
                return errors
            else:
                return current_user.id
        except:
            errors.append("Email not registered")
            return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    hashed_pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class SecretManager(models.Manager):
    def validate(self,data,user_id):
        errors=[]
        if len(data['secret']) > 0:
            user = User.objects.get(id=user_id)
            secret = Secret.objects.create(user = user, content = data['secret'])
            return True
        else:
            errors.append("Don't be shy, share a secret!")
            return errors

class Secret(models.Model):
    user = models.ForeignKey(User, related_name='all_secrets')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = SecretManager()
