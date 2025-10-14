from django.contrib import admin
from .models import Todo, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'todo_count']
    list_filter = ['user']
    search_fields = ['name', 'user__username']
    
    def todo_count(self, obj):
        return obj.todos.count()
    todo_count.short_description = 'تعداد تسک‌ها'

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'priority', 'is_completed', 'due_date', 'created_at']
    list_filter = ['is_completed', 'priority', 'category', 'user']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'title', 'description', 'category')
        }),
        ('وضعیت', {
            'fields': ('is_completed', 'priority', 'due_date')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )