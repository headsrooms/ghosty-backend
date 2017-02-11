from Ghosty_API.models import Work, Deceased, Task
from django.contrib.auth.models import User
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import parser_classes
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer

from .serializers import UserSerializer, WorkSerializer, DeceasedSerializer, TaskSerializer


@parser_classes((JSONParser, FormParser, MultiPartParser))
class UserViewSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes_by_action = {'default': [permissions.IsAuthenticated()],
                                    'update': [TokenHasReadWriteScope()],
                                    'create': [permissions.AllowAny()]}

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return (permission for permission in self.permission_classes_by_action[self.action])
        except KeyError:
            # action is not set return default permission_classes
            return (permission for permission in self.permission_classes_by_action['default'])

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer,)


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
class DeceasedViewSet(viewsets.ModelViewSet):
    """
    List all customers, or create a new one.
    """

    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
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
