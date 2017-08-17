"""ocs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from app.urls import router as url_router
from app.urls_login import router as url_login_router
from decorator_include import decorator_include
from django.conf import settings
from api.decorator import is_loginned, login_required
from app.views import AppricationError


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(url_router.urls)),
    url(r'', decorator_include([login_required], url_login_router.urls)),
    url(r'', decorator_include([login_required], 'app.urls_login')),
    url(r'', decorator_include([is_loginned], 'app.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls)),

handler500 = AppricationError.as_view()
