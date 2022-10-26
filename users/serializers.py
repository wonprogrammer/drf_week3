# models에 정의된 objects들을 딕셔너리 형태 즉, JSON형태의 str으로 만들어 자동으로 response 할 수 있게 만들어 주는게 serializers
from dataclasses import field
from rest_framework import serializers
from users.models import User

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