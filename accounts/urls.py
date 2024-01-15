from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    ProfileView,
    UserRegistrationApiView,
    activate,
    UserLoginApiView,
    UserLogoutApiView,
    UserViewset,
)
router = DefaultRouter()
router.register('', UserViewset)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile' ),
    path('activate/<uid64>/<token>/', activate, name='activate'),
    
    path('api/register/', UserRegistrationApiView.as_view(), name='api-register'),
    path('api/login/', UserLoginApiView.as_view(), name='api-login'),
    path('api/logout/', UserLogoutApiView.as_view(), name='api-logout'),
    path('api/', include(router.urls)),

]
# urlpatterns = [
#     path('profile/', ProfileView.as_view(), name='profile' ),
    
#     path('register/', UserRegistrationApiView.as_view(), name='register'),
#     path('login/', UserLoginApiView.as_view(), name='login'),
#     path('logout/', UserLogoutApiView.as_view(), name='logout'),
#     path('api/', include(router.urls)),
#     path('active/<uid64>/<token>/', activate, name='active'),
# ]