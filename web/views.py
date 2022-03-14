from django.db.models import Avg
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping

from web.models import Rest, Review, Menu


@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self,request):
        return render(request,'home.html');

    @request_mapping("/search", method="get")
    def search(self,request):
        return render(request,'search.html');

    @request_mapping("/login", method="get")
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/restDetail", method="get")
    def restDetail(self, request):
        # home에서 클릭한 id 가져오기
        rest = Rest.objects.get(id=1);
        star_avg = Review.objects.filter(rest=1).aggregate(s_avg=Avg('s_rating'), m_avg=Avg('m_rating'), p_avg=Avg('p_rating'));
        menu = Menu.objects.filter(rest=1);
        review = Review.objects.filter(rest=1);
        context = {
            'rest': rest,
            'star_avg': star_avg,
            'menu': menu,
            'review': review
        };
        return render(request, 'restDetail.html', context);

    @request_mapping("/reviewreg", method="get")
    def reviewreg(self, request):
        return render(request, 'reviewreg.html');

    @request_mapping("/regiRest", method="get")
    def regiRest(self, request):
        return render(request, 'regiRest.html');

    @request_mapping("/list", method="get")
    def list(self, request):
        return render(request, 'list.html');

    @request_mapping("/view", method="get")
    def view(self, request):
        return render(request, 'view.html');

    @request_mapping("/write", method="get")
    def write(self, request):
        return render(request, 'write.html');

    @request_mapping("/edit", method="get")
    def edit(self, request):
        return render(request, 'edit.html');

    @request_mapping("/register", method="get")
    def register(self, request):
        return render(request, 'register.html');