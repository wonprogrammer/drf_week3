# models에 정의된 objects들을 딕셔너리 형태 즉, JSON형태의 str으로 만들어 자동으로 response 할 수 있게 만들어 주는게 serializers
from dataclasses import field
from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleListSerializer


class UserprofileSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField : id표기 / StringRelatedFiled : email 표기
    # followings = serializers.StringRelatedFiled(many=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # 내가 작성한 게시글 보기
    article_set = ArticleListSerializer(many=True)

    # 내가 좋아요 한 게시글 보기
    like_articles = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "followings", "followers", 'article_set', 'like_articles')




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # 사용자가 만든 계정 암호 = 해시값으로 변경 및 db에 전달하기
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, validated_data):
        # 사용자가 만든 계정 암호 = 해시값으로 변경 및 db에 전달하기
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token