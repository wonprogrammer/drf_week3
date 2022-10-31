from rest_framework import serializers
from articles.models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # 여기서 정의된 user의 email이 위에 user값에 들어가게 된다
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Comment
        # fields = '__all__'
        # fields : all에서 1개만 제외할때는 exclude 쓸 수 있음
        exclude = ('article', )



class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields가 한개더라도 무조건 ',' 붙여줘야 함 -> 안그러면 str로 인식
        fields = ("content",)



# ----------------------------------------------------------------



class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # ArticleSerializer가 선언된 게시글의 댓글을 볼때 단순 id가 아닌 CommentSerializer에 저장된 정보를 json 형태로 불러 올 수 있다.
    comment_set = CommentSerializer(many=True)
    # ArticleSerializer가 선언된 게시글의 좋아요를 누른 사용자를 볼때 단순 id가 아닌 사용자의 id를 string:문자로 가져오게 할 수 있다.
    likes = serializers.StringRelatedField(many=True)

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
    # 1. list를 불러올때 좋아요 갯수도 불러오고싶을때! + commnets_count도 동일!
    likes_count = serializers.SerializerMethodField()
    commnets_count = serializers.SerializerMethodField()

    # 여기서 정의된 user의 email이 위에 user값에 들어가게 된다
    def get_user(self, obj):
        return obj.user.email

    # 2. 위에서 좋아요 수 정의 해주고, 여기서 갯수 받아오는 함수 정의
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_commnets_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Article
        # 3. likes_count : 좋아요 수 보여주는 필드 추가
        fields = ("pk", "title", "image", "update_at", "user", "likes_count", "commnets_count")
    # 원래 여기서 user 값은 id 값으로 들어 왔었지만 그럼 user가 누군지 정확히 알 수 없기 때문에 14~17번 코드의 정의로 user 값에 email이 들어가도록 설정해준다.


