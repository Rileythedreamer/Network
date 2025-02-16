from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from .models import User, Post, Follow, Like


N = 10  
#number of posts on each page

#function for paginating posts:
def paginate_posts(queryset, request):
    posts_paginator = Paginator(queryset, N)
    page_number = request.GET.get('page', 1)
    page_obj = posts_paginator.get_page(page_number)
    return page_obj

def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    page_obj = paginate_posts(posts, request)
    return render(request, "network/index.html", {
        "page_obj" : page_obj
    })


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


@login_required
def create_new_post(request):
    if request.method=="POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newpost.html", {
            "newPostForm" : PostForm()
        })
        
        

def profile_page(request, username):
    profile_user = User.objects.get(username=username)
    followings = []
    for following_object in request.user.followings.all():
        followings.append(following_object.following)
    if profile_user in followings:
        is_following = True
    else:
        is_following = False
        
    num_followers = profile_user.followers.count()
    num_followings = profile_user.followings.count()
    if not num_followers:
        num_followers = 0
    if not num_followings:
        num_followings = 0
    return render(request, "network/profile.html",{
        "num_followers" : num_followers,
        "num_followings" : num_followings,
        "profile_user" : profile_user,
        "is_following" : is_following  
    })

def followers_posts_view(request, username):
    profile_user = User.objects.get(username= username)
    followers_queryset = profile_user.followers.all()
    followers = []
    for follow_object in followers_queryset:
        followers.append(follow_object.follower)
    
    posts_by_followers = Post.objects.filter(author__in = followers).order_by('-timestamp')
    page_obj = paginate_posts(posts_by_followers, request)
    return render(request, "network/index.html",{
        "page_obj": page_obj 
    })

def followings_posts_view(request, username):
    profile_user = User.objects.get(username= username)
    followings_queryset = profile_user.followings.all()
    followings = []
    for follow_object in followings_queryset:
        followings.append(follow_object.following)
    posts_by_followings = Post.objects.filter(author__in=followings).order_by('-timestamp')
    page_obj = paginate_posts(posts_by_followings, request)
    return render(request, "network/index.html",{
        "page_obj": page_obj
    })


@login_required
def follow_view(request, username):
    user_following = User.objects.get(username=username)
    Follow.objects.create(
        following = user_following,
        follower = request.user
    )
    return HttpResponseRedirect(reverse("profile", args=(username,)))

@login_required
def unfollow_view(request, username):
    user_unfollowing = User.objects.get(username=username)
    follow_obj = Follow.objects.filter(following= user_unfollowing, follower = request.user)
    follow_obj.delete()
    return HttpResponseRedirect(reverse("profile", args=(username,)))

@login_required
def edit(request, post_id):
    if request.method == "POST":
        content=request.POST["content"]
        
        
        Post.objects.filter(id=post_id).update(content=content)
        return HttpResponseRedirect(reverse("index"))
    else:
        post = Post.objects.get(id=post_id)
        PostForm
        return render(request, "network/edit.html", {
            "post":post
        })
 

@login_required
def like_view(request, post_id):
    liker = request.user
    post = Post.objects.get(id=post_id)
    
    # error catching
    if not liker:
        return JsonResponse({"status": "{Failure : user not logged in.}"})
    
    if not post:
        return JsonResponse({"status": "{Failure : post doesn't exist.}"})
        
    new_like_obj = Like.objects.create(
        liker = liker,
        post = post
    )
    like_count = Like.objects.filter(post=post).count()
    if not new_like_obj:
        return JsonResponse({"status": "{Failur: like wasn't recorded successfuly.}"})
    return JsonResponse({
        "status": "success",
        "like_count":like_count,
        "liked":True
        
        })
    
@login_required
def unlike_view(request, post_id):
    unliker = request.user
    post = Post.objects.get(id=post_id)
    
    # error catching
    if not unliker:
        return JsonResponse({"status": "{Failure : user not logged in.}"})
    
    if not post:
        return JsonResponse({"status": "{Failure : post doesn't exist.}"})
        
    like_obj = Like.objects.filter(
        liker = unliker,
        post = post
    )
    try:
        like_obj.delete()
    except ObjectDoesNotExist:
        return JsonResponse({
            "status": "Failure", 
            "failure_message" : "Like obj does not exist"
            })
    like_count = Like.objects.filter(post=post).count()
    
    return JsonResponse({
        "status": "success",
        "like_count": like_count,
        "liked":False
        })