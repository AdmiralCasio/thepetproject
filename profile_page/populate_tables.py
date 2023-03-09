import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad2groupproject.settings')

import django
django.setup()

from PIL import Image
from datetime import date

from thepetproject.models import UserProfile, Post, Comment, UserHasLikedComment, UserHasLikedPost
from django.contrib.auth.models import User

def populate():
    users = [
        {'username': 'jeremyjohn145',
        'password': 'password123',
        'name': 'Jeremy John',
        'date_joined': '2022-01-02',
        'picture': 'cat.jpg'},
        {'username': 'johnboy69',
        'password': 'password123',
        'name': 'John Billingsley',
        'date_joined': '2022-03-04',
        'picture':None},
        {'username': 'jesus',
        'password': 'password123',
        'name': 'Jesus, Son of Christ',
        'date_joined': '2022-03-02',
        'picture':'jesus.jpg'},
        {'username': 'yecats',
        'password': 'password123', 
        'name': 'Stacey McLain',
        'date_joined': '2022-09-09',
        'picture':'cat.jpg'}
        
        # {
        #     'username': ,
        #     'password': ,
        #     'name': ,
        #     'date_joined': 
        # }
    ]
    
    posts = [
        {'caption': "isn't he cute",
         'date_posted': '2023-04-06',
         'time_posted': '14:50:22',
         'likes': 1,
         'number_of_comments': 1,
         'posted_by': 'jesus',
         'liked_by': ['yecats'],
         'image':'09012022_112903.mov.00_00_28_21.Still001.jpg'},
        {'caption': "he's so small!",
         'date_posted': '2023-05-04',
         'time_posted':'13:45:32',
         'likes': 1,
         'number_of_comments': 1,
         'posted_by': 'yecats',
         'liked_by': ['jesus'],
         'image':'IMG-20230308-WA0013.jpg'}
    ]
    
    comments = [
        {'text': "this is nice",
         'likes': 0,
         'date_posted': '2023-05-04',
         'time_posted': '14:12:12',
         'posted_by': 'johnboy69',
         'posted_on': 2,
         'liked_by': ['jesus']},
        {'text': "this isn't nice",
         'likes': 1,
         'date_posted': '2023-06-14',
         'time_posted': '13:02:12',
         'posted_by': 'jeremyjohn145',
         'posted_on': 1,
         'liked_by': ['yecats'],
         }
    ]
    
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
    user = User.objects.get_or_create(username=username, password=password)[0]
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
    
    