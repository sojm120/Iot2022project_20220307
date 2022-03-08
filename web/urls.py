from django_request_mapping import UrlPattern

from web.views import MyView

urlpatterns = UrlPattern();
urlpatterns.register(MyView);
