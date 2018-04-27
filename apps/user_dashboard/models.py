from __future__ import unicode_literals
from django.db import models
import re
import string

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def basic_validator(self, postData, type):
		errors = {}

		if type == "register":
			if len(postData["first_name"]) < 2 or validate(postData["first_name"]) == False:
				errors["first_name"] = "First Name at least 2 characters and must not contain numbers"
			if len(postData["last_name"]) < 2 or validate(postData["last_name"]) == False:
				errors["last_name"] = "Last Name at least 2 characters and must not contain numbers"
			if postData["password"] != postData["confirm_password"]:
				errors["confirm_password"] = "Password and Confirm password should match"
			if len(postData["password"]) < 8 or len(postData["password"]) == 0:
				errors["password"] = "Password at fewer than 8 characters and not empty"

		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "Invalid Email Address!"

		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	user_level = models.IntegerField()
	description = models.TextField(default='')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()


class Post(models.Model):
	post_message = models.TextField(default='')
	posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster_by", default="")
	posted_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster_to", default="")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Comment(models.Model):
	comment_message = models.IntegerField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment", default="")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor", default="")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()



def validate(name):
    digits = set(string.digits)
    pwd = set(name)

    return pwd.isdisjoint(digits)
