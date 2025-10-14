from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007AFF')
    icon = models.CharField(max_length=50, default='📁')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['name', 'user']
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='todos'
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def toggle_complete(self):
        """تغییر وضعیت انجام تسک"""
        self.is_completed = not self.is_completed
        self.save()
    
    def days_until_due(self):
        """محاسبه روزهای باقی‌مانده تا موعد انجام"""
        if self.due_date:
            delta = self.due_date - timezone.now()
            return delta.days
        return None