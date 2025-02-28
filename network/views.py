from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages

from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by('-date_time')
    return render(request, "network/index.html", {
        'posts': posts
    })

def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = profile_user.posts.all()
    return render(request, 'network/profile.html', {
        'profile_user': profile_user,
        'posts': posts
    })


@require_POST
def create_newPost(request):
    # Get post conent from submit form
    content = request.POST.get('text', '').strip()
    if content:
         # Creating a new object to Posts
        Posts.objects.create(
            author = request.user,
            content = content
        )
        messages.success(request, 'Post successfully created!')
        # Redirect after create new post
        return redirect("index")
    else:
        messages.info(request, "Content cannot be empty!")
        return redirect("index")  


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
