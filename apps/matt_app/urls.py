from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index$', views.index, name ='index'),
    url(r'^add_quote$', views.add_quote, name='add_quote'),
    url(r'^add_to_favs/(?P<id>\d+)$', views.add_to_favs, name='add_to_favs'),
    url(r'^remove_from_favs/(?P<id>\d+)$', views.remove_from_favs, name='remove_from_favs'),
    url(r'^show_user/(?P<id>\d+)$', views.show_user, name='show_user'),
    url(r'^logOut$', views.logOut, name='logOut'),
]
