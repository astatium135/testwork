from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from authorization.models import Subscribe

# Create your views here.

def auth(request):
	if not request.user.is_authenticated:
		if request.method == "GET":
			return render(request, "authorization/auth.html")
		else:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user, backend='django.contrib.auth.backends.ModelBackend')
				return redirect("/userinfo")
			else:
				return render(request, "authorization/auth.html", {'error': "Login and password don't find"})
	else:
		return redirect("/userinfo")

def userinfo(request):
	if request.user.is_authenticated:
		return render(request, "authorization/userinfo.html",)
	else:
		return redirect("/")

def out(request):
	logout(request)
	return redirect("/")
	
def signup(request):
	if request.user.is_authenticated:
		return redirect("/userinfo")
	if request.method == "GET":
		return render(request, "authorization/signup.html")
	else:
		username = request.POST.get('username')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		subscribe = request.POST.get('subscribe')
		if User.objects.filter(username=username):
			return render(request, "authorization/signup.html", {'error': "This login already exist"})
		elif password == password2 and len(str(password))>5:
			user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
			user.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		if subscribe:
			Subscribe.objects.create(user=user);
		return redirect("/userinfo")