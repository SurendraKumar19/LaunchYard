from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^register/', register),
    url(r'^login/', user_login),
    url(r'^logout/', user_logout),
    url(r'^create_issue', create_issue),
    url(r'^assign_issue/', assign_issue),
    url(r'^get_all_issues/', get_all_issues),
    url(r'^get_user_assigned_issues/', get_user_assigned_issues),
    url(r'^update_issue/', update_issue),
]