from django.contrib import admin
from .models import Profile, CustomUser, Post, FriendsManager, FriendList, Comment, Like

admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(FriendsManager)
admin.site.register(FriendList)
admin.site.register(Comment)
admin.site.register(Like)