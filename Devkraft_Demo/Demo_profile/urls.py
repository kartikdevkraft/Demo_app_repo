from rest_framework.routers import DefaultRouter 
from .views import RoleViewSet, UserViewSet,UserProfileViewSet
from .views import LoginAPIView, LogoutAPIView
from django.urls import path

route = DefaultRouter()
route.register('role', RoleViewSet)
route.register('user', UserViewSet)
route.register('profile', UserProfileViewSet)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout')
] + route.urls
