from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserprofileSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your views here.


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)




# TokenObtainPairView을 CustomTokenObtainPairView가 상속받는다.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class mocView(APIView):
    # permissions.디폴트 퍼미션 모델 중 : IsAdminUser는 로그인 되어있는지 확인할때 사용 / IsAuthenticated 는 로그인 된 사용자인지 확인!
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        user.is_admin = True
        user.save()
        return Response("get 요청")




class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("unfollow", status=status.HTTP_200_OK)
        else:
            you.followers.add(request.user)
            return Response("follow", status=status.HTTP_200_OK)




class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserprofileSerializer(user)
        return Response(serializer.data)
        