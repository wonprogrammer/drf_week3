from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from articles import serializers
from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer
from django.db.models import Q


# Create your views here.


# 게시글의 전체 리스트(GET) + 게시글 작성하기(POST)
class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all( )

        # 1. 내가 원하는 objects만 가져오고 싶기 때문에 ArticleSerializer에서 -> ArticleListSerializer로 재정의
        # 2. ArticleListSerializer 에서 정의된 user가 -> 아래함수(def post)에서 인증되려면 serializer 재정의 필요 -> ArticleCreateSerializer 
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FeedView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = Q()
        for user in request.user.followings.all():
            q.add(Q(user=user), q.OR)
        feeds = Article.objects.filter(q)
        serializers = ArticleListSerializer(feeds, many=True)
        return Response(serializers.data)







class ArticleDetailView(APIView):
    # 본인 게시글 가져오기
    def get(self, request, article_id):
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)



    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response("삭제 완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)





class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments,  many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user = request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  




class CommentDetailView(APIView):
    def put(self, request, comment_id, article_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, comment_id, article_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제 완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)





class LikeView(APIView):
    # 좋아요 한적 없으면 post 가능하게 / 있으면 아무기능 없게
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("unlike", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("like", status=status.HTTP_200_OK)
