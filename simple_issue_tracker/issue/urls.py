from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^register/', register),
    url(r'^login/', user_login),
    url(r'^logout/', user_logout),
    url(r'^create_issue', create_issue),
    url(r'^assign_issue/', assign_issue),
]