from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Todo, Category
from .serializers import (
    TodoSerializer, CategorySerializer, TodoCreateSerializer,
    UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer
)
from .permissions import IsOwner
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Todo.objects.filter(user=user)
        
        # فیلتر بر اساس وضعیت
        status_filter = self.request.query_params.get('status', None)
        if status_filter == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif status_filter == 'active':
            queryset = queryset.filter(is_completed=False)
        
        # فیلتر بر اساس دسته‌بندی
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # فیلتر بر اساس اولویت
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # جستجو در عنوان و توضیحات
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # مرتب‌سازی
        sort = self.request.query_params.get('sort', '-created_at')
        if sort in ['title', '-title', 'created_at', '-created_at', 'due_date', '-due_date']:
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TodoCreateSerializer
        return TodoSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        """تغییر وضعیت انجام/انجام نشده"""
        todo = self.get_object()
        todo.toggle_complete()
        serializer = self.get_serializer(todo)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """آمار کلی تسک‌ها"""
        todos = self.get_queryset()
        stats = {
            'total': todos.count(),
            'completed': todos.filter(is_completed=True).count(),
            'active': todos.filter(is_completed=False).count(),
            'high_priority': todos.filter(priority='high', is_completed=False).count(),
            'overdue': todos.filter(due_date__lt=timezone.now(), is_completed=False).count(),
        }
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """تسک‌های آینده"""
        todos = self.get_queryset().filter(
            due_date__gt=timezone.now(),
            is_completed=False
        ).order_by('due_date')[:10]
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(APIView):
    """
    ویو برای ثبت‌نام کاربر - بدون نیاز به CSRF
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'success': True,
                'user': UserProfileSerializer(user).data,
                'token': token.key,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Registration failed'
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    """
    ویو برای ورود کاربر - بدون نیاز به CSRF
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            
            return Response({
                'success': True,
                'user': UserProfileSerializer(user).data,
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Login failed'
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutView(APIView):
    """
    ویو برای عملیات logout کاربر
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        خروج کاربر از سیستم
        """
        try:
            # لاگاوت کردن کاربر
            logout(request)
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Logout failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(APIView):
    """
    ویو برای مشاهده و ویرایش پروفایل کاربر
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        دریافت اطلاعات پروفایل کاربر
        """
        serializer = UserProfileSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        })
    
    def put(self, request, *args, **kwargs):
        """
        ویرایش اطلاعات پروفایل کاربر
        """
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'user': serializer.data,
                'message': 'Profile updated successfully'
            })
        else:
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Profile update failed'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        """
        ویرایش جزئی اطلاعات پروفایل کاربر
        """
        return self.put(request, *args, **kwargs)