from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    ProtectedView,
    UserCreateView,
    ChangePasswordView,
    EmployeeListCreateView,
    EmployeeDetailView,
    EmployeeFieldDefinitionListCreateView,
    EmployeeFieldDefinitionDetailView,
    EmployeeFormListCreateView,
    EmployeeFormDetailView,
)

urlpatterns = [
    # User endpoints
    path("register/", UserCreateView.as_view(), name="user_create"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    
    # Token endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Employee Field Definition endpoints
    path("employee-field-definitions/", EmployeeFieldDefinitionListCreateView.as_view(), name="field_definition_list_create"),
    path("employee-field-definitions/<int:field_id>/", EmployeeFieldDefinitionDetailView.as_view(), name="field_definition_detail"),
    
    # Employee Form endpoints
    path("forms/", EmployeeFormListCreateView.as_view(), name="form_list_create"),
    path("forms/<int:form_id>/", EmployeeFormDetailView.as_view(), name="form_detail"),
    
    # Employee endpoints
    path("employees/", EmployeeListCreateView.as_view(), name="employee_list_create"),
    path("employees/<int:emp_id>/", EmployeeDetailView.as_view(), name="employee_detail"),
]