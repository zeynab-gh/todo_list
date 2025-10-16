from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TodoViewSet, 
    CategoryViewSet, 
    UserRegistrationView, 
    UserProfileView,
    UserLoginView,
    UserLogoutView,
  
)

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication URLs
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),  # یا از user_login استفاده کنید
    path('api/auth/logout/', UserLogoutView.as_view(), name='logout'),  # یا از user_logout استفاده کنید
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # برای Session Authentication (اختیاری)
    path('api-auth/', include('rest_framework.urls')),
]