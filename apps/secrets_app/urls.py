from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^secrets$', views.secrets, name='secrets'),
    url(r'^like/(?P<secret_id>\d+)$', views.like, name='like'),
    url(r'^unlike/(?P<secret_id>\d+)$', views.unlike, name='unlike'),
    url(r'^delete/(?P<secret_id>\d+)$', views.delete, name='delete'),
    url(r'^popular$', views.popular, name='popular'),
    url(r'^post_secret$', views.post_secret, name='post_secret'),
    url(r'^my_secrets$', views.my_secrets, name='my_secrets'),
    url(r'^other_secrets$', views.other_secrets, name='other_secrets'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^home$', views.home, name='home')
]
