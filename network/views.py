from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
from .models import User,NPost_model,Profile

#ADD A NEW MODEL CALLED FOLLOW WHERE USER IS CHAR NOT FOREIGN KEY

def index(request):
   posts=NPost_model.objects.all()
   paginator=Paginator(posts,3)
   page_number=request.GET.get('page')
   page_obj=paginator.get_page(page_number)
   if request.user.is_authenticated:
    owner=User.objects.get(username=request.user)
    return render(request, "network/index.html",{ "Posts":page_obj,
                                                "Owner":owner})
   else:
        return render(request, "network/index.html",{ "Posts":NPost_model.objects.all})
       

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
            if user.is_authenticated:
                Profile.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def npost(request):
 
 if request.user.is_authenticated:

    if request.method=="POST":
        user=User.objects.get(username=request.user)
        content=request.POST['new_form']
        NPost_model.objects.create(users=user, post_content=content)
   
    return render(request,"network/new_post.html")
 
def user_profile(request,profile_user):

    user_name=User.objects.get(username=profile_user)
    posters=get_object_or_404(Profile,user=user_name)
    posts=NPost_model.objects.filter(users=user_name).order_by('post_content')

    following=False
    if request.user.is_authenticated:
     user=User.objects.get(username=request.user)

     for follower in posters.followers.all():
      if follower==user:
        following=True 

     return render(request,"network/profile.html",{"posts":posts,"profile_following":posters.num_following,"profile_followers":posters.num_followers, "profile_user":posters.user,"user":user,"bool_following":following, "poster_id":posters.pk})
    
    else:

        return render(request,"network/profile.html",{"posts":posts,"profile_following":posters.num_following,"profile_followers":posters.num_followers, "profile_user":posters.user,"poster_id":posters.pk})


def follow(request,user_id):

    if request.method=="POST":

        requester=User.objects.get(username=request.user)
        user_1=Profile.objects.get(user=requester)

        profile=Profile.objects.get(id=user_id)
        user_2=User.objects.get(username=profile.user)

        user_1.following.add(user_2)
        user_1.save()
        user_1.num_following= user_1.num_following+1
        user_1.save()

        profile.followers.add(requester)
        profile.save()
        profile.num_followers=profile.num_followers+1
        profile.save()

        return HttpResponseRedirect(reverse("index"))

def unfollow(request,user_id):

    if request.method=="POST":

        requester=User.objects.get(username=request.user)
        user_1=Profile.objects.get(user=requester)

        profile=Profile.objects.get(id=user_id)
        user_2=User.objects.get(username=profile.user)

        user_1.following.remove(user_2)
        user_1.save()
        user_1.num_following-=1
        user_1.save()

        profile.followers.remove(requester)
        profile.save()
        profile.num_followers-=1
        profile.save()

        return HttpResponseRedirect(reverse("index"))
def user_authentication(request,post_id):
   
   clicked_post=NPost_model.objects.get(pk=post_id)
   user=clicked_post.users

   if request.user==user:
      value={"boolean":1}

      return JsonResponse(value)
   else:
      value={"boolean":0}

      return JsonResponse(value)
      
      
   
'Add a if statement that returns the newpost page when the edit post button is clicked'
def create_edit(request,post_id):

    post=NPost_model.objects.get(pk=post_id)
    data={"content":post.post_content}

    return JsonResponse(data)

def recieve_edit(request):
 
 if request.method == "POST":
        
        data = json.loads(request.body)
        content = data.get("post_content", "")
        pkey = data.get("pk", "")

        try:
            post = NPost_model.objects.get(pk=pkey)
            post.post_content = content
            post.save()

            return JsonResponse({'message': 'Post updated successfully'}, status=200)
        
        except NPost_model.DoesNotExist:

            return JsonResponse({'error': 'Post not found'}, status=404)
 return JsonResponse({'error': 'Invalid request method'}, status=400)

 #return JsonResponse({"result":"Edit made successfully"}, status=201)

 #get the pk of the post, take this function and comebine it with the other function

 '''post.post_content=data.get("post_content")
        post.save()'''

def following_page(request,user):

    account=Profile.objects.get(user=request.user)
    array=[]

    for person in account.following.all():
       for post in NPost_model.objects.filter(users=person):
           array.append(post)
    
    return render(request,"network/Following.html",{"posts":array})

def liked_or_not_liked(user_request,liked_post,liked):
     
     if(liked):
        liked_post.user_likes.add(user_request)
        
     else:
        liked_post.user_likes.remove(user_request)

     liked_post.save()

   
@login_required
def like_post(request,user_id):
   if(request.method=="POST"or request.method=="GET"):
    user_request=User.objects.get(username=request.user.username)
    liked_post= NPost_model.objects.get(pk=user_id)

    if(user_request not in liked_post.user_likes.all()):
         liked={"bool_value":0}

         if(request.method=="POST"):
           liked={"bool_value":1}
           liked_or_not_liked(user_request=user_request, liked_post=liked_post,liked=liked.get("bool_value"))
        
    else:
         liked={"bool_value":1}

         if(request.method=="POST"):
           liked={"bool_value":0}
           liked_or_not_liked(user_request=user_request, liked_post=liked_post,liked=liked.get("bool_value"))
   
    liked_post.likes=liked_post.user_likes.count()
    liked.update({"number_of_likes":liked_post.likes})

    return JsonResponse(liked)       