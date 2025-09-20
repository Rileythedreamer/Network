import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Post, Follow, Like
from .forms import PostForm

N = 10 # Number of Posts per Page


def paginate_posts(posts, page_number):
    paginator = Paginator(posts, N)
    return paginator.get_page(page_number)


def index(request):
    all_posts = Post.objects.all().order_by("-date_added")
    return render(request, "network/index.html", {
        "page_obj" : paginate_posts(all_posts, request.GET.get('page'))
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
def create_post_view(request):
    if request.method == "POST":
        new_post_form = PostForm(request.POST)
        if new_post_form.is_valid:
            new_post = new_post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "network/create.html", {
        "post_form" : PostForm()
    })

@login_required  
def profile_view(request, profile_id):
    profile_user = User.objects.get(pk=profile_id)
    followers = Follow.objects.filter(followed=profile_user).count()
    followings = Follow.objects.filter(follower=profile_user).count()
    profile_user_posts = Post.objects.filter(author=profile_user).order_by("-date_added")
    print(True if profile_user in request.user.following.all() else False)
    
    return render(request, "network/profile.html", {
        "profile_user":profile_user,
        "followers" : followers,
        "followings" : followings,
        "is_in_followings": Follow.objects.filter(follower=request.user, followed=profile_user),
        "page_obj": paginate_posts(profile_user_posts , request.GET.get('page'))
    })
    
@login_required
def follow_view(request, profile_id):
    profile_user = User.objects.get(pk = profile_id)
    if request.method=="POST":
        action = request.POST.get('action')
        if action == "Follow":
            Follow.objects.create(follower= request.user,followed=profile_user).save()
            
        elif action== "Unfollow":
            Follow.objects.filter(follower= request.user,followed=profile_user).delete()
            
            
        return HttpResponseRedirect(reverse("profile", args=[profile_user.id]))
    
@login_required
def following_view(request):
    following_users = Follow.objects.filter(follower=request.user).values_list("followed")
    posts = Post.objects.filter(author__in=following_users)
    
    return render(request, "network/index.html", {
        "page_obj": paginate_posts(posts, request.GET.get("page"))
    })


@login_required
def edit_post_view(request, post_id):
    if request.method == "GET":
        this_post = Post.objects.get(pk=post_id)
        # print("what is going on")
        print(this_post.content)
        return JsonResponse({"content": this_post.content})
    else:
        data = json.loads(request.body)
        if data.get("content") is not None:
            # print(data["content"])
            post_obj = Post.objects.get(pk=post_id)
            post_obj.content = data["content"]
            post_obj.save()
        return JsonResponse({"success": "."}, status=200)


@login_required
def like_view(request, post_id):
    if request.method == "PUT":
        post_obj = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("liked") is not None:
            print(data["liked"])
            if data["liked"] == True:
                new_like = Like.objects.create(liker=request.user, liked=post_obj)
                new_like.save()
                
            elif data["liked"] == False:
                removing_like = Like.objects.filter(liker=request.user, liked=post_obj)
                removing_like.delete()
                
        likes = post_obj.calculate_likes()
        post_obj.save()
        return JsonResponse({"likes": likes}, status=200)
    