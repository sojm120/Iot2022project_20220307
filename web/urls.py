from django.urls import path
from django_request_mapping import UrlPattern
from . import views

from web.views import MyView
from .views_rest import RestView
from .views_review import ReviewView

urlpatterns = UrlPattern();
urlpatterns.register(MyView);
urlpatterns.register(RestView);
urlpatterns.register(ReviewView);