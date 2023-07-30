from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import user_view

urlpatterns = [ 
    # path('register', views.register_user, name='register_user'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("adding_user/", views.user_view, name="adding_user"),
    path("add_user/", views.add_user, name="add_user"),
    path("add_api/", views.add_api, name="add_api"),
    path("remove_user/", views.remove_user, name="remove_user"),
    path("update_user/", views.update_user, name="update_user"),
    path("remove_api/", views.remove_api, name="remove_api"),
    path("update_api/", views.update_api, name="update_api"),
    path("view_api/", views.view_api, name="view_api"),
]