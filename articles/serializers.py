from rest_framework import serializers
from articles.models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields가 한개더라도 무조건 ',' 붙여줘야 함 -> 안그러면 str로 인식
        fields = ("content",)



class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # 여기서 정의된 user의 email이 위에 user값에 들어가게 된다
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Article
        fields = '__all__'


# def post
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "image", "content")



# def get
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # 여기서 정의된 user의 email이 위에 user값에 들어가게 된다
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Article
        fields = ("pk", "title", "image", "update_at", "user")
    # 원래 여기서 user 값은 id 값으로 들어 왔었지만 그럼 user가 누군지 정확히 알 수 없기 때문에 14~17번 코드의 정의로 user 값에 email이 들어가도록 설정해준다.


