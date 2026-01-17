from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import (
    UserCreateSerializer,
    ChangePasswordSerializer,
    EmployeeSerializer,
    EmployeeListSerializer,
    EmployeeFieldDefinitionSerializer,
    EmployeeFormSerializer,
)
from .models import Employee, EmployeeFieldDefinition, EmployeeForm


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'message': 'User created successfully'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {
                    'message': 'Password changed successfully'
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employee Field Definition Views
class EmployeeFieldDefinitionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fields = EmployeeFieldDefinition.objects.all()
        serializer = EmployeeFieldDefinitionSerializer(fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeFieldDefinitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeFieldDefinitionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, field_id):
        try:
            field = EmployeeFieldDefinition.objects.get(id=field_id)
        except EmployeeFieldDefinition.DoesNotExist:
            return Response(
                {'error': 'Field definition not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeFieldDefinitionSerializer(field)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, field_id):
        try:
            field = EmployeeFieldDefinition.objects.get(id=field_id)
        except EmployeeFieldDefinition.DoesNotExist:
            return Response(
                {'error': 'Field definition not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeFieldDefinitionSerializer(field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, field_id):
        try:
            field = EmployeeFieldDefinition.objects.get(id=field_id)
        except EmployeeFieldDefinition.DoesNotExist:
            return Response(
                {'error': 'Field definition not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        field.delete()
        return Response(
            {'message': 'Field definition deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


# Employee Views
class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, emp_id):
        try:
            employee = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, emp_id):
        try:
            employee = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, emp_id):
        try:
            employee = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        employee.delete()
        return Response(
            {'message': 'Employee deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "JWT authentication successful"
        })


class EmployeeFormListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forms = EmployeeForm.objects.all()
        serializer = EmployeeFormSerializer(forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeFormDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, form_id):
        try:
            # For ID 1, get or create the single form
            if form_id == 1:
                form, created = EmployeeForm.objects.get_or_create(
                    pk=1,
                    defaults={
                        'form_name': 'Employee Form',
                        'form_description': 'Master form for employee data collection',
                        'is_active': True,
                    }
                )
            else:
                form = EmployeeForm.objects.get(id=form_id)
        except EmployeeForm.DoesNotExist:
            return Response(
                {'error': 'Form not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeFormSerializer(form)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, form_id):
        try:
            # For ID 1, get or create the single form
            if form_id == 1:
                form, created = EmployeeForm.objects.get_or_create(
                    pk=1,
                    defaults={
                        'form_name': 'Employee Form',
                        'form_description': 'Master form for employee data collection',
                        'is_active': True,
                    }
                )
            else:
                form = EmployeeForm.objects.get(id=form_id)
        except EmployeeForm.DoesNotExist:
            return Response(
                {'error': 'Form not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmployeeFormSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, form_id):
        try:
            form = EmployeeForm.objects.get(id=form_id)
        except EmployeeForm.DoesNotExist:
            return Response(
                {'error': 'Form not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        form.delete()
        return Response(
            {'message': 'Form deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
