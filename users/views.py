from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
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
    # permissions.디폴트 퍼미션 모델 중 : IsAdminUser는 로그인 되어있는지 확인할때 사용 
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        return Response('get 요청')