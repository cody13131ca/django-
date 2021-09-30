from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # トップページのリンク
    path('likeordering', views.Indexlike.as_view(), name='indexlike'),
    # トップページのリンク(いいねの多い順)
    path('post_create', views.PostCreate.as_view(), name='post_create'),
    # 新規投稿ページのリンク
    path(
        'post_detail/<int:pk>',
        views.PostDetail.as_view(),
        name='post_detail'),
    # 詳細画面表示
    path(
        'post_update/<int:pk>',
        views.PostUpdate.as_view(),
        name='post_update'),
    # 更新画面表示
    path(
        'post_delete/<int:pk>',
        views.PostDelete.as_view(),
        name='post_delete'),
    # 削除画面
    path('post_list', views.PostList.as_view(), name='post_list'),
    # リスト画面
    path('login', views.Login.as_view(), name='login'),
    # ログイン画面
    path('logout', views.Logout.as_view(), name='logout'),
    # ログアウト画面
    path('signup', views.SignUp.as_view(), name='signup'),
    # サインアップ画面
    path('like/<int:post_id>', views.Like_add, name='like_add'),
    path('dislike/<int:post_id>', views.DisLike_add, name='dislike_add'),
    # いいね・よくないね
    path('category_list', views.CategoryList.as_view(), name='category_list'),
    path(
        'category_detail/<str:name_en>',
        views.CategoryDetail.as_view(),
        name='category_detail'),
    # カテゴリー
    path('tag_list', views.TagList.as_view(), name='tag_list'),
    path(
        'tag_detail/<str:name>',
        views.TagDetail.as_view(),
        name='tag_detail'),
    # タグ
    path('search', views.Search, name='search'),
    # 検索


]
