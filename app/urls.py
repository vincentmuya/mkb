from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url("login", views.login_request, name="login"),
    url("logout", views.logout_request, name="logout"),
    url("new/client", views.new_client, name="new_client"),
    url("client_list", views.client_list, name="client_list"),
    url(r'^update/client/(?P<pk>\d+)/$', views.update_client, name='update-client'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.client_detail, name='client_detail'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^search$', views.search_results, name='search_results'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
