from django.urls import path
from . import views


urlpatterns = [
    path('adduser/', views.userAdd.as_view(), name='adduser'),
    path('users/', views.usersList.as_view(), name="users"),
    path('users/<int:pk>/', views.userGet.as_view(), name="user"),
    #path('users/<pk>', views.userDetail.as_view(), name="user"),
]
