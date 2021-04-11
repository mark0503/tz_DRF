from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post-detail', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'url', 'comments']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'url', 'posts')


UserModel = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail', read_only=True)
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post', 'url']
