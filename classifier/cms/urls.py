from django.conf.urls import url
from cms import views

urlpatterns = [
    # 記事
    url(r'^article/$', views.article_list, name='article_list'),   # 一覧
    url(r'^article/add/$', views.article_edit, name='article_add'),  # 登録
    url(r'^article/mod/(?P<article_id>\d+)/$',
        views.article_edit, name='article_mod'),  # 修正
    url(r'^article/del/(?P<article_id>\d+)/$',
        views.article_del, name='article_del'),   # 削除
]
