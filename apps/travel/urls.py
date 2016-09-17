from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^travels$', views.main, name='main'),
    url(r'^travels/login$', views.login, name='login'),
    url(r'^travels/user$', views.user, name='user'),
    url(r'^travels/destination/(?P<travel_id>\d+)$', views.travel, name='travel'),
    url(r'^travels/add$', views.add, name='add'),
    url(r'^user/login_process$', views.login_process, name='login_process'),
    url(r'^user/register_process$', views.register_process, name='register_process'),
    url(r'^user/logout$', views.logout, name='logout'),
    url(r'^travels/add_travel$', views.add_travel, name='add_travel'),
    url(r'^travels/(?P<travel_id>\d+)/join$', views.join, name='join'),

]
