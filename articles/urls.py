from django.urls import path
from articles import views


urlpatterns = [
    # 게시글 => GET : 게사글 다 불러오고 / POST : 게시글을 작성 할 수 있게끔 하는 페이지
    path('', views.ArticleView.as_view(), name='article_view'),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    # 댓글
    path('comment/', views.CommentView.as_view(), name='comment_view'),
    path('comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'),
    # 좋아요
    path('like/', views.LikeView.as_view(), name='like_view'),
]