"""soc_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static

from auths.views import (
    CustomUserViewSetTrial,
    PhoneViewSet,
    TrialApiView,
)
from chats.views import (
    ChatViewSet,
    ChatModelApiView
)

urlpatterns = [
    path(settings.ADMIN_SITE_URL, admin.site.urls),
    path("api/v1/pp", TrialApiView.as_view()),
    path("api/v1/cc", ChatModelApiView.as_view())
] + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]


# --------------------------------------
# API Endpoints
#
router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)
router.register('auths/users', CustomUserViewSetTrial)
router.register('auths/phones', PhoneViewSet)
router.register('chats/chats', ChatViewSet)

urlpatterns += [
    path(
        'api/v1/',
        include(router.urls)
    )
]
