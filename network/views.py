from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by('-date_time')
    paginator = Paginator(posts, 10) #Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj
    })

@csrf_exempt
@login_required
def follow_unfollow(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        data = json.loads(request.body)
        action = data.get('action') # Get follow or unfollow

        if action == 'follow':
            request.user.following.add(target_user)
            response = {
                'message': f'You are now following {target_user.username}',
                'followers': request.user.following.count()
                }
        elif action == 'unfollow':
            request.user.following.remove(target_user)
            response = {
                'message': f'You have unfollowed {target_user.username}',
                'followers': request.user.following.count()
                }
        else:
            response = {'error': 'Invalid action'}
        return JsonResponse(response)


@login_required
def following(request, user_id):
    # Сheck if the user exists and get access to it
    user = get_object_or_404(User, id=user_id)
    # Get all following_id that user are following
    followingListId = user.following.values_list('id', flat=True)
    posts = Posts.objects.filter(author__id__in = followingListId).order_by('-date_time')
    return render(request, 'network/following.html', {
        'posts': posts
    })

def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = profile_user.posts.all().order_by('-date_time')
    paginator = Paginator(posts, 10) #Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_following = profile_user.followers.filter(id=request.user.id).exists()
    return render(request, 'network/profile.html', {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'is_following': is_following
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
