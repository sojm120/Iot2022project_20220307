from django_request_mapping import UrlPattern

from web.views import MyView
from web.views_board import BoardView
from web.views_rest import RestView
from web.views_review import ReviewView

urlpatterns = UrlPattern();
urlpatterns.register(MyView);
urlpatterns.register(RestView);
urlpatterns.register(ReviewView);
urlpatterns.register(BoardView);