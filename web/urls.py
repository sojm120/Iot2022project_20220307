from django_request_mapping import UrlPattern

from web.views import MyView
from web.views_review import ReviewView

urlpatterns = UrlPattern();
urlpatterns.register(MyView);
urlpatterns.register(ReviewView);