from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from apps.user_dashboard.models import *
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime

def index(request):
	if "id" in request.session :
		if request.session["user_level"] == 9:
			return redirect("/dashboard/admin")
		else:
			return redirect("/dashboard")
	else:
		return render(request, "user_dashboard/index.html")

def signin(request):
		return render(request, "user_dashboard/signin.html")

def register(request):
	if "id" not in request.session:
		return render(request, "user_dashboard/register.html")
	else:
		if request.session["user_level"] == 1:
			return redirect("/dashboard")
		else:
			return render(request, "user_dashboard/register.html")

def registration(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST, "register")

		if not len(errors):
			for error in errors:
				messages.add_message(request, messages.WARNING, errors[error], extra_tags='register')

			return redirect("/register")
		else:
			if "added_by_admin" not in request.POST:
				if not User.objects.filter(user_level = 9):
					save_user(request.POST, 9)

					request.session["id"] = user.id
					request.session["first_name"] = request.POST["first_name"]
					request.session["last_name"] = request.POST["last_name"]
					request.session["email"] = request.POST["email"]
					request.session["user_level"] = 9

					return redirect("/dashboard/admin")
				else:
					messages.add_message(request, messages.WARNING, "Already have registered admin!", extra_tags='register')
					
					return 	redirect("/register")
			else:
				save_user(request.POST, 1)

				return redirect("/dashboard/admin")

def save_user(data, user_level):
	user = User()
	user.first_name = data["first_name"]
	user.last_name = data["last_name"]
	user.email = data["email"]
	user.password = data["password"]
	user.user_level = user_level
	user.save()

def login(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST, "login")

		if len(errors):
			for error in errors:
				messages.add_message(request, messages.WARNING, errors[error], extra_tags='login')

			return redirect("/signin")
		else:
			user = User.objects.filter(email=request.POST["email"], password=request.POST["password"])

			if not user:
				messages.add_message(request, messages.WARNING, "Wrong email or password", extra_tags='login')
				
				return redirect("/signin")
			else:
				request.session["id"] = user.first().id
				request.session["first_name"] = user.first().first_name
				request.session["last_name"] = user.first().last_name
				request.session["email"] = user.first().email
				request.session["user_level"] = 9 if user.first().user_level == 9 else 1

				return redirect("/dashboard/admin")


def user_dashboard(request):
	if "id" in request.session :
		if request.session["user_level"] == 1:
			return render(request, "user_dashboard/success.html", {"users" : User.objects.all()})
		else:
			return redirect("/dashboard/admin")
	else:
		return redirect("/")

def admin_dashboard(request):
	if "id" in request.session :
		return render(request, "user_dashboard/success.html", {"users" : User.objects.all()})
	else:
		return redirect("/")


def edit_user(request):
	if "id" in request.session :
		if request.session["user_level"] == 9:
			return render(request, "user_dashboard/edit_user.html", {"user" : User.objects.filter(id=request.session["id"]).first()})
		else:
			return redirect("/dashboard")
	else:
		return redirect("/")

def admin_edit_user(request, number):
	if "id" in request.session :
		if request.session["user_level"] == 9:
			return render(request, "user_dashboard/admin_edit_user.html", {"user" : User.objects.filter(id=number).first()})
		else:
			return redirect("/dashboard")
	else:
		return redirect("/")

def admin_update_user(request):
	if request.method == "POST":
		user = User.objects.filter(id=request.POST["user_id"]).first()

		if "email" in request.POST:
			user.email = request.POST["email"]
			user.first_name = request.POST["first_name"]
			user.last_name = request.POST["last_name"]

			if request.session["user_level"] == 9 and "user_level" in request.POST:
				user.user_level = request.POST["user_level"]

			user.save()

		if "password" in request.POST:
			if request.POST["password"] == request.POST["confirm_password"]:
				user.password = request.POST["password"]
				user.save()
			else:
				messages.add_message(request, messages.WARNING, "Password and confirm password is not equal.", extra_tags='password')


		return redirect("/users/edit/"+request.POST["user_id"])
	else:
		return redirect("/")

def normal_edit_user(request):
	user = User.objects.filter(id=request.session["id"]).first()

	if "email" in request.POST:
		user.email = request.POST["email"]
		user.first_name = request.POST["first_name"]
		user.last_name = request.POST["last_name"]
		user.save()

	if "password" in request.POST:
		if request.POST["password"] == request.POST["confirm_password"]:
			user.password = request.POST["password"]
			user.save()
		else:
			messages.add_message(request, messages.WARNING, "Password and confirm password is not equal.", extra_tags='password')

	if "description" in request.POST:
		user.description = request.POST["description"]
		user.save()

	return render(request, "user_dashboard/edit_user.html", {"user" : user})

def show_user(request, number):
	if "id" in request.session :
		context = {
				"user" :  User.objects.filter(id=number).first(),
				"messages" : User.objects.raw("SELECT user_dashboard_post.id as post_id, user_dashboard_post.*, posted_by.* FROM user_dashboard_post JOIN user_dashboard_user ON user_dashboard_user.id  = user_dashboard_post.posted_to_id JOIN user_dashboard_user as posted_by ON posted_by.id  = user_dashboard_post.posted_by_id WHERE user_dashboard_user.id = %s", [number]),
				"comments" : User.objects.raw("SELECT user_dashboard_comment.*, user_dashboard_user.* FROM user_dashboard_comment JOIN user_dashboard_post ON user_dashboard_post.id  = user_dashboard_comment.post_id JOIN user_dashboard_user ON user_dashboard_user.id = user_dashboard_comment.user_id")
			}

		return render(request, "user_dashboard/user_profile.html", context)
	else:
		return redirect("/")


def post_message(request):
	if "id" in request.session :
		if request.method == "POST":
			post = Post()
			post.post_message = request.POST["post_message"]
			post.posted_to = User.objects.filter(id=request.POST["posted_to"]).first()
			post.posted_by = User.objects.filter(id=request.session["id"]).first()
			post.save();

		return redirect("/users/show/"+request.POST["posted_to"])
	else:
		return redirect("/")

def post_comment(request):
	if request.method == "POST":
		comment = Comment()
		comment.comment_message = request.POST["post_comment"]
		comment.user = User.objects.filter(id=request.session["id"]).first()
		comment.post = Post.objects.filter(id=request.POST["post_id"]).first()
		comment.save();
		
	return redirect("/users/show/"+request.POST["posted_to"])

def logoff(request):
	del request.session['id']

	return redirect("/")

