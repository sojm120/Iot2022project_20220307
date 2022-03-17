import json
import logging

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_request_mapping import request_mapping

from web.models import Cust

from config.settings import UPLOAD_DIR
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
        return render(request, 'search.html');

    @request_mapping("/login", method="get")
    def login(self, request):
        return render(request, 'login.html');

    @request_mapping("/restDetail", method="get")
    def restDetail(self, request):
        # home에서 클릭한 id 가져오기
        rest = Rest.objects.get(id=1);
        star_avg = Review.objects.filter(rest=1).aggregate(s_avg=Avg('s_rating'), m_avg=Avg('m_rating'), p_avg=Avg('p_rating'));
        menu = Menu.objects.filter(rest=1);
        review = Review.objects.filter(rest=1).order_by('-id'); # 내림차순 정렬
        imgpath = Imgpath.objects.all();
        context = {
            'rest': rest,
            'star_avg': star_avg,
            'menu': menu,
            'review': review,
            'imgpath': imgpath,
            'reviewlist': 'reviewlist.html'
        };
        return render(request, 'restDetail.html', context);

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

    @request_mapping("/profile/<str:pk>", method="get")
    def profile(self, request, pk):
        profile = Cust.objects.get(id=pk);
        context = {
            'Cust': profile
        };
        return render(request, 'profile.html',context);

    @request_mapping("/profileupdate/<str:pk>", method="get")
    def profileupdate(self, request, pk):
        profile = Cust.objects.get(id=pk);
        context = {
            'Cust': profile
        };
        return render(request, 'profileupdate.html', context);

    @request_mapping("/profileupdateimpl/<str:pk>", method="post")
    def profileupdateimpl(self, request, pk):
        name = request.POST['name'];
        birth = request.POST['birth'];
        gender = request.POST['gender'];
        email = request.POST['email'];
        phone = request.POST['phone'];
        address = request.POST['address'];

        cust = Cust.objects.get(id=pk);
        cust.name = name;
        cust.birth = birth;
        cust.gender = gender;
        cust.email = email;
        cust.phone = phone;
        cust.address = address;
        cust.save()
        return redirect('/restDetail')

    @request_mapping("/registerimpl", method="post")
    def registerimpl(self, request):
        id = request.POST['custid'];
        pwd = request.POST['custpw'];
        name = request.POST['custname'];
        birth = request.POST['birth'];
        gender = request.POST['gender'];
        email = request.POST['custemail'];
        address1 = request.POST['address1'];
        address2 = request.POST['address2'];
        phone = request.POST['custphone'];
        host_flag = int(request.POST['host_flag']);
        custimg = request.POST['custimg'];

        print(id,pwd,name,birth,gender,email,address1+' '+address2,phone,host_flag,custimg);
        context = {};
        try:
            Cust.objects.get(id = id);
            context['center'] = 'register.html';
        except:
            Cust(id=id, pwd=pwd, name=name, birth=birth, gender=gender, email=email, address=address1+address2, phone=phone, host_flag=host_flag, custimg=custimg).save();
            context['center'] = 'registerok.html';
            context['rname'] = name;
        return render(request, 'home.html', context);

    @request_mapping("/loginimpl", method="post")
    def loginimpl(self, request):
        # id, pwd 를 프로그램을 확인 한다.
        id = request.POST['custid'];
        pwd = request.POST['custpw'];
        try:
            cust = Cust.objects.get(id=id);
            if cust.pwd == pwd:
                request.session['sessionid'] = cust.id;
                request.session['sessionname'] = cust.name;
                request.session['sessionimg'] = cust.custimg;
        except:
            return render(request,'login.html');
        return render(request, 'home.html');

    @request_mapping("/logout", method="get")
    def logout(self, request):
        if request.session['sessionid'] != None:
            del request.session['sessionid'];
        return render(request, 'home.html');

    @request_mapping("/faq", method="get")
    def faq(self, request):
        return render(request, 'faq.html');
