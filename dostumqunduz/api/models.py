from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    name = models.CharField(max_length=264)
    last_name = models.CharField(max_length=264)
    picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
    gender = models.BooleanField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')


    def wholename(self):
        return {'name':self.name,'last_name':self.last_name, 'id':self.user.id, 'picture':self.picture.url if self.picture else '', 'gender':self.gender}

    def __str__(self):
        return self.name+' '+self.last_name





class FriendsManager(models.Model):
    current = models.ForeignKey(CustomUser, related_name='friendsmanager', on_delete=models.CASCADE)
    friend_requests = models.ForeignKey(CustomUser, related_name='friend_requests', on_delete=models.CASCADE)

    def accept(self):
        user1 = FriendList.objects.create(friends=self.current, friend=self.friend_requests)
        user1.save()
        user2 = FriendList.objects.create(friends=self.friend_requests, friend=self.current)
        user2.save()
        return str(self.current)+' is now friends with '+str(self.friend_requests)

    class Meta:
        unique_together = ('current', 'friend_requests',)




    def __str__(self):
        return self.current.email

class FriendList(models.Model):
    friends = models.ForeignKey(CustomUser, related_name='friends', blank=True, null=True, on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friend', blank=True, null=True, on_delete=models.CASCADE)
    def get_friends_name(self):
        return {'name':self.friend.profile, 'id':self.friend.id, 'picture':self.friend.profile.picture.url}
    def __str__(self):
        return str(self.friends.profile)+ ' and '+str(self.friend)

class Post(models.Model):
    body= models.TextField()
    created = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post')
    
    def __str__(self):
        return self.body
    class Meta:
        ordering = ['-created']


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_post')

    def __str__(self):
        return self.user.email
    class Meta:
        unique_together = ('post', 'user',)



class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment


class Messages(models.Model):
    message = models.TextField()
    sent_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent')
    received_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    int_sender = models.IntegerField()
    int_receiver = models.IntegerField()


