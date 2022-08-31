from django.urls import path
from .views import (
        MakerMapView, SignInView, SignUpView, 
        LogOutView, ProfileView, UserListView,
        UserView
    )

app_name = 'gis_app'

urlpatterns = [
    path('', MakerMapView.as_view(), name='marker'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user/<int:pk>/', UserView.as_view(), name='user'),
    path('user/list/', UserListView.as_view(), name='users_list'),
]