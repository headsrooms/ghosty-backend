"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from Ghosty_API import views

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter(trailing_slash=False)

router.register(r'works', views.WorkViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
                  url(r'^api/', include(router.urls, namespace='api')),
                  # url(r'^users/$', views.UserList.as_view()),
                  # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
                  url(r'^admin/', admin.site.urls),
                  url(r'^docs/', include('rest_framework_docs.urls')),
                  url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
