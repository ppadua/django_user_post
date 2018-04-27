from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from apps.user_dashboard.models import *
from django.contrib import messages
import bcrypt


def index(request):
	return render(request, "user_dashboard/index.html")

def register(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST, "register")

		if len(errors):
			for error in errors:
				messages.add_message(request, messages.WARNING, errors[error], extra_tags='register')

			return redirect("/")
		else:
			user = User()
			user.first_name = request.POST["first_name"]
			user.last_name = request.POST["last_name"]
			user.email = request.POST["email"]
			user.password = bcrypt.hashpw(request.POST["password"].encode('utf8'), bcrypt.gensalt())
			user.save()

			return render(request, "user_dashboard/success.html", {"first_name" : request.POST["first_name"] })

def login(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST, "login")

		if len(errors):
			for error in errors:
				messages.add_message(request, messages.WARNING, errors[error], extra_tags='login')

			return redirect("/")
		else:
			user = User.objects.filter(email=request.POST["email"], password=request.post["password"])


			if not user:
				messages.add_message(request, messages.WARNING, "Wrong email or password", extra_tags='login')
				return redirect("/")
			else:
				return render(request, "user_dashboard/success.html", {"first_name" : user.first().first_name})
