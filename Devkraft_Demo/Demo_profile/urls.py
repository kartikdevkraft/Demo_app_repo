from rest_framework.routers import DefaultRouter 
from .views import RoleViewSet, UserViewSet

route = DefaultRouter()
route.register('role', RoleViewSet)
route.register('user', UserViewSet)

urlpatterns = route.urls