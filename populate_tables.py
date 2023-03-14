import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad2groupproject.settings')

import django
django.setup()

from PIL import Image
from datetime import date

import json
from thepetproject.models import UserProfile, Post, Comment, UserHasLikedComment, UserHasLikedPost
from django.contrib.auth.models import User

def populate():
    with open("population_data.json") as f:
        data = json.load(f)
        
        users = data[0]
        
        posts = data[1]
        
        comments = data[2]
    
    user_list = []
    post_list = []
    
    for user in users:
        user_list.append(add_user(user['username'], user['password'], user['name'], date_joined=user['date_joined'], image_path=user['picture']))
        
    for post in posts:
        post_list.append(add_post(post['caption'], post['date_posted'], post['time_posted'], post['posted_by'], post['likes'], post['number_of_comments'], post['liked_by'], image_path=post['image']))
        
    #TODO: Comment adding
    for comment in comments:
        add_comment(comment['text'], comment['date_posted'], comment['time_posted'], comment['posted_by'], comment['posted_on'], comment['likes'], comment['liked_by'])
        
    for u in UserProfile.objects.all():
        print(f"Created:{u.user}")
        for p in Post.objects.filter(user=u):
            print(f"{u} posted {p} with caption {p.caption}, image {p.image} and comments:")
            for c in Comment.objects.filter(post=p):
               print(f"- {c}: {c.text} by {c.user}")

def add_user(username, password, name, date_joined, image_path=None):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username)
        user.set_password(password)
    else:
        user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get_or_create(user=user, name=name, date_joined=date_joined)[0]
    if image_path:
        user_profile.picture = os.path.join(username, image_path)
    user.save()
    user_profile.save()
    return user_profile

def add_post(caption, date_posted, time_posted, user, likes, number_of_comments, like_users, image_path=None):
    user_record = UserProfile.objects.get_or_create(user=User.objects.get(username=user))[0]
    post = Post.objects.get_or_create(caption=caption, date_posted=date_posted, time_posted=time_posted, user=user_record)[0]
    post.likes = likes
    post.number_of_comments = number_of_comments
    if image_path:
        post.image = f"{user}/posts/{image_path}"
    for like_user in like_users:
        has_liked = UserHasLikedPost.objects.get_or_create(user=UserProfile.objects.get(user=User.objects.get(username=like_user)), post=post)[0]
        has_liked.save()
    post.save()
    return post

def add_comment(text, date_posted, time_posted, user, post, likes, like_users):
    comment = Comment.objects.get_or_create(text=text, user=UserProfile.objects.get(user=User.objects.get(username=user)), post=Post.objects.get(post_id=post), time_posted=time_posted, date_posted=date_posted)[0]
    comment.likes = likes
    for like_user in like_users:
        has_liked = UserHasLikedComment.objects.get_or_create(user=UserProfile.objects.get(user=User.objects.get(username=like_user)), comment=comment)[0]
        has_liked.save()
    comment.save()
    return comment

if __name__ == '__main__':
    print("Starting population script...")
    populate()
    
    