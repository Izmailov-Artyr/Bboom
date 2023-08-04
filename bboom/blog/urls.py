from django.urls import path, include
from .views import UserList,  PostCreate, PostDel, UserPostList, users_list,  user_posts, add_post, delete_post


urlpatterns = [
    path('api/v1/posts/', PostCreate.as_view(), name='post-list'),
    path('api/v1/users', UserList.as_view(), name='users'),
    path('api/v1/auth/', include('rest_framework.urls'), name='auth'),
    path('api/v1/posts/<int:pk>/', PostDel.as_view(), name='del-post'),
    path('api/v1/users/<int:user>/', UserPostList.as_view(), name='user-post'),
    path('', users_list, name='users-list'),
    path('posts/<int:pk>/', user_posts, name='user-posts'),
    path('post/add/', add_post, name='add_post'),
    path('post/del/<int:pk>/', delete_post, name='delete-post')
]