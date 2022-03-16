from django.urls import path
from django_request_mapping import UrlPattern
from . import views

from web.views import MyView

urlpatterns = UrlPattern();
urlpatterns.register(MyView);

