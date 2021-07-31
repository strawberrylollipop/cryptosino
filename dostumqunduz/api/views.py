from rest_framework import pagination, serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import Profile, CustomUser, Post, Comment, FriendsManager, Like, FriendList
from .serializers import AcceptFriendRequest, ProfileSerializer, UserSerializer, PostSerializer, SendFriendRequest, SentFriendRequest, CommentSerializer, IncomingFriendRequestsSer, FriendsPostSerializer, WriteCommentSerializer, LikeSerializer, SearchSerializer, ShowFriendsSer, TimelineSer, ProfileForRegisterSerializer, FriendsPostSerializerPag, PostSerializerTLine
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import mixins
from django.contrib.auth import login, authenticate
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models.query import QuerySet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse 
from itertools import chain
from django.http import Http404
from django.db.models import Q
from .pagination import StandardResultsSetPagination, SmallResultsSetPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination



class SearchView(APIView):
    def get_object(self, name, last_name):
        try:
            if last_name:
                return Profile.objects.filter(Q(name__iexact=name, last_name__iexact=last_name) | Q(name__iexact=last_name, last_name__iexact=name))
            else:
                return Profile.objects.filter(Q(name__iexact=name) | Q(last_name__iexact=name))
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, name, last_name=None, format=None):
        queryset = self.get_object(name, last_name)
        ser = SearchSerializer(queryset, many=True,  context={'request': request})
        return Response(ser.data)




class TextPost(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser,)




class PostView(APIView):

    parser_classes = (MultiPartParser, JSONParser)


    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CommentView(APIView):
    def post(self, request, format=None):
        serializer = WriteCommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateDeleteCommentView(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(user=self.request.user, pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






class LikeViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer






        

class UnlikeView(APIView):
    def get_object(self, pk):
        try:
            return Like.objects.get(user=self.request.user, post=pk)
        except Like.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    def post(self, request, format=None):
        serializer = LikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GetCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        paginator = StandardResultsSetPagination()
        id = kwargs.get('id', 'Error')
        comm=Comment.objects.filter(post=id)
        result_page = paginator.paginate_queryset(comm, request)
        commentSet=CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(commentSet.data)










class ProfileApiView(APIView):

    parser_classes = [MultiPartParser, JSONParser]


    def post(self, request, format=None, *args, **kwargs):
        data=request.data
        UserSerializerView = UserSerializer(data=data)
        print(UserSerializerView)
        print(data)
        if UserSerializerView.is_valid():
            usern=UserSerializerView.save()
            data['user']=usern.pk
            ProfileSerializerView=ProfileForRegisterSerializer(data=data)
            if ProfileSerializerView.is_valid():
                ProfileSerializerView.save()
                user =  authenticate(request,email=data['email'], password=data['password'])
                if user:
                    login(request, user)
                return Response(ProfileSerializerView.data, status=status.HTTP_201_CREATED)
            usern.delete()
            return Response(ProfileSerializerView.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializerView.errors, status=status.HTTP_400_BAD_REQUEST)

class TestProfileApiView(ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser)

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer





class AcceptFriendRequestView(mixins.CreateModelMixin,
                                GenericViewSet):
    serializer_class=AcceptFriendRequest





class IncomingFriendRequestsView(ListAPIView):
    serializer_class = IncomingFriendRequestsSer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.friend_requests.all()

class IncomingFriendRequestsViewTest(mixins.ListModelMixin,GenericViewSet):
    queryset=FriendsManager
    serializer_class = IncomingFriendRequestsSer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        user = self.request.user
        print(user)
        queryset = self.queryset.objects.filter(friend_requests=user)
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset



class SendFriendRequestApiView(APIView):
    def post(self, request, format=None):
        if request.data['friend_requests']==request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        quer = FriendList.objects.filter(friends = request.user, friend=request.data['friend_requests'])
        print(quer.exists())
        if quer.exists()==False:
            print('\n\n\n\n\n\n\n')
            print(request.data['friend_requests'])
            print(request.user)
            print('\n\n\n\n\n\n\n')
            serializer = SendFriendRequest(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)






class SentFriendRequestApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        sentlist = [person.friend_requests.profile.wholename() for person in user.friendsmanager.all()]
        return Response(sentlist)



class TestMix(APIView):
    def get(self, request, format=None):
        snippets = FriendsManager.objects.all()
        serializer = SendFriendRequest(snippets, many=True)

        CustomUserQueryset = CustomUser.objects.all()
        ProfileQueryset = Profile.objects.all()
        CustomUserSerializerView = UserSerializer(CustomUserQueryset, many=True)
        ProfileSerializerView = ProfileSerializer(ProfileQueryset, many=True)
        return Response({'prof':ProfileSerializerView.data, 'req':serializer.data})



class ProfileGetApiView(APIView):
    def get(self, request, format=None):
        ProfileSerializerView = ProfileSerializer(request.user.profile)
        return Response(ProfileSerializerView.data)

class TimelineView(APIView):
    pagination_class = StandardResultsSetPagination

    def get_object(self, user_pk):
        try:
            return Profile.objects.get(user=user_pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, user_pk, format=None):
        prof = self.get_object(user_pk)
        ProfileSerializerView = TimelineSer(prof, context={
        'request': request
    })
        return Response(ProfileSerializerView.data)



class TimelinePostsView(ListAPIView):
    pagination_class = SmallResultsSetPagination
    serializer_class = PostSerializerTLine

    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['user_pk'])






class FriendsPostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        paginator = SmallResultsSetPagination()
        user = self.request.user
        postarray= [ efriend.friend.post.all() for efriend in user.friends.all()]
        result_list = list(chain.from_iterable(postarray))
        result_page = paginator.paginate_queryset(result_list, request)
        
        serializer=FriendsPostSerializer(result_page, many=True,context={
        'request': request
    })  
        return paginator.get_paginated_response(serializer.data)













class FriendsPostApiViewPag(ListAPIView):
    serializer_class = FriendsPostSerializerPag



    def get_queryset(self):
        return CustomUser.objects.filter(id=1)



    def list(self, request):
        queryset = self.get_queryset()
        serializer = FriendsPostSerializerPag(queryset, many=True, context={'request': request})
        return Response(serializer.data)




class TestFriendsPostApiViewPag(ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=FriendsPostSerializerPag