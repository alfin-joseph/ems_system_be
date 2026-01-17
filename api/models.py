from django.db import models
from django.contrib.auth.models import User


class EmployeeFieldDefinition(models.Model):
    """Defines the structure of dynamic fields for employees"""
    FIELD_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('EMAIL', 'Email'),
        ('NUMBER', 'Number'),
        ('DATE', 'Date'),
        ('TEXTAREA', 'Text Area'),
        ('SELECT', 'Select Dropdown'),
        ('CHECKBOX', 'Checkbox'),
        ('RADIO', 'Radio Button'),
        ('FILE', 'File Upload'),
        ('PHONE', 'Phone'),
        ('URL', 'URL'),
        ('DECIMAL', 'Decimal'),
    ]
    
    field_name = models.CharField(max_length=100, unique=True)
    field_label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)
    is_required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # For select, radio, checkbox - store options as JSON
    options = models.JSONField(default=list, blank=True)
    
    # Validation constraints
    min_length = models.IntegerField(null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Pattern for regex validation
    pattern = models.CharField(max_length=500, blank=True, null=True)
    
    # Default value
    default_value = models.CharField(max_length=500, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.field_label} ({self.field_name})"


class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('SALES', 'Sales'),
        ('MARKETING', 'Marketing'),
        ('FINANCE', 'Finance'),
        ('OPERATIONS', 'Operations'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('LEAVE', 'On Leave'),
    ]
    
    # Fixed required fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='OTHER')
    role = models.CharField(max_length=100)
    
    # Dynamic fields stored as JSON
    dynamic_data = models.JSONField(default=dict, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    hire_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['department']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class EmployeeForm(models.Model):
    """Single master form for employee data collection with customizable fields"""
    FIXED_FIELDS = [
        {'id': 'fixed_name', 'name': 'name', 'label': 'Full Name', 'type': 'TEXT', 'required': True, 'order': 1},
        {'id': 'fixed_email', 'name': 'email', 'label': 'Email', 'type': 'EMAIL', 'required': True, 'order': 2},
        {'id': 'fixed_department', 'name': 'department', 'label': 'Department', 'type': 'SELECT', 'required': True, 'order': 3},
        {'id': 'fixed_role', 'name': 'role', 'label': 'Role', 'type': 'TEXT', 'required': True, 'order': 4},
        {'id': 'fixed_hire_date', 'name': 'hire_date', 'label': 'Hire Date', 'type': 'DATE', 'required': False, 'order': 5},
        {'id': 'fixed_status', 'name': 'status', 'label': 'Status', 'type': 'SELECT', 'required': False, 'order': 6},
    ]
    
    form_name = models.CharField(max_length=255, default='Employee Form')
    form_description = models.TextField(blank=True)
    
    # Store field configuration as JSON array
    # Each field object: {id, name, label, type, required, order, options, validation, etc.}
    fields = models.JSONField(default=list)  # Stores custom fields
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.form_name
    
    def save(self, *args, **kwargs):
        """Ensure only one form exists"""
        if not self.pk and EmployeeForm.objects.exists():
            # Update existing form instead of creating new one
            existing = EmployeeForm.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_form(cls):
        """Get or create the single employee form"""
        form, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'form_name': 'Employee Form',
                'form_description': 'Master form for employee data collection',
                'is_active': True,
            }
        )
        return form
    
    def get_all_fields(self):
        """Returns fixed fields + custom fields in order"""
        all_fields = self.FIXED_FIELDS.copy()
        all_fields.extend(self.fields)
        return sorted(all_fields, key=lambda x: x.get('order', 0))
