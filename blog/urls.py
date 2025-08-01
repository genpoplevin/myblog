from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(
        'tag/<slug:tag_slug>/',
        views.post_list,
        name='post_list_by_tag'
    ),
    path(
        'follow/',
        views.follow_index,
        name='follow_index'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        '<int:post_id>/comment/',
        views.post_comment,
        name='post_comment'
    ),
    path(
        'create/',
        views.post_create,
        name='post_create'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/delete/',
        views.post_delete,
        name='post_delete'
    ),
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
]
