from django.contrib.auth.models import User
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import parser_classes
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer

from Ghosty_API.models import Work, Customer, Task, Assignment
from .serializers import UserSerializer, WorkSerializer, CustomerSerializer, TaskSerializer, AssignmentSerializer


@parser_classes((JSONParser, FormParser, MultiPartParser))
class UserViewSet(CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)


@parser_classes((JSONParser, FormParser, MultiPartParser))
class WorkViewSet(viewsets.ModelViewSet):
    """
    List all works, or create a new work.
    """

    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    authentication_classes = (OAuth2Authentication,)


@parser_classes((JSONParser, FormParser, MultiPartParser))
class CustomerViewSet(viewsets.ModelViewSet):
    """
    List all customers, or create a new one.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    authentication_classes = (OAuth2Authentication,)


@parser_classes((JSONParser, FormParser, MultiPartParser))
class TaskViewSet(viewsets.ModelViewSet):
    """
    List all tasks, or create a new task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    authentication_classes = (OAuth2Authentication,)


@parser_classes((JSONParser, FormParser, MultiPartParser))
class AssignmentViewSet(viewsets.ModelViewSet):
    """
    List all assignments, or create a new one.
    """

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    authentication_classes = (OAuth2Authentication,)
