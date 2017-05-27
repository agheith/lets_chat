from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^process$', views.process),
    url(r'^secrets$', views.secrets),
    url(r'^like/(?P<id>\d+)/(?P<sentby>\w+)$', views.newlike),
    url(r'^delete/(?P<id>\d+)/(?P<sentby>\w+)$', views.delete),
    url(r'^popular$', views.popular),
    url(r'^logout$', views.logout),
]
