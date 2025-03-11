# Standart libraries
import json

# Django imports
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# network app imports
from .models import User, Posts, Like


def index(request):
    posts = Posts.objects.all().order_by('-date_time')
    paginator = Paginator(posts, 10) #Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Count likes/dislikes and adding new atrributes for post in page_obj
    for post in page_obj:
        post.likes_count = Like.objects.filter(post=post, reaction='like').count()
        post.dislikes_count = Like.objects.filter(post=post, reaction='dislike').count()
        if request.user.is_authenticated:
            post.user_liked = Like.objects.filter(post=post, user=request.user, reaction='like').exists()
            post.user_disliked = Like.objects.filter(post=post, user=request.user, reaction='dislike').exists()

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })

@login_required
@require_POST
def like_dislike(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    # Get reaction
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    reaction = data.get('reaction')

    # Check reacion on correct
    if reaction not in ['like', 'dislike']:
        return JsonResponse({'error': 'Invalid reaction'}, status=400)

     # If the reaction is not specified, return an error
    if not reaction:
            return JsonResponse({'error': 'Reaction is required.'}, status=400)
    
    # Check what reaction has been post and create a new object or update
    like_obj, created = Like.objects.update_or_create(
        user = request.user,
        post = post,
        defaults= {'reaction': reaction}
    )
    # Count all likes and dislikes for the post
    likes = Like.objects.filter(post=post, reaction='like').count()
    dislikes = Like.objects.filter(post=post, reaction='dislike').count()
    count = {'likes': likes, 'dislikes': dislikes}

    # Inform if record has been created or update
    if created:
        response = {'message': f'{reaction.capitalize()} has been added successfully', 'count': count}
    else:
        response = {'message': f'Reaction has been changed to "{reaction}" successfully', 'count': count}

    return JsonResponse(response)
    
@login_required
def editPost(request, post_id):
    if request.method == 'PUT':
        # Get post or response 404
        target_post = get_object_or_404(Posts, id=post_id)

        # Check that request.user is author post
        if request.user.id != target_post.author.id:
            return JsonResponse({'error': 'You are not allowed to edit this post.'}, status=403)

        # Get editContent
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        editContent = data.get('editContent')

        # If the content is not specified, return an error
        if not editContent:
            return JsonResponse({'error': 'Content is required.'}, status=400)

        # Change post value content in Posts 
        target_post.content = editContent
        target_post.save()

        response = {'message': f'Content in post has been change successfully updated.'}
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@require_POST
@login_required
def follow_unfollow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    action = data.get('action') # Get follow or unfollow

    # Check if action specified
    if not action or action not in ['follow', 'unfollow']:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    if target_user.id == request.user.id:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)

    if action == 'follow':
        request.user.following.add(target_user)
        response = {
            'message': f'You are now following {target_user.username}',
            'followers': target_user.followers.count()
            }
    elif action == 'unfollow':
        request.user.following.remove(target_user)
        response = {
            'message': f'You have unfollowed {target_user.username}',
            'followers': target_user.followers.count()
            }
    return JsonResponse(response)


@login_required
def following(request, user_id):
    # Сheck if the user exists and get access to it
    user = get_object_or_404(User, id=user_id)
    # Get all following_id that user are following
    followingListId = user.following.values_list('id', flat=True)
    posts = Posts.objects.filter(author__id__in = followingListId).order_by('-date_time')

    paginator = Paginator(posts, 10) #Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Count likes/dislikes and adding new atrributes for post in page_obj
    for post in page_obj:
        post.likes_count = Like.objects.filter(post=post, reaction='like').count()
        post.dislikes_count = Like.objects.filter(post=post, reaction='dislike').count()
        post.user_liked = Like.objects.filter(post=post, user=request.user, reaction='like').exists()
        post.user_disliked = Like.objects.filter(post=post, user=request.user, reaction='dislike').exists()

    return render(request, 'network/following.html', {
        'page_obj': page_obj
    })

def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = profile_user.posts.all().order_by('-date_time')
    paginator = Paginator(posts, 10) #Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

# Count likes/dislikes and adding new atrributes for post in page_obj
    for post in page_obj:
        post.likes_count = Like.objects.filter(post=post, reaction='like').count()
        post.dislikes_count = Like.objects.filter(post=post, reaction='dislike').count()
        post.user_liked = Like.objects.filter(post=post, user=request.user, reaction='like').exists()
        post.user_disliked = Like.objects.filter(post=post, user=request.user, reaction='dislike').exists()

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
