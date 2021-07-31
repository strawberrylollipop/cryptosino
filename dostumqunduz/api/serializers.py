from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Profile, FriendList, FriendsManager, Comment, Post, CustomUser, Like
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

class ProfileSerializer(serializers.ModelSerializer): 
    picture = serializers.ImageField(required=False, allow_null=True)


    class Meta:
        model = Profile
        fields = ('name', 'last_name', 'picture', 'gender', 'user')
        extra_kwargs = {"picture": {"required": False, "allow_null": True}}





class ProfileForRegisterSerializer(serializers.ModelSerializer): 
    picture = serializers.ImageField(required=False, allow_null=True)


    class Meta:
        model = Profile
        fields = ('name', 'last_name', 'picture', 'gender', 'user')
        extra_kwargs = {"picture": {"required": False, "allow_null": True}}








class TestRegisterSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileForRegisterSerializer()
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
















class TimelineSer(serializers.ModelSerializer): 
    picture = serializers.ImageField(required=False, allow_null=True)
    isfriend = serializers.SerializerMethodField('get_isfriend')
    sentreq = serializers.SerializerMethodField('get_sentreq')
    recreq = serializers.SerializerMethodField('get_recreq')


    class Meta:
        model = Profile
        fields = ('name', 'last_name', 'picture', 'gender', 'user', 'id', 'isfriend', 'sentreq', 'recreq')
        extra_kwargs = {"picture": {"required": False, "allow_null": True}}

    def get_isfriend(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
        quer = FriendList.objects.filter(friends = user, friend=value.user)
        return quer.exists()

    def get_sentreq(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
        quer = FriendsManager.objects.filter(current = user, friend_requests=value.user)
        return quer.exists()

    def get_recreq(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
        quer = FriendsManager.objects.filter(current = value.user, friend_requests=user)
        return quer.exists()





class PostSerializer(serializers.HyperlinkedModelSerializer): 
    image = serializers.ImageField(required=False, allow_null=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('body', 'image', 'user')
        extra_kwargs = {"image": {"required": False, "allow_null": True}}



class PostSerializerTLine(serializers.HyperlinkedModelSerializer): 
    image = serializers.ImageField(required=False, allow_null=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    comment_count = serializers.SerializerMethodField('get_comment_count')
    like_count = serializers.SerializerMethodField('get_like_count')
    liked = serializers.SerializerMethodField('get_liked')

    class Meta:
        model = Post
        fields = ('body', 'image', 'user', 'id', 'comment_count', 'liked', 'like_count')
        extra_kwargs = {"image": {"required": False, "allow_null": True}}


    def get_comment_count(self, value):
        count = value.comments.all().count()
        return count


    def get_liked(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
            return value.likes.filter(user=user, post=value.id).exists()
    def get_like_count(self, value):
        count = value.likes.all().count()
        return count





















class FriendsPostSerializer(serializers.ModelSerializer): 
    image = serializers.ImageField(required=False, allow_null=True)
    userprof = serializers.SerializerMethodField('get_userprof')
    comment_count = serializers.SerializerMethodField('get_comment_count')
    like_count = serializers.SerializerMethodField('get_like_count')
    liked = serializers.SerializerMethodField('get_liked')



    class Meta:
        model = Post
        fields = ('body', 'image', 'id','userprof', 'comment_count', 'liked', 'like_count')
        extra_kwargs = {"image": {"required": False, "allow_null": True}}

    def get_userprof(self, value):
        serializer = ProfileSerializer(instance=value.user.profile)
        return serializer.data


    def get_comment_count(self, value):
        count = value.comments.all().count()
        return count


    def get_liked(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
            return value.likes.filter(user=user, post=value.id).exists()
    def get_like_count(self, value):
        count = value.likes.all().count()
        return count





class PostSerializerForFR(serializers.HyperlinkedModelSerializer): 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ('body', 'image', 'user')
        extra_kwargs = {"image": {"required": False, "allow_null": True}}







class FriendsPostSerializerPag(serializers.ModelSerializer): 




    class Meta:
        model = CustomUser
        fields = ('email','id')




















class WriteCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Comment
        fields=('user','post', 'comment', 'id')
        read_only_fields = ('id',)





class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    c_owner = serializers.SerializerMethodField('get_c_owner')

    class Meta:
        model=Comment
        fields=('user','post', 'comment', 'id', 'c_owner')

    def get_c_owner(self, value):
        return value.user.profile.wholename()







class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Like
        fields=('user','post')






class SendFriendRequest(serializers.ModelSerializer): 
    current = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FriendsManager
        fields = ['current', 'friend_requests' ]

class SentFriendRequest(serializers.ModelSerializer): 
    class Meta:
        model = FriendsManager
        fields = ['current', 'friend_requests' ]

class AddFriend(serializers.ModelSerializer):
    class Meta:
        model=FriendList
        fields=('friends','friend')

class AcceptFriendRequest(serializers.ModelSerializer):
    friends = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model=FriendList
        fields=('friend', 'friends')

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            user = request.user
        try:
            if user.friend_requests.get(current_id=validated_data.get('friend').id):
                customer_serializer = AddFriend(data={'friend':validated_data.get('friend').id,'friends':validated_data.get('friends').id})
                if customer_serializer.is_valid():
                    customer_serializer.save()
                customer_serializer2 = AddFriend(data={'friends':validated_data.get('friend').id,'friend':validated_data.get('friends').id})
                if customer_serializer2.is_valid():
                    customer_serializer2.save()
                user.friend_requests.filter(current=validated_data.get('friend')).delete()


                return customer_serializer.validated_data
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)

class ShowFriendsSer(serializers.ModelSerializer):
    friends = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=FriendList
        fields=('friends','friend')




class ListFriendRequestSer(serializers.ModelSerializer):
    class Meta:
        model=FriendsManager
        fields=('friend_requests', 'current')




class IncomingFriendRequestsSer(serializers.ModelSerializer):
    friend_requests = serializers.HiddenField(default=serializers.CurrentUserDefault())
    info = serializers.SerializerMethodField('get_info')

    def get_info(self, value):
        qs = Profile.objects.filter(user=value.current_id)
        serializer = ProfileSerializer(instance=qs, many=True)
        return serializer.data



    class Meta:
        model=FriendsManager
        fields=('friend_requests', 'current','info')







class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)




class SearchSerializer(serializers.ModelSerializer):

    isfriend = serializers.SerializerMethodField('get_isfriend')
    sentreq = serializers.SerializerMethodField('get_sentreq')
    recreq = serializers.SerializerMethodField('get_recreq')

    class Meta:
        model = Profile
        fields = ('name', 'last_name', 'picture', 'gender', 'user', 'isfriend', 'sentreq', 'recreq')

    def get_isfriend(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
        quer = FriendList.objects.filter(friends = user, friend=value.user)
        return quer.exists()

    def get_sentreq(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
        quer = FriendsManager.objects.filter(current = user, friend_requests=value.user)
        return quer.exists()

    def get_recreq(self, value):
        request = self.context.get('request', None)
        if request:
            user = request.user
        quer = FriendsManager.objects.filter(current = value.user, friend_requests=user)
        return quer.exists()
