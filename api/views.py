from rest_framework import generics, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from . import serializers
from django.contrib.auth.models import User
from .models import Post, Comment
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .pagination import ArticlePagination


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = serializers.UserSerializer


class PostList(generics.ListCreateAPIView):
    pagination_class = ArticlePagination
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['owner__username', 'title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    pagination_class = ArticlePagination
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['owner__username']


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CommentList(generics.ListCreateAPIView):
    pagination_class = ArticlePagination
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
