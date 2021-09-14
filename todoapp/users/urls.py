from django.conf.urls import url
from .views import Login, GetUser


urlpatterns = [
    url('login$', Login.as_view(), name='user-login'),
    url('get-user$', GetUser.as_view(), name='get-user')
]