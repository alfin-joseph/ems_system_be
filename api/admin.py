from django.contrib import admin
from .models import Employee, EmployeeFieldDefinition


@admin.register(EmployeeFieldDefinition)
class EmployeeFieldDefinitionAdmin(admin.ModelAdmin):
    list_display = ('field_label', 'field_name', 'field_type', 'is_required', 'order', 'is_active')
    list_filter = ('field_type', 'is_required', 'is_active', 'created_at')
    search_fields = ('field_name', 'field_label')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)
    
    fieldsets = (
        ('Field Configuration', {
            'fields': ('field_name', 'field_label', 'field_type', 'order', 'is_active')
        }),
        ('Validation Rules', {
            'fields': ('is_required', 'min_length', 'max_length', 'min_value', 'max_value', 'pattern'),
            'classes': ('collapse',)
        }),
        ('Options & Default', {
            'fields': ('options', 'default_value'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'role', 'status', 'hire_date', 'created_at')
    list_filter = ('department', 'role', 'status', 'hire_date', 'created_at')
    search_fields = ('name', 'email', 'role', 'department')
    readonly_fields = ('created_at', 'updated_at', 'dynamic_data_display')
    date_hierarchy = 'hire_date'
    
    fieldsets = (
        ('Fixed Information', {
            'fields': ('user', 'name', 'email', 'department', 'role')
        }),
        ('Employment Details', {
            'fields': ('status', 'hire_date')
        }),
        ('Dynamic Data', {
            'fields': ('dynamic_data_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def dynamic_data_display(self, obj):
        import json
        return json.dumps(obj.dynamic_data, indent=2) if obj.dynamic_data else 'No dynamic data'
    dynamic_data_display.short_description = 'Dynamic Data (JSON)'

