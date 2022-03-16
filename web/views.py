from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_request_mapping import request_mapping
import json

from web.models import Rest, Review, Menu, Imgpath


@request_mapping("")
class MyView(View):

    @request_mapping("/", method="get")
    def home(self, request):
        rest = Rest.objects.all();
        star_rating = Review.objects.all();
        imgpath = Imgpath.objects.all();
        context = {
            'rest': rest,
            'star_rating': star_rating,
            'imgpath': imgpath
        };
        return render(request, 'home.html', context);

    @request_mapping("/search", method="get")
    def search(self,request):
        return render(request,'search.html');

    @request_mapping("/login", method="get")
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/register", method="get")
    def register(self, request):
        return render(request, 'register.html');

    @request_mapping("/restDetail", method="get")
    def restDetail(self, request):
        return render(request, 'restDetail.html');

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