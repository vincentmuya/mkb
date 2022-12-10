from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url("login", views.login_request, name="login"),
    url("register", views.register_request, name="register"),
    url("logout", views.logout_request, name="logout"),
    url("new/product", views.new_property, name="new_property"),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.property_detail, name='property_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
